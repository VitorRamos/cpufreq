# -*- coding: utf-8 -*-
"""
    Module with CPUFreq class that manage the CPU frequency.


"""

from os import listdir
from os import path
import re
from ._common import LINUX
from ._common import BASEDIR
from ._common import GOVERNORINFOFILE
from ._common import FREQINFOFILE
from ._common import FREQDIR
from ._common import FREQCURINFO
from ._common import FREQSET
from ._common import GOVERNORSET
from ._common import DRIVERFREQ


class CPUFreqBaseError(Exception):
    """Base Exception raised for errors in the Class CPUFreq."""
    pass


class CPUFreqErrorInit(CPUFreqBaseError):
    """Exception raised for errors at initializing of CPUFreq Class.

    Attributes:
        expression - input expression in which the error occurred
        message - explanation of the error
    """

    def __init__(self, message):
        self.message = message


class CPUFreq:
    """
    Class that manage cpus frequencies

        Atrributes
            basedir - Base directory to get/set cpus setups
            governos - List of available governos
            frequencies - List of available frequencies

        Methods
            get_governos()
            get_frequencies()
            readFromCPUFiles()
            writeOnCPUFiles()
            get_current_frequencie()
            list_governos()
            list_frequencies()
            lists_current_governos()
            list_current_frequencies()
            change_governo()
            change_frequency()
            change_max_frequency()
            disable_cpu()
            enable_cpu()

    """

    def __new__(cls, *args, **kwargs):
        if not LINUX:
            raise(CPUFreqErrorInit("ERROR: %s Class should be used only on "
                                   "Linux Systems." % cls.__name__))
            return None
        elif not DRIVERFREQ:
            raise(CPUFreqErrorInit("ERROR: %s Class should be used only with "
                                   "OS CPU Power driver activated (Linux ACPI "
                                   "module, for example)." % cls.__name__))
            return None
        else:
            return super(CPUFreq, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        """
        Initialize the class attributes.

        """

        self.basedir = BASEDIR
        self.freqdir = FREQDIR
        self.freqcurfile = FREQCURINFO
        self.freqsetfile = FREQSET
        self.governorsetfile = GOVERNORSET
        self.governos = self.read_from_cpufiles(GOVERNORINFOFILE)
        self.frequencies = self.read_from_cpufiles(FREQINFOFILE)

    def get_governos(self):
        """
        Get the governos list.

        :return List of available governos
        """

        return self.governos

    def get_frequencies(self):
        """
        Get the frequencies list.

        :return List of available frequencies
        """

        return self.frequencies

    def read_from_cpufiles(self, filename):
        """
        Read the available governos from system cpu info file.

        :param filename: File name to read from
        :return List of dictionary with available cpus info
        """

        cpu = {'cpu': 0, 'data': 0}
        cpus = []
        for ldir in listdir(self.basedir):
            if re.match('cpu[0-9]', ldir):
                fp = path.join(self.basedir, ldir, self.freqdir, filename)
                try:
                    with open(fp) as f:
                        data = [i for i in f.read().split()]
                    cpu['cpu'] = int(ldir.strip('cpu'))
                    cpu['data'] = data
                    cpus.append(cpu.copy())
                except IOError:
                    print("Error: File %s does not appear to exist "
                          "or permission error." % fp)
        return cpus

    def write_on_cpufiles(self, filename, data):
        """
        Write a data in a governo cpu file.

        :param filename: File name to read from
        :param data: data to write in filename file
        """

        for ldir in listdir(self.basedir):
            if re.match('cpu[0-9]', ldir):
                fp = path.join(self.basedir, ldir, self.freqdir, filename)
                try:
                    with open(fp, "w") as f:
                        f.write(data)
                except IOError:
                    print("Error: File %s does not appear to exist "
                          "or permission error." % fp)

    def get_current_frequencies(self, cpu=-1):
        """
        Read the current frequency from system cpu info file.

        :param cpu: Specifc CPU to get frequency info
        :return List of dictionary with available cpus info
        """

        if cpu == -1:
            return self.read_from_cpufiles(self.freqcurfile)
        else:
            fp = path.join(self.basedir, "cpu%d" % cpu,
                           self.freqdir, self.freqcurfile)
            with open(fp, "r") as f:
                frs = f.read()
            return frs

    def list_governos(self):
        """
        Print the governos list.

        :return
        """

        for cpu in self.governos:
            print(cpu['cpu'], cpu['data'])

    def list_frequencies(self):
        """
        Print the frequencies list.

        :return
        """

        for cpu in self.frequencies:
            print(cpu['cpu'], cpu['data'])

    def list_current_governos(self):
        """
        Print the current governor.

        :return
        """

        for cpu in self.read_from_cpufiles(self.governorsetfile):
            print(cpu['cpu'], cpu['data'])

    def list_current_frequencies(self):
        """
        Print the current frequency.

        :return
        """

        for cpu in self.read_from_cpufiles(self.freqcurfile):
            print(cpu['cpu'], cpu['data'])

    def change_governo(self, name, cpu=-1):
        """
        Change the actual governor.

        :param name: name of governor to set
        :param cpu: Specifc CPU to set the governor info
        :return
        """

        if name not in self.governos[0]['data']:
            return
        if cpu == -1:
            self.write_on_cpufiles(self.governorsetfile, name)
        else:
            fp = path.join(self.basedir, "cpu%d" % cpu,
                           self.freqdir, self.governorsetfile)
            try:
                with open(fp, "w") as f:
                    f.write(name)
            except IOError:
                print("Error: File %s does not appear to exist "
                      "or permission error." % fp)

    def change_frequency(self, freq, cpu=-1):
        """
        Change the actual frequency.

        :param freq: frequency value to set
        :param cpu: Specifc CPU to set the frequency info
        :return
        """

        if freq not in self.frequencies[0]['data']:
            return
        self.change_max_frequency(freq, cpu=cpu)
        if cpu == -1:
            self.write_on_cpufiles(self.freqsetfile, freq)
        else:
            fp = path.join(self.basedir, "cpu%d" % cpu,
                           self.freqdir, self.freqsetfile)
            try:
                with open(fp, "w") as f:
                    f.write(freq)
            except IOError:
                print("Error: File %s does not appear to exist "
                      "or permission error." % fp)

    def change_max_frequency(self, freq, cpu=-1):
        """
        Set the max frequency.

        :param freq: frequency value to set
        :param cpu: Specifc CPU to set the frequency info
        :return
        """

        if cpu == -1:
            self.write_on_cpufiles('scaling_max_freq', freq)
        else:
            fp = path.join(self.basedir, "cpu%d" % cpu,
                           self.freqdir, "scaling_max_freq")
            try:
                with open(fp, "w") as f:
                    f.write(freq)
            except IOError:
                print("Error: File %s does not appear to exist "
                      "or permission error." % fp)

    def disable_cpu(self, cpu):
        """
        Turn the CPU on.

        :param cpu: Specifc CPU to turn on
        :return
        """

        fp = path.join(self.basedir, "cpu%d" % cpu, "online")
        try:
            with open(fp, "r+") as f:
                if '1' in f.read():
                    f.write("0")
        except IOError:
            print("Error: File %s does not appear to exist "
                  "or permission error." % fp)

    def enable_cpu(self, cpu):
        """
        Turn the CPU off.

        :param cpu: Specifc CPU to turn off
        :return
        """

        fp = path.join(self.basedir, "cpu%d" % cpu, "online")
        try:
            with open(fp, "r+") as f:
                if '0' in f.read():
                    f.write("1")
        except IOError:
            print("Error: File %s does not appear to exist "
                  "or permission error." % fp)
