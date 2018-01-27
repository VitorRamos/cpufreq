import cpufreq
import time

x= cpufreq.CPUFreq()
x.lits_current_governos()
x.list_current_frequencies()

x.change_governo("userspace")
freq= x.get_frequencies()[0]['data']
for f in freq:
	print "Frequencia ", f
	x.change_frequency(f)
	x.list_current_frequencies()
	time.sleep(1)

x.change_governo("ondemand")
x.lits_current_governos()
x.list_current_frequencies()

x.disable_cpu(3)
time.sleep(5)
x.enable_cpu(3)
time.sleep(5)
