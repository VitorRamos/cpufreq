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
    print("main")

if __name__ == '__main__':
    main()