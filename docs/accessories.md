# Accessories

The RFSoC comes with a Micro SD card, a Micro USB 3.0 cable, a power supply and two SMA cables. Other optional accessories can be used with the RFSoC 2x2 including RF antennas, filters and amplifiers as described below. 



## Recommended RF accessories

### Antenna

Recommendations:



### Filters



### Amplifiers





## Included accessories

### SD Card

If you need to make a new PYNQ image, the recommended Micro SD card size for PYNQ is 8GB. We recommend you use a 16GB or greater *branded/high quality* SD card. A larger capacity card will allow you to install more packages and overlays and save more data to the card. 

A branded card, or a higher quality card is likely to be more reliable and higher speed cards will be faster to burn, and may give some (modest) performance increase when using your board. 

### Power supply

**Check details**

If you need a replacement power supply, see:

### Micro USB 3.0 Cable

A composite USB 3.0 cable is used as a USB "Ethernet gadget" between your computer and the board. You can replace this cable with any compatible Micro USB composite cable. The Micro USB 3.0 port is backward compatible with USB 2.0 cables. You can use a Micro USB (2.0) cable and connect it to the left side of the USB composite port on the board. 

USB 3.0 is faster than 2.0, but for Ethernet Gadget with the RFSoC 2x2, the performance difference may not be significant. 

### SMA cables

2 x 30 cm SMA cables are included with the board and are mainly intended for loopback testing. You can use other SMA cables if required.  

## Optional Accessories

#### Micro USB (2.0) cable

The RFSoC 2x2 also has a Micro USB UART/JTAG port. A standard Micro USB (2.0) cable is optional and can be connected to this port. You can use this if you need to access a serial terminal on the UART. You can also use JTAG on this cable/port to connect to the board from Vivado to download a bitstream, or for JTAG debug. 

### Ethernet cable

USB Ethernet gadget is the recommended way to connect to the board and use PYNQ. If you do not want to use this, or you have an issue using Ethernet Gadget, you can use an Ethernet cable to connect your computer to your board instead. You can also use an Ethernet cable to connect your board to a network. Any standard Ethernet cable can be used. 

If you connect the board to your network where a DHCP server manages IP addresses, the board can be automatically allocated an IP address. If you want to connect your board directly to your computer, you will need to configure the Ethernet connection on your computer. 

This needs to be done for other boards that use PYNQ via an Ethernet cable. You can follow the same [PYNQ documentation for configuring an Ethernet connection for the ZCU104](https://pynq.readthedocs.io/en/latest/getting_started/zcu104_setup.html#ethernet).

### DisplayPort

The RFSoC 2x2 has a Mini DisplayPort. A Mini DisplayPort cable (to DisplayPort, or to Mini DisplayPort) can be used to connect a compatible display. The Zynq Ultrascale+ RFSoC DisplayPort controller supports DisplayPort 1.2a. Please check that you have a compatible monitor. A short list of [tested Zynq Ultrascale+ DisplayPort monitors](https://www.xilinx.com/support/answers/68671.html) is available.

#### Display port to HDMI adapter

If you do not have a DisplayPort monitor, you may be able to use a Mini DisplayPort to HDMI adapter. Adapters tend to come in two types - active and passive. Passive adapters are generally not compatible, and it is not guaranteed that all DisplayPort to HDMI adapters will work with the Zynq Ultrascale+ DisplayPort controller. 

For more information and recommended adapters, see this discussion on [supported Zynq Ultrascale+ DisplayPort to HDMI adapters on the Element 14 community forum](https://www.element14.com/community/thread/72867/l/ultra96-v2-mini-dp-to-hdmi-adapter).

### USB devices

You can add standard USB peripherals to your board. E.g. USB webcam, keyboard, mouse, USB WiFi dongles.  

Be aware any USB WiFi or USB Bluetooth devices you connect may interfere with any RF signals you are trying to capture.