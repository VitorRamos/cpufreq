import cpufreq
import time

cpu = cpufreq.CPUFreq()
cpu.list_current_governos()
cpu.list_current_frequencies()

cpu.change_governo("userspace")
cpu.get_frequencies()  # list of possible frequencies for all cpus
freq = cpu.get_frequencies()[0]['data']  # cpu frequencies
for f in freq:
    print("Frequency %d" % f)
    cpu.change_frequency(f)  # change frequency all cpus
    cpu.list_current_frequencies()
    time.sleep(1)

cpu.change_governo("ondemand")
cpu.list_current_governos()
cpu.list_current_frequencies()

cpu.disable_cpu(3)
time.sleep(5)
cpu.enable_cpu(3)
time.sleep(5)
