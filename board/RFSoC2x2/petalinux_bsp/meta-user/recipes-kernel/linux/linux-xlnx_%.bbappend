SRC_URI += " file://bsp.cfg"
SRC_URI += " file://i2c.cfg"
SRC_URI += " file://pl_mem.cfg"

FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

