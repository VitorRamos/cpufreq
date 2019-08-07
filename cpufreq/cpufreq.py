# -*- coding: utf-8 -*-
"""
    Module with CPUFreq class that manage the CPU frequency.
"""
from os import path
import sys


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


class cpuFreq:
    """
    Class that manage cpus frequencies
        Attributes
            driver
            available_governors
            available_frequencies
        Methods
            enable_all_cpu()
            reset()
            disable_hyperthread()
            disable_cpu()
            enable_cpu()
            set_frequencies()
            set_min_frequencies()
            set_max_frequencies()
            set_governors()
            get_online_cpus()
            get_governors()
            get_frequencies()
    """

    BASEDIR = "/sys/devices/system/cpu"
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cpuFreq.__instance == None:
            LINUX = sys.platform.startswith("linux")
            DRIVERFREQ = path.isfile(path.join(cpuFreq.BASEDIR,
                                            "cpu0",
                                            "cpufreq",
                                            "scaling_driver"))
            if not LINUX:
                raise(CPUFreqErrorInit("ERROR: %s Class should be used only on " \
                "Linux Systems." % cls.__name__))
            elif not DRIVERFREQ:
                raise(CPUFreqErrorInit("ERROR: %s Class should be used only with " \
                "OS CPU Power driver activated (Linux ACPI " \
                "module, for example)." % cls.__name__))
            else:
                cpuFreq.__instance= super().__new__(cls)
                fpath = path.join("cpu0","cpufreq","scaling_driver")
                datad = cpuFreq.__instance.__read_cpu_file(fpath).rstrip("\n").split()[0]

                fpath = path.join("cpu0","cpufreq","scaling_available_governors")
                datag = cpuFreq.__instance.__read_cpu_file(fpath).rstrip("\n").split()

                fpath = path.join("cpu0","cpufreq","scaling_available_frequencies")
                dataf = cpuFreq.__instance.__read_cpu_file(fpath).rstrip("\n").split()
                
                cpuFreq.__instance.driver = datad
                cpuFreq.__instance.available_governors = datag
                cpuFreq.__instance.available_frequencies = [int(f) for f in dataf]

        return cpuFreq.__instance

    # private
    def __read_cpu_file(self, fname):
        fpath = path.join(cpuFreq.BASEDIR, fname)
        with open(fpath, "rb") as f:
            data = f.read().decode("utf-8")
        return data

    def __write_cpu_file(self, fname, data):
        fpath = path.join(cpuFreq.BASEDIR,fname)
        with open(fpath, "wb") as f:
            f.write(data)

    def __get_cpu_variable(self, var):
        data = {}
        for cpu in self.__get_ranges("online"):
            fpath = path.join("cpu%i"%cpu,"cpufreq",var)
            data[int(cpu)] = self.__read_cpu_file(fpath).rstrip("\n").split()[0]
        return data

    def __get_ranges(self, fname):
        str_range = self.__read_cpu_file(fname).strip("\n").strip()
        l = []
        if not str_range:
            return l
        for r in str_range.split(","):
            mr = r.split("-")
            if len(mr) == 2:
                l += list(range(int(mr[0]),  int(mr[1])+1))
            else:
                l += [int(mr[0])]
        return l

    # interfaces
    def enable_all_cpu(self):
        """
        Enable all offline cpus
        """
        for cpu in self.__get_ranges("offline"):
            fpath = path.join("cpu%i"%cpu,"online")
            self.__write_cpu_file(fpath, b"1")

    def reset(self, rg=None):
        """
        Enable all offline cpus, and reset max and min frequencies files

        rg: range or list of threads to reset
        """
        if type(rg) == int:
            rg= [rg]
        to_reset= rg if rg else self.__get_ranges("present")
        self.enable_cpu(to_reset)
        for cpu in to_reset:
            self.set_governors("ondemand", rg=cpu)
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_max_freq")
            self.__write_cpu_file(fpath, str(max(self.available_frequencies)).encode())
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_min_freq")
            self.__write_cpu_file(fpath, str(min(self.available_frequencies)).encode())

    def disable_hyperthread(self):
        """
        Disable all threads attached to the same core
        """
        to_disable = []
        online_cpus = self.__get_ranges("online")
        for cpu in online_cpus:
            fpath = path.join("cpu%i"%cpu,"topology","thread_siblings_list")
            to_disable += self.__get_ranges(fpath)[1:]
        to_disable = set(to_disable) & set(online_cpus)

        for cpu in to_disable:
            fpath = path.join("cpu%i"%cpu,"online")
            self.__write_cpu_file(fpath, b"0")

    def disable_cpu(self, rg):
        """
        Disable cpus

        rg: range or list of threads to disable
        """
        if type(rg) == int:
            rg= [rg]
        to_disable= set(rg) & set(self.__get_ranges("online"))
        for cpu in to_disable:
            fpath = path.join("cpu%i"%cpu,"online")
            self.__write_cpu_file(fpath, b"0")

    def enable_cpu(self, rg):
        """
        Enable cpus

        rg: range or list of threads to enable
        """
        if type(rg) == int:
            rg= [rg]
        to_disable= set(rg) & set(self.__get_ranges("offline"))
        for cpu in to_disable:
            fpath = path.join("cpu%i"%cpu,"online")
            self.__write_cpu_file(fpath, b"1")

    def set_frequencies(self, freq, rg=None):
        """
        Set cores frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """

        if not type(freq) is int:
            raise(CPUFreqErrorInit("ERROR: Frequency should be a Integer value"))
        to_change = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_change= set(rg) & set(self.__get_ranges("online"))
        max_freqs= self.get_max_freq()
        min_freqs= self.get_min_freq()
        for cpu in to_change:
            if freq < min_freqs[cpu] or freq > max_freqs[cpu]:
                raise(CPUFreqErrorInit("ERROR: Frequency should be between min and max frequencies " \
                    "interval: %s - %s." % (min_freqs[cpu],max_freqs[cpu])))
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_setspeed")
            self.__write_cpu_file(fpath, str(freq).encode())

    def set_max_frequencies(self, freq, rg=None):
        """
        Set cores max frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """

        if not type(freq) is int:
            raise(CPUFreqErrorInit("ERROR: Frequency should be a Integer value"))
        to_change = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_change= set(rg) & set(self.__get_ranges("online"))
        min_freqs= self.get_min_freq()
        for cpu in to_change:
            if freq < min_freqs[cpu]:
                raise(CPUFreqErrorInit("ERROR: Frequency should be gt min frequencies " \
                    "interval: %s" % (min_freqs[cpu])))
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_max_freq")
            self.__write_cpu_file(fpath, str(freq).encode())

    def set_min_frequencies(self, freq, rg=None):
        """
        Set cores min frequencies

        freq: int frequency in KHz
        rg: list of range of cores
        """
        if not type(freq) is int:
            raise(CPUFreqErrorInit("ERROR: Frequency should be a Integer value"))
        to_change = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_change= set(rg) & set(self.__get_ranges("online"))
        max_freqs= self.get_max_freq()
        for cpu in to_change:
            if freq > max_freqs[cpu]:
                raise(CPUFreqErrorInit("ERROR: Frequency should be lt max frequencies " \
                    "interval: %s" % (max_freqs[cpu])))
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_min_freq")
            self.__write_cpu_file(fpath, str(freq).encode())

    def set_governors(self, gov, rg=None):
        """
        Set governors

        gov: str name of the governor
        rg: list of range of cores
        """
        to_change = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_change= set(rg) & set(self.__get_ranges("online"))
        for cpu in to_change:
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_governor")
            self.__write_cpu_file(fpath, gov.encode())

    def get_online_cpus(self):
        """
        Get current online cpus
        """
        return self.__get_ranges("online")

    def get_governors(self):
        """
        Get current governors
        """
        return self.__get_cpu_variable("scaling_governor")

    def get_frequencies(self):
        """
        Get current frequency speed
        """
        freqs = self.__get_cpu_variable("scaling_cur_freq")
        for i in freqs:
            freqs[i] = int(freqs[i])
        return freqs
    
    def get_max_freq(self, rg=None):
        """
        Get max frequency possible

        rg: list of range of cores
        """
        to_load = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_load= set(rg) & set(self.__get_ranges("online"))
        data = {}
        for cpu in to_load:
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_max_freq")
            data[int(cpu)] = int(self.__read_cpu_file(fpath).rstrip("\n").split()[0])
        return data
    
    def get_min_freq(self, rg=None):
        """
        Get min frequency possible
        rg: list of range of cores
        """
        to_load = self.__get_ranges("online")
        if type(rg) == int:
            rg= [rg]
        if rg: to_load= set(rg) & set(self.__get_ranges("online"))
        data = {}
        for cpu in to_load:
            fpath = path.join("cpu%i"%cpu,"cpufreq","scaling_min_freq")
            data[int(cpu)] = int(self.__read_cpu_file(fpath).rstrip("\n").split()[0])
        return data
