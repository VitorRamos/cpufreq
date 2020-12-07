# cpufreq

[![Build Status](https://travis-ci.com/VitorRamos/cpufreq.svg?branch=master)](https://travis-ci.com/VitorRamos/cpufreq)

Python module to control the frequency on Linux systems.

## Features

 - Get current Frenquency and governor by CPU.
 - Set frequency by CPU.
 - Enable and Disable CPUs.

## Prerequisites

 - Custom CPU power managment enabled on BIOS
 - Power Management Driver installed (acpi for example)
 - Python3.5 or newer

## Site

 - <https://github.com/VitorRamos/cpufreq>

## Installation

 $ pip3 install cpufreq

## Usage

 ### In a command line:

```
  # Listing the governors and frequencies of cpus
     cpufreq --info
  # Setting a governor for specifics CPU
     cpufreq setgovernor powersave --cpus 0,1,2
  # Resetting cpus and frequencies status
     cpufreq --reset
  # Help 
     cpufreq --help
```

 #### In a python script:
 Use the example file script: example.py

