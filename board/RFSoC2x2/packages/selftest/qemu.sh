#! /bin/bash
# Copyright (C) 2021 Xilinx, Inc
# SPDX-License-Identifier: BSD-3-Clause

set -x
set -e

. /etc/environment
export HOME=/root
export BOARD=${PYNQ_BOARD}

# replace boot.py; will overwrite the existing boot.py
cp -rf boards/RFSoC2x2/rfsoc_self_test/bootpy/boot.py /boot/boot.py

