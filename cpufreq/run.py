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

def argsparsevalidation(avail_govs):
    """
    Validation of script arguments passed via console.

    :return: argparse object with validated arguments.
    """

    parser = argparse.ArgumentParser(description='Script to get and set '
                                                 'frequencies configurations'
                                                 'of cpus by command line')
    p_group = parser.add_mutually_exclusive_group()
    p_group.add_argument('--info', action='store_true',
                                   help='Print status of governors and frequencies')
    p_group.add_argument('--reset', action='store_true',
                                    help='Reset the governors and max and min frequencies')
    subparsers = parser.add_subparsers(help="Available commands")

    parse_setgovernor = subparsers.add_parser('setgovernor', help='Set the governor for all online cpus or '
                                        'with optional specific cpus. Ex: cpufreq setgovernor "ondemand"')
    parse_setgovernor.add_argument('governor', help='Choice the governor name to set'
                                               choices=avail_govs)
    p_setgovernor_group = parse_setgovernor.add_mutually_exclusive_group()
    p_setgovernor_group.add_argument('--all', action='store_true',
                                              help='Set the governor for all online cpus.')
    p_setgovernor_group.add_argument('--cpus', type=argsparseintlist,
                                               help='List of CPUs numbers (first=0) to set gorvernor '
                                                    'Ex: 0,1,3,5')

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
    args = parser.parse_args()
    return args

def set_governors(c,governor, cpus=None):
    try:
        c = cpuFreq()
        c.set_governors(gov=governor, rg=cpus)
        print("Governors set successfully.")
    except CPUFreqErrorInit as err:
        print("{0}".format(err))    
    
def info(c):
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

def main():
    """
    Main function executed from console run.
    """    
    try:
        c = cpuFreq()
    except CPUFreqErrorInit as err:
        print("{0}".format(err))    
        exit()

    avail_govs = c.get_available_governors()

    args = argsparsevalidation(avail_govs)

    if args.info is True:
        info(c)
    elif args.reset is True:
        c.reset()
        print("Governors, maximum and minimum frequencies reset successfully.")
    elif args.setgovernors:
        print("cpu list: ", args.cpus)
        avail_cpus = c.get_online_cpus() 
        avail_governors = c.get_available_governors()
        if not set(args.cpus).issubset(set(avail_cpus)):
            print("ERROR: cpu list has number(s) that not in permissible set list.")
            exit(1)
        elif args.setgovernor not in avail_governors:
            print("ERROR: governor name not not in permissible governors list.")
            exit(1)
        c.set_governors(gov=args.setgovernor,rg=args.cpus)
        print("Governor set successfully.")


if __name__ == '__main__':
    main()