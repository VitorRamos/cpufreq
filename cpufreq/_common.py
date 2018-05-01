# -*- coding: utf-8 -*-
"""
    Basic Enviroments Constants

"""

import sys
from os import path

# If Python version is 3
PY3 = sys.version_info[0] == 3

# If O.S. is Linux
LINUX = sys.platform.startswith("linux")

BASEDIR = "/sys/devices/system/cpu"
GOVERNORINFOFILE = "scaling_available_governors"
FREQINFOFILE = "scaling_available_frequencies"
FREQDIR = "cpufreq"
FREQCURINFO = "cpuinfo_cur_freq"
FREQSET = "scaling_setspeed"
GOVERNORSET = "scaling_governor"

DRIVERFREQ = path.isfile(path.join(BASEDIR,
                                   "cpu0",
                                   FREQDIR,
                                   GOVERNORINFOFILE)) \
             and path.isfile(path.join(BASEDIR,
                                       "cpu0",
                                       FREQDIR,
                                       FREQINFOFILE))
