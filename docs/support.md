# RFSoC 2x2 support

## PYNQ support

Questions about using PYNQ on the RFSoC 2x2 can be posted to the PYNQ support forum:

* [PYNQ Support Forum](https://discuss.pynq.io/)

You can also check for other RFSoC 2x2 projects, and post your own in the [Community Corner](https://discuss.pynq.io/c/community-projects-chat/14). 



## Xilinx support

Questions related to Xilinx tools and building designs for your board, including HLS design, can be posted on the Xilinx technical support forums:

* [Xilixn Support Forum](https://forums.xilinx.com)



## Hardware problems

Follow the troubleshooting guide below, and post questions on the [PYNQ support forum](https://discuss.pynq.io/). 



## Troubleshooting

Check the [PYNQ Documentation](http://pynq.readthedocs.io/) for FAQs related to PYNQ. 



## RFSoC 2x2 FAQ

* **I do not see any LEDs turn on after trying to power-on the board**

  This indicates there is no power going to the board, or the board is dead.

  * Check the power supply is connected correctly

  * Check the power switch is in the correct position

* **The PS-STATUS LED is RED**

  This indicates the PS is not booting the PYNQ image

  * Check the SD card is inserted, and has a valid PYNQ image
  * Check that jumper JP1/JTAG is configured to boot from SD Card

* **I do not see the DONE LED or the white flashing LEDS**

  This indicates the PS has not booted properly. 

  * Check the SD card has a valid PYNQ image

  * Connect a serial terminal and check the console for the boot log

    If the boot process stalls, or continuously restarts, try to capture the console information and post it to the [PYNQ support forum](https://discuss.pynq.io/). 

* **I have no Ethernet connection/I do not see the new connection on my computer**

  * On your host computer, check a new Ethernet device is available in your network connections. You may need to check hardware manager in Windows, and the equivalent in other operating systems, to see if the Ethernet device was recognized, and if the driver was automatically loaded.  
  * Check the Micro USB 3.0 cable is connected to your host PC and board
  * If you are using a Mac, RNDIS support may need to be installed for USB "Ethernet gadget" to work correctly. One way to install this is via [HORNDIS](https://www.joshuawise.com/horndis). This has been tested by the PYNQ team with macOS Catalina. This cannot be installed on Big Sur without disabling the Mac protection scheme. 

* **My board seems to have booted correctly (I see the correct LED sequence), but I cannot connect to Jupyter**

  * I get a "404" or the Jupyter log-in webpage or it does not load at all

  * Connect a serial terminal, and check the boot log. Check if Jupyter Notebook server has started, and that it is still running. 

    You can do this by checking if the following command returns something:

    `ps -ef | grep Jupyter` 

    e.g. 

    ```
    root    1434  1405  0 09:16 pts/0   00:00:00
    ```

  
