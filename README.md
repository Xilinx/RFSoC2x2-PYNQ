# RFSoC 2x2 Kit

View the *RFSoC 2x2 Kit GitHub page* for this repository on [www.rfsoc-pynq.io](http://www.rfsoc-pynq.io/).

This repository is used to host the *GitHub Documentation Page* for the
RFSoC2x2 kit. It includes the sources for the documentation, and board
collateral including source code and build scripts for the RFSoC 2x2 *base*
design. The design files in this repository are compatible with Xilinx
Vivado 2020.1, and PYNQ v2.6.0 and later.

Users can find the Vivado board files on
[Xilinx Vivado board repository](https://github.com/Xilinx/XilinxBoardStore/tree/2020.1/boards/Xilinx/rfsoc2x2/1.1).

![alt](./docs/images/01_rfsoc_2x2_t.png)

## Steps to rebuild the PYNQ SD card image for the RFSoC 2x2 (Linux)

1. First choose a location to clone this repository:

	```bash
	export RFSoC2x2_REPO = <local_path>
	```

2. Do the following to clone this repository:

	```bash
	git clone https://github.com/Xilinx/RFSoC2x2-PYNQ.git $RFSoC2x2_REPO
	```

3. Download the overlay files, which allows users to skip the bitstream
   building time. 
   
	```bash
	pushd $RFSoC2x2_REPO/board/RFSoC2x2/base
	wget -O base.bit "https://www.xilinx.com/bin/public/openDownload?filename=pynq.base.rfsoc2x2.2.6.1.bit"
	wget -O base.hwh "https://www.xilinx.com/bin/public/openDownload?filename=pynq.base.rfsoc2x2.2.6.1.hwh"
	popd
	```

4. Go to PYNQ sdbuild folder and build the image with correct board folder 
   path:

	```bash
	make BOARDDIR=$RFSoC2x2_REPO
	```

## Steps to rebuild the RFSoC 2x2 base overlay design (Linux)

Go to the base overlay folder and run make:

```bash
cd $RFSoC2x2_REPO/board/RFSoC2x2/base
make
```

## Third-party license and source code

License and Copyrights Info [TAR/GZIP](https://www.xilinx.com/bin/public/openDownload?filename=rfsoc2x2-pynq-v1.0-license.tar.gz)

Open Components Source Code [TAR/GZIP](https://www.xilinx.com/bin/public/openDownload?filename=rfsoc2x2-pynq-v1.0-open_components.tar.gz)


Copyright (C) 2021 Xilinx, Inc

SPDX-License-Identifier: BSD-3-Clause
