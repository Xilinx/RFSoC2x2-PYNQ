#   Copyright (c) 2021, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
os.environ['BOARD'] = 'RFSoC2x2'
import xrfclk
import rfsystem
from smbus2 import SMBus, i2c_msg
import pynq
import pynq.lib
from .constants import *


__author__ = "Yun Rock Qu"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


class BaseOverlay(pynq.Overlay):
    """Base overlay for the board.

    The base overlay contains Pmod 0 and 1, LEDs, RGBLEDs, push buttons,
    switches, and pin control gpio.

    After reloading the base overlay, the I2C and display port should become
    available as well.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_loaded():
            self.iop_pmod0.mbtype = "Pmod"
            self.iop_pmod1.mbtype = "Pmod"
            self.PMOD0 = self.iop_pmod0.mb_info
            self.PMOD1 = self.iop_pmod1.mb_info
            self.PMODA = self.PMOD0
            self.PMODB = self.PMOD1

            self.leds = self.leds_gpio.channel1
            self.leds.setdirection('out')
            self.leds.setlength(4)
            self.rgbleds = [pynq.lib.RGBLED(i) for i in range(2)]
            self.buttons = self.btns_gpio.channel1
            self.buttons.setdirection('in')
            self.buttons.setlength(4)
            self.switches = self.sws_gpio.channel1
            self.switches.setdirection('in')
            self.switches.setlength(4)

            self.gpio_initialized = False
            self.i2c_initialized = False
            self.display_port_initialized = False
            self.rfclks_initialized = False

    def assert_lmk_reset(self):
        """Assert the LMK chip reset.

        This can be done explicitly if users want to reset the chip.

        """
        self.pin_control.register_map.GPIO_DATA[0:0] = 1
        self.rfclks_initialized = False

    def deassert_lmk_reset(self):
        """Pull the LMK chip out from reset mode.

        This is the default behavior after the overlay has been loaded.

        """
        self.pin_control.register_map.GPIO_DATA[0:0] = 0

    def set_syzygy_vio(self, voltage):
        """Set syzygy VIO setting to enable syzygy interface.

        This method will assert the sygyzy interface enable signal first;
        users should be able to see D46 LED is on.
        Then this method will set the specified VIO setting.
        Only volatile memory will be written.

        Parameters
        ----------
        voltage : float
            The desired VIO voltage level.

        """
        self.pin_control.register_map.GPIO_DATA[1:1] = 1
        if voltage not in MCP4716_DAC_REG:
            raise ValueError("Voltage value not supported.")

        with SMBus(MCP_I2C_BUS) as bus:
            msg = i2c_msg.write(MCP_SLAVE_ADDR, MCP4716_DAC_REG[voltage])
            bus.i2c_rdwr(msg)

    def init_gpio(self):
        """Initialize the GPIO control drivers.

        The GPIO pins will control the I2C-SPI converter chip read data path.

        """
        for gpio_num in [330, 331]:
            if not os.path.exists("/sys/class/gpio/gpio{}".format(gpio_num)):
                with open("/sys/class/gpio/export", 'w') as f:
                    f.write('{}'.format(gpio_num))
            with open("/sys/class/gpio/gpio{}/direction".format(
                    gpio_num), 'w') as f:
                f.write('out')
            with open("/sys/class/gpio/gpio{}/value".format(
                    gpio_num), 'w') as f:
                f.write('1')
        self.gpio_initialized = True

    def init_dp(self, service='pynq-x11', force=False):
        """Initialize the display port drivers.

        This should happen after a bitstream is loaded since the display port
        control pins are connected to EMIO pins coming out from PL.

        Parameters
        ----------
        service : str
            The name of the service that uses the display port.
        force : bool
            To force the corresponding service to restart or not.

        """
        if force:
            cmd = "systemctl restart {0}".format(service)
        else:
            cmd = "if systemctl list-units -a --state=active | grep {0} ; " \
                  "then systemctl restart {0} ; fi".format(service)
        ret = os.system(cmd)
        if ret:
            raise RuntimeError(
                'Restarting {} service failed.'.format(service))
        self.display_port_initialized = True

    def init_i2c(self):
        """Initialize the I2C control drivers on RFSoC2x2.
        This should happen after a bitstream is loaded since I2C reset
        is connected to PL pins. The I2C-related drivers are made loadable
        modules so they can be removed or inserted.
        """
        module_list = ['i2c_dev', 'i2c_mux_pca954x', 'i2c_mux']
        for module in module_list:
            cmd = "if lsmod | grep {0}; then rmmod {0}; fi".format(module)
            ret = os.system(cmd)
            if ret:
                raise RuntimeError(
                    'Removing kernel module {} failed.'.format(module))

        module_list.reverse()
        for module in module_list:
            cmd = "modprobe {}".format(module)
            ret = os.system(cmd)
            if ret:
                raise RuntimeError(
                    'Inserting kernel module {} failed.'.format(module))

        self.i2c_initialized = True

    def init_rf_clks(self, lmk_freq=122.88, lmx_freq=409.6):
        """Initialise the LMK and LMX clocks for the radio hierarchy.

        The radio clocks are required to talk to the RF-DCs and only need
        to be initialised once per session.

        """        
        if not self.rfclks_initialized:
            self.assert_lmk_reset()
            self.deassert_lmk_reset()
            if not self.i2c_initialized:
                self.init_i2c()
            xrfclk.set_ref_clks(lmk_freq=lmk_freq, lmx_freq=lmx_freq)
            self.rfclks_initialized = True

