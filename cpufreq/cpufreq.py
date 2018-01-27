import os
import re

class CPUFreq:
	def __init__(self):
		self.basedir= "/sys/devices/system/cpu"
		self.governos= self.readFromCPUFiles('scaling_available_governors')
		self.frequencies= self.readFromCPUFiles('scaling_available_frequencies')
	
	def readFromCPUFiles(self, file_name):
		cpu= {'cpu':0, 'data':0}
		cpus= []
		for dir in os.listdir(self.basedir):
			if re.match('cpu[0-9]',dir):
				try:
					gov= open(self.basedir+"/"+dir+"/cpufreq/"+file_name, "rb")
					data= filter(None,gov.read().rstrip('\n').split(' '))
					cpu['cpu']= int(dir.strip('cpu'))
					cpu['data']= data
					cpus.append(cpu.copy())
				except IOError:
					print "Error: File does not appear to exist.", self.basedir+"/"+dir+"/cpufreq/"+file_name
		return cpus
	
	def writeOnCPUFiles(self, file_name, data):
		for dir in os.listdir(self.basedir):
			if re.match('cpu[0-9]',dir):
				try:
					gov= open(self.basedir+"/"+dir+"/cpufreq/"+file_name, "wb")
					gov.write(data)
				except IOError:
					print "Error: File does not appear to exist.", self.basedir+"/"+dir+"/cpufreq/"+file_name

	def get_governos(self):
		return self.governos
	
	def get_frequencies(self):
		return self.frequencies	

	def list_governos(self):
		for cpu in self.governos:
			print cpu['cpu'], cpu['data']

	def list_frequencies(self):
		for cpu in self.frequencies:
			print cpu['cpu'], cpu['data']
	
	def lits_current_governos(self):
		for cpu in self.readFromCPUFiles('scaling_governor'):
			print cpu['cpu'], cpu['data']
	
	def list_current_frequencies(self):
		for cpu in self.readFromCPUFiles('cpuinfo_cur_freq'):
			print cpu['cpu'], cpu['data']
	
	def change_governo(self, name, cpu= -1):
		if not name in self.governos[0]['data']:
			return

		if cpu == -1:
			self.writeOnCPUFiles('scaling_governor', name)
		else:
			try:
				gov= open(self.basedir+"/cpu"+str(cpu)+"/cpufreq/scaling_governor", "wb")
				gov.write(name)
			except IOError:
				print "Error: File does not appear to exist.", self.basedir+"/cpu"+str(cpu)+"/cpufreq/scaling_governor"
		
	def change_frequency(self, freq, cpu= -1):
		if not freq in self.frequencies[0]['data']:
			return

		if cpu == -1:
			self.writeOnCPUFiles('scaling_setspeed', freq)
		else:
			try:
				gov= open(self.basedir+"/cpu"+str(cpu)+"/cpufreq/scaling_setspeed", "wb")
				gov.write(freq)
			except IOError:
				print "Error: File does not appear to exist.", self.basedir+"/cpu"+str(cpu)+"/cpufreq/scaling_setspeed"
	
	def disable_cpu(self, cpu):
		try:
			on= open(self.basedir+"/cpu"+str(cpu)+"/online", "r+b")
			f= on.read()
			if '1' in f:
				on.write("0")
			on.close()
		except IOError:
			print "Error: File does not appear to exist.", self.basedir+"/cpu"+str(cpu)+"/online"
	
	def enable_cpu(self, cpu):
		try:
			on= open(self.basedir+"/cpu"+str(cpu)+"/online", "r+b")
			f= on.read()
			if '0' in f:
				on.write("1")
			on.close()
		except IOError:
			print "Error: File does not appear to exist.", self.basedir+"/cpu"+str(cpu)+"/online"

