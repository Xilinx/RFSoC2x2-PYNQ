#! /bin/bash
# Copyright (C) 2021 Xilinx, Inc
# SPDX-License-Identifier: BSD-3-Clause

set -x
set -e

. /etc/environment
export HOME=/root
export BOARD=${PYNQ_BOARD}

apt remove -y python3-terminado
apt remove -y python3-zmq

pip3 install terminado==0.8.1 pyzmq==17 notebook==5.2.2 \
	nbconvert==5.5.0 jupyter-client==5.3.1 ipykernel==4.8.2 nbsphinx==0.3.1

pip3 install voila==0.1.13
