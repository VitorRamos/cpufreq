#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Module to run standalone cpufreq commands

"""

from cpufreq import cpuFreq,CPUFreqErrorInit

def test1():
    c = cpuFreq()
    g = c.get_governors()
    print(g)

def test2():
    c = cpuFreq()
    f = c.get_max_freq()
    print(f)

def main():
    """
    Main function executed from console run.
    """
    try:
        c = cpuFreq()
        print("Informations about the System:")
        print("Driver: {0}".format(c.get_driver()))
        print("Available Governors: {0}".format(', '.join(c.get_available_governors())))
        print("Available Frequencies: {0}".format(', '.join(c.get_available_frequencies())))
        print("Status of CPUs:")
        govs = c.get_governors()
        freqs = c.get_frequencies()
        print("{:4} - {:>12} - {:>8}".format("CPU","Governor","Frequencie"))
        for c in govs["cpu"].keys():
            print("{:4d} - {:>12} - {:>8}".format(c,govs["cpu"][c],freqs["cpu"][c]))
    except CPUFreqErrorInit as err:
        print("{0}".format(err))


if __name__ == '__main__':
    main()