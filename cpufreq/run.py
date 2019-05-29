#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Module to run standalone cpufreq commands

"""

import argparse
from cpufreq import cpuFreq,CPUFreqErrorInit


def argsparselist(txt):
    """
    Validate a list of txt argument.

    :param txt: argument with comma separated int strings.
    :return: list of strings.
    """

    txt = txt.split(',')
    listarg = [i.strip() for i in txt]
    return listarg

def argsparseintlist(txt):
    """
    Validate a list of int arguments.

    :param txt: argument with comma separated numbers.
    :return: list of integer converted numbers.
    """

    txt = txt.split(',')
    listarg = [int(i) for i in txt]
    return listarg

def argsparsevalidation():
    """
    Validation of script arguments passed via console.

    :return: argparse object with validated arguments.
    """

    parser = argparse.ArgumentParser(description='Script to get and set '
                                                 'frequencies configurations'
                                                 'of cpus by command line')
    subparsers = parser.add_subparsers(help="Available commands")

    parse_info = subparsers.add_parser('info', 
                                       help='print status of governors and frequencies', 
                                       default=1)

    parse_reset = subparsers.add_parser('reset', 
                                        help='reset the governors and max and min frequencies', 
                                        default=1)

    # parser.add_argument('c', type=argsparseintlist,
    #                     help='List of cores numbers to be '
    #                          'used. Ex: 1,2,4')
    # parser.add_argument('-p', '--package', help='Package Name to run',
    #                     required=True)
    # parser.add_argument('-c', '--compiler',
    #                     help='Compiler name to be used on run. '
    #                          '(Default: %(default)s).',
    #                     choices=compilerchoicebuilds, default='gcc-hooks')
    # parser.add_argument('-f', '--frequency', type=argsparseintlist,
    #                     help='List of frequencies (KHz). Ex: 2000000,2100000')
    # parser.add_argument('-i', '--input', type=argsparseinputlist,
    #                     help=helpinputtxt, default='native')
    # parser.add_argument('-r', '--repetitions', type=int,
    #                     help='Number of repetitions for a specific run. '
    #                          '(Default: %(default)s)', default=1)
    # parser.add_argument('-b', '--cpubase', type=int,
    #                     help='If run with thread affinity(limiting the '
    #                          'running cores to defined number of cores), '
    #                          'define the cpu base number.')
    parser.add_argument('info', 
                        help='print status of governors and frequencies', default=1)
    args = parser.parse_args()
    return args

def reset():
    try:
        c = cpuFreq()
        c.reset()
        print("Governors, maximum and minimum frequencies reset successfully.")
    except CPUFreqErrorInit as err:
        print("{0}".format(err))    
    
def info():
    try:
        c = cpuFreq()
        print("Informations about the System:")
        print("Driver: {0}".format(c.get_driver()))
        print("Available Governors: {0}".format(', '.join(c.get_available_governors())))
        print("Available Frequencies: {0}".format(', '.join(c.get_available_frequencies())))
        print("Status of CPUs:")
        govs = c.get_governors()
        freqs = c.get_frequencies()
        minfreq = c.get_min_freq()
        maxfreq = c.get_max_freq()
        print("{:^4} - {:^12} - {:^8} - {:^8} - {:^8}".format("CPU","Governor","Frequencie", "Min Freq.", "Max Freq."))
        for c in govs["cpu"].keys():
            print("{:4d} - {:>12} - {:>8} - {:>8} - {:>8}".format(c,govs["cpu"][c],freqs["cpu"][c],minfreq["cpu"][c],maxfreq["cpu"][c]))
    except CPUFreqErrorInit as err:
        print("{0}".format(err))    

def main():
    """
    Main function executed from console run.
    """
    args = argsparsevalidation()
    
    print(args)
    if args.info:
        info()
    elif args.reset:
        reset()



if __name__ == '__main__':
    main()