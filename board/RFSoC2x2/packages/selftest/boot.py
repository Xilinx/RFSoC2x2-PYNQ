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
import logging
from time import time, sleep
from datetime import datetime
import netifaces
import pandas as pd
from pynq import get_rails, DataRecorder
from pynq.overlays.base import BaseOverlay
import xrfdc
# TODO: FIX
# from rfsystem.transmitter import Transmitter
# from rfsystem.receiver import Receiver
# from rfsystem.data_inspector import Visualiser
from rfsystem.spectrum_sweep import SpectrumSweep


__author__ = "Yun Rock Qu"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


# Test constants
V_ERR = 10
MIN_V_ERR = (100 - V_ERR) / 100
MAX_V_ERR = (100 + V_ERR) / 100
RAIL_RANGES = {
    '0V85': {'voltage': (0.85 * MIN_V_ERR, 0.85 * MAX_V_ERR),
             'current': (0, 20)},
    '1V1_DC': {'voltage': (1.1 * MIN_V_ERR, 1.1 * MAX_V_ERR),
               'current': (0, 2)},
    '1V2_PL': {'voltage': (1.2 * MIN_V_ERR, 1.2 * MAX_V_ERR),
               'current': (-3, 3)},
    '1V2_PS': {'voltage': (1.2 * MIN_V_ERR, 1.2 * MAX_V_ERR),
               'current': (-3, 3)},
    '1V8': {'voltage': (1.8 * MIN_V_ERR, 1.8 * MAX_V_ERR),
            'current': (0, 6)},
    '2V5_DC': {'voltage': (2.5 * MIN_V_ERR, 2.5 * MAX_V_ERR),
               'current': (0, 2)},
    '3V3': {'voltage': (3.3 * MIN_V_ERR, 3.3 * MAX_V_ERR),
            'current': (0, 2)},
    '3V5_DC': {'voltage': (3.5 * MIN_V_ERR, 3.5 * MAX_V_ERR),
               'current': (0, 6)},
    '5V0_DC': {'voltage': (5 * MIN_V_ERR, 5 * MAX_V_ERR),
               'current': (0, 2)}
}
BITSTREAM_PATH = '/usr/local/lib/python3.6/dist-packages/' \
                 'pynq/overlays/base/base.bit'


class SelfTestOverlay(BaseOverlay):

    def __init__(self, bitfile_name=BITSTREAM_PATH, autoconfig=False,
                 **kwargs):
        super().__init__(bitfile_name, **kwargs)
        addrs = netifaces.ifaddresses('eth0')
        self.mac = addrs[netifaces.AF_LINK][0]['addr'].upper()
        self._dac_tile_228 = self._dac_block_0 = None
        self._dac_tile_229 = self._dac_block_4 = None
        self._adc_tile_224 = self._adc_block_0 = None
        self._adc_tile_226 = self._adc_block_4 = None
        self.transmit = None
        self.receive = None
        self.sweep = None
        self.leds = self.rgbleds = None
        self.pmbus_rails = None
        self.pmbus_sensors = None
        self.pmbus_recorder = None
        self.dct_results = None

        if autoconfig:
            self.configure()

    def configure(self):
        """The main call to configure all the components.

        This step can generate some exceptions for bad boards so we have to
        be careful. By default, this `configure()` will not be called.
        A formal test should follow the steps in this method.

        """
        self.init_i2c()
        self.config_pmbus()
        self.init_rf_clks()
        self.config_dac228()
        self.config_dac229()
        self.config_adc224()
        self.config_adc225()
        self.config_tx_rx()
        self.config_sweep()

    def config_dac228(self):
        """Configure DAC Tile 228 and DAC 0

        """
        self._dac_tile_228 = self.usp_rf_data_converter.dac_tiles[0]
        self._dac_block_0 = self._dac_tile_228.blocks[0]

        self._dac_tile_228.DynamicPLLConfig(1, 409.6, 4096)
        self._dac_block_0.NyquistZone = 1
        self._dac_block_0.MixerSettings = {
            'CoarseMixFreq': xrfdc.COARSE_MIX_BYPASS,
            'EventSource': xrfdc.EVNT_SRC_IMMEDIATE,
            'FineMixerScale': xrfdc.MIXER_SCALE_1P0,
            'Freq': -64,
            'MixerMode': xrfdc.MIXER_MODE_C2R,
            'MixerType': xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset': 0.0
        }
        self._dac_block_0.UpdateEvent(xrfdc.EVENT_MIXER)
        self._dac_tile_228.SetupFIFO(True)

    def config_dac229(self):
        """Configure DAC Tile 229 and DAC 4

        """
        self._dac_tile_229 = self.usp_rf_data_converter.dac_tiles[1]
        self._dac_block_4 = self._dac_tile_229.blocks[0]

        self._dac_tile_229.DynamicPLLConfig(1, 409.6, 4096)
        self._dac_block_4.NyquistZone = 1
        self._dac_block_4.MixerSettings = {
            'CoarseMixFreq': xrfdc.COARSE_MIX_BYPASS,
            'EventSource': xrfdc.EVNT_SRC_IMMEDIATE,
            'FineMixerScale': xrfdc.MIXER_SCALE_1P0,
            'Freq': -64,
            'MixerMode': xrfdc.MIXER_MODE_C2R,
            'MixerType': xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset': 0.0
        }
        self._dac_block_4.UpdateEvent(xrfdc.EVENT_MIXER)
        self._dac_tile_229.SetupFIFO(True)

    def config_adc224(self):
        """Configure ADC Tile 224 and ADC 0

        """
        self._adc_tile_224 = self.usp_rf_data_converter.adc_tiles[0]
        self._adc_block_0 = self._adc_tile_224.blocks[0]

        self._adc_tile_224.DynamicPLLConfig(1, 409.6, 4096)
        self._adc_block_0.NyquistZone = 1
        self._adc_block_0.MixerSettings = {
            'CoarseMixFreq': xrfdc.COARSE_MIX_BYPASS,
            'EventSource': xrfdc.EVNT_SRC_TILE,
            'FineMixerScale': xrfdc.MIXER_SCALE_1P0,
            'Freq': 2048,
            'MixerMode': xrfdc.MIXER_MODE_R2C,
            'MixerType': xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset': 0.0
        }
        self._adc_block_0.UpdateEvent(xrfdc.EVENT_MIXER)
        self._adc_tile_224.SetupFIFO(True)

    def config_adc225(self):
        """Configure ADC Tile 225 and ADC 4

        """
        self._adc_tile_226 = self.usp_rf_data_converter.adc_tiles[2]
        self._adc_block_4 = self._adc_tile_226.blocks[0]

        self._adc_tile_226.DynamicPLLConfig(1, 409.6, 4096)
        self._adc_block_4.NyquistZone = 1
        self._adc_block_4.MixerSettings = {
            'CoarseMixFreq': xrfdc.COARSE_MIX_BYPASS,
            'EventSource': xrfdc.EVNT_SRC_TILE,
            'FineMixerScale': xrfdc.MIXER_SCALE_1P0,
            'Freq': 2048,
            'MixerMode': xrfdc.MIXER_MODE_R2C,
            'MixerType': xrfdc.MIXER_TYPE_FINE,
            'PhaseOffset': 0.0
        }
        self._adc_block_4.UpdateEvent(xrfdc.EVENT_MIXER)
        self._adc_tile_226.SetupFIFO(True)

    def config_tx_rx(self):
        """Configure transmit object and receive object.

        This relies on previous components have been configured correctly.

        """
        # TODO: FIX
        self.transmit = self.radio.transmitter
        self.receive = self.radio.receiver

    def config_pmbus(self):
        """Configure pmbus related attributes.

        This includes the pmbus rails and sensors.

        """
        self.pmbus_rails = get_rails()
        sensors = []
        for rail in list(self.pmbus_rails.values()):
            sensors.append(rail.voltage)
            sensors.append(rail.current)
            sensors.append(rail.power)
        self.pmbus_sensors = sensors
        self.pmbus_recorder = DataRecorder(*sensors)

    def config_sweep(self):
        """Configure the spectrum sweep.

        Use a default setting.

        """
        freq = [100, 400, 900, 1400, 1900, 2200, 2600, 2800, 3200, 3500]
        self.sweep = SpectrumSweep(self.transmit, self.receive,
                                   frequencies=freq, visualise=False)

    def test_pll_clks(self):
        """Method to test the PLL clocks

        Reading from the GPIO. 1 indicates that the clock is locked and has
        been detected.

        Returns
        -------
        dict
            A dictionary storing a total number of 5 test results, each being
            a bool value, indicating pass or fail.

        """
        dc_clk_locks = {}
        clk_lock_reg = self.clk_locked_gpio.read()
        dc_clk_locks['ddr_lock'] = bool((clk_lock_reg >> 0) & 0x1)
        dc_clk_locks['adc_224_lock'] = bool((clk_lock_reg >> 1) & 0x1)
        dc_clk_locks['adc_226_lock'] = bool((clk_lock_reg >> 2) & 0x1)
        dc_clk_locks['dac_228_lock'] = bool((clk_lock_reg >> 3) & 0x1)
        dc_clk_locks['dac_229_lock'] = bool((clk_lock_reg >> 4) & 0x1)
        return dc_clk_locks

    def test_power_rail(self):
        """Check pmbus for non nominal values.

        SYZYGY power rail will not be tested since it is module dependent.

        Returns
        -------
        dict
            A dictionary storing the power rail test results, each being
            a bool value, indicating pass or fail.

        """
        pmbus_flags = {}
        for rail, rail_sensors in RAIL_RANGES.items():
            for sensor in rail_sensors:
                key = '{}_{}'.format(rail, sensor)
                pmbus_flags[key] = True
                for m in self.pmbus_recorder.frame[key]:
                    if not rail_sensors[sensor][0] <= m <= \
                           rail_sensors[sensor][1]:
                        pmbus_flags[key] = False
        return pmbus_flags

    def test_sweep(self):
        """Runs spectrum sweep whilst recording pmbus sensors.

        Returns
        -------
        dict
            A dictionary storing the power rail test results, each being
            a bool value, indicating pass or fail.

        """
        with self.pmbus_recorder.record(1):
            self.dct_results = self.sweep.run()

        dc_channel_flags = {}
        for ch_index, ch_flag in enumerate(self.sweep.passed):
            dc_channel_flags['dc_ch_{}'.format(ch_index)] = bool(ch_flag)
        return dc_channel_flags


start_time = time()
test_flags = {}

boot_log_dir = '/boot/BootLogs'
test_log_dir = '/boot/TestLogs'
if not os.path.exists(boot_log_dir):
    os.mkdir(boot_log_dir)
if not os.path.exists(test_log_dir):
    os.mkdir(test_log_dir)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

now = datetime.now()
time_str = now.strftime("%Y_%m_%d_%H_%M_%S")
testlog = os.path.join(test_log_dir, '{}_test.log'.format(time_str))
bootlog = os.path.join(boot_log_dir, '{}_boot.log'.format(time_str))
logger = logging.getLogger()
fhandler = logging.FileHandler(filename=testlog, mode='a')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
tty_path = '/dev/ttyPS0'
tty = os.open(tty_path, os.O_RDWR)


def logprint(message):
    logging.debug(message)
    if terminal_ok:
        os.write(tty, bytes(message + '\n', 'utf-8'))
    print(message)


"""Section 0: Log the boot message, download overlay

This section is supposed to be free of errors. If it does not boot properly,
there is no way to test.

The serial needs some time to be stable, give it 10 second timeout period.

"""
command = 'dmesg > {}'.format(bootlog)
os.system(command)
test_overlay = SelfTestOverlay()

timeout, terminal_ok = 10, True
msg = '==== Self-test started ===='
while timeout > 0:
    try:
        ret = os.write(tty, bytes(msg + '\n', 'utf-8'))
        if ret > 0:
            break
    except:
        pass
    timeout -= 1
    sleep(1)
if timeout == 0:
    terminal_ok = False

"""Section 1: Test the basic components.

This section includes the basic tests for MAC, LEDs, I2C, and PMBUS.

"""
mac = test_overlay.mac
mac_group = 'FC:C2:3D'
test_flags['mac_test'] = True
try:
    assert mac[0:8] == mac_group
except:
    test_flags['mac_test'] = False
logprint('MAC: {}'.format(test_flags['mac_test']))
logprint('MAC address: {}'.format(mac))


test_flags['config_leds'] = True
try:
    test_overlay.config_leds()
except:
    test_flags['config_leds'] = False
logprint('LED: {}'.format(test_flags['config_leds']))


test_flags['init_i2c'] = True
try:
    test_overlay.init_i2c()
except:
    test_flags['init_i2c'] = False
logprint('I2C: {}'.format(test_flags['init_i2c']))


test_flags['config_syzygy'] = True
try:
    test_overlay.set_syzygy_vio(1.2)
except:
    test_flags['config_syzygy'] = False
logprint('SYZYGY: {}'.format(test_flags['config_syzygy']))


test_flags['config_pmbus'] = True
try:
    test_overlay.config_pmbus()
except:
    test_flags['config_pmbus'] = False
logprint('Configure PMBUS: {}'.format(test_flags['config_pmbus']))


if test_flags['mac_test'] and test_flags['config_leds'] and \
        test_flags['init_i2c'] and test_flags['config_syzygy'] and \
        test_flags['config_pmbus']:
    test_overlay.leds[0].on()


"""Section 2: Test Clocks

In this section we will reconfiguret the RF clock chips, namely, LMK and LMX
chips.

"""
test_flags['set_ref_clks'] = True
try:
    test_overlay.init_rf_clks()
except:
    test_flags['set_ref_clks'] = False
logprint('Set RF clocks: {}'.format(test_flags['set_ref_clks']))


if test_flags['set_ref_clks']:
    test_overlay.leds[1].on()


"""Section 3: Test RF components.

We will configure the RF components, including ADC, DAC. After that, we 
sweep the frequency domain while checking power.

"""
test_flags['config_rf'] = True
try:
    test_overlay.config_dac228()
    test_overlay.config_dac229()
    test_overlay.config_adc224()
    test_overlay.config_adc225()
    test_overlay.config_tx_rx()
    test_overlay.config_sweep()
except:
    test_flags['config_rf'] = False
logprint('Configure ADC/DAC: {}'.format(test_flags['config_rf']))


test_flags['clk_test'] = True
try:
    clk_locks = test_overlay.test_pll_clks()
    test_flags.update(clk_locks)
    for clk, lock_state in clk_locks.items():
        logprint('{}: {}'.format(clk, lock_state))
        test_flags['clk_test'] = test_flags['clk_test'] and lock_state
except:
    test_flags['clk_test'] = False
logprint('Configure ADC/DAC: {}'.format(test_flags['config_rf']))


test_flags['pmbus_rails'] = True
try:
    rails = map(str, test_overlay.pmbus_rails.values())
    logprint('\n' + '\n'.join(rails))
except:
    test_flags['pmbus_rails'] = False
logprint('PMBUS rails: {}'.format(test_flags['pmbus_rails']))


test_flags['dc_test'] = True
try:
    dc_ch_flags = test_overlay.test_sweep()
except:
    test_flags['dc_test'] = False
else:
    test_flags.update(dc_ch_flags)
    for dc_ch in dc_ch_flags.values():
        test_flags['dc_test'] = test_flags['dc_test'] and dc_ch
logprint('DC tests: {}'.format(test_flags['dc_test']))


test_flags['pmbus_test'] = True
try:
    pmbus_ch_flags = test_overlay.test_power_rail()
except:
    test_flags['pmbus_test'] = False
else:
    test_flags.update(pmbus_ch_flags)
    for pmbus_ch in pmbus_ch_flags.values():
        test_flags['pmbus_test'] = test_flags['pmbus_test'] and pmbus_ch
logprint('PMBUS tests: {}'.format(test_flags['pmbus_test']))


if test_flags['pmbus_rails'] and test_flags['pmbus_test']:
    test_overlay.leds[2].on()


if test_flags['config_rf'] and test_flags['dc_test']:
    test_overlay.leds[3].on()


try:
    df_ch0 = pd.DataFrame(data=test_overlay.dct_results[0],
                          index=["TX Frequency (MHz)",
                                 "RX Fundamental (MHz)",
                                 "SFDR excl harm & dc. (dBm)"])
    logprint('ch0:\n' + str(df_ch0.round(2)))
except:
    logprint('ch0 data not available.')

try:
    df_ch1 = pd.DataFrame(data=test_overlay.dct_results[1],
                          index=["TX Frequency (MHz)",
                                 "RX Fundamental (MHz)",
                                 "SFDR excl harm & dc. (dBm)"])
    logprint('ch1:\n' + str(df_ch1.round(2)))
except:
    logprint('ch1 data not available.')

try:
    dump = str(test_overlay.pmbus_recorder.frame)
    logprint('pmbus dump:\n' + dump)
except:
    logprint('PMBUS recorder data not available.')


""" Final check if all tests passed.

Light on green LEDs if all tests have passed. Otherwise light red.

"""
self_test_passed = True
for flag, flag_val in test_flags.items():
    logprint('{}: {}'.format(flag, flag_val))
    self_test_passed = self_test_passed and flag_val

if self_test_passed:
    test_overlay.rgbleds[0].on(2)
    test_overlay.rgbleds[1].on(2)
    logprint('Test PASS.')
else:
    test_overlay.rgbleds[0].on(4)
    test_overlay.rgbleds[1].on(4)
    logprint('Test FAIL.')

end_time = time()
logprint('Test took {0:.2f}s'.format(end_time - start_time))
logprint('Test logged to: {}'.format(testlog))
logprint('==== Self-test finished ====')
os.close(tty)
