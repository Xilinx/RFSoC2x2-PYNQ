SRC_URI_append = " file://platform-top.h"
SRC_URI += "file://bsp.cfg \
            file://ethernet.cfg \
	    file://0001-read-from-at24mac402-extended-memory.patch \
            "

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
