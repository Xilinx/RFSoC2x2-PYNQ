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


__author__ = "David Northcote"
__copyright__ = "Copyright 2021, Xilinx"
__email__ = "pynq_support@xilinx.com"


from pynq import DefaultIP


class PacketGenerator(DefaultIP):
    """Driver for the Packet Generator core.
    
    The Packet Generator is a simple IP core written in
    VHDL. The core is used to generate AXI-Stream packets
    for interfacing to an AXI DMA. The AXI-Stream packets
    are written to the master AXI-Stream interface when
    requested by the user through the transfer register.
    
    Attributes
    ----------
    packetsize : an int
        The packetsize defines the number of valid samples
        between the start of an AXI-Stream packet and a valid
        tlast strobe. The acceptable range is an int between
        2 and 4096.
        
    transfer : a bool
        The transfer property allows the user to communicate
        with the packet generator, such that an AXI-Stream
        packet of size packetsize, is transferred to the
        master AXI-Stream interface on the rising edge.
    
    """
    
    def __init__(self, description):
        super().__init__(description=description)
        
    bindto = ['xilinx.com:ip:packet_generator:1.0']

    @property
    def packetsize(self):
        """The number of valid samples between the start
        of an AXI-Stream packet and a valid tlast strobe."""
        return self.read(0x00)
    
    @packetsize.setter
    def packetsize(self, packetsize):
        if 2 <= packetsize <= 4096:
            self.write(0x00, packetsize)
        else:
            raise ValueError(
                'Packet size incorrect, should be in range 2 to 4096.')

    @property
    def transfer(self):
        """On the rising edge, transfer an AXI-Stream packet
        to the master AXI-Stream interface."""
        return self.read(0x04)
    
    @transfer.setter
    def transfer(self, transfer):
        if transfer:
            self.write(0x4, int(1))
        else:
            self.write(0x4, int(0))
