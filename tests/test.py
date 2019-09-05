import unittest
import cpufreq


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

        self.cpu= cpufreq.cpuFreq()
        self.cpu.reset()
        self.online= self.cpu.get_online_cpus()

    def test_min_max(self):
        self.cpu.reset()
        for f in self.cpu.available_frequencies[1:]:
            self.cpu.set_max_frequencies(f)
            is_maxf= lambda x: x == f
            maxfs= self.cpu.get_max_freq().values()
            print(maxfs, f)
            self.assertTrue(all(map(is_maxf,maxfs)))
        
        self.cpu.reset()
        for f in self.cpu.available_frequencies[1:]:
            self.cpu.set_min_frequencies(f)
            is_minf= lambda x: x == f
            minfs= self.cpu.get_min_freq().values()
            self.assertTrue(all(map(is_minf,minfs)))

        ordered_freqs= sorted(self.cpu.available_frequencies)
        self.cpu.reset()
        self.cpu.set_max_frequencies(ordered_freqs[0])
        with self.assertRaises(cpufreq.CPUFreqBaseError):
            self.cpu.set_min_frequencies(ordered_freqs[1])

        self.cpu.reset()
        self.cpu.set_min_frequencies(ordered_freqs[1])
        with self.assertRaises(cpufreq.CPUFreqBaseError):
            self.cpu.set_max_frequencies(ordered_freqs[0])
        
        self.cpu.reset()
        self.cpu.set_min_frequencies(ordered_freqs[2])
        self.cpu.set_max_frequencies(ordered_freqs[4])
        with self.assertRaises(cpufreq.CPUFreqBaseError):
            self.cpu.set_frequencies(ordered_freqs[5])
        with self.assertRaises(cpufreq.CPUFreqBaseError):
            self.cpu.set_frequencies(ordered_freqs[1])
            
    def test_set_governos(self):
        print("Testing set governor")
        # set_governors, get_governors
        self.cpu.reset()
        govs= self.cpu.get_governors()

        self.assertEqual(len(govs), len(self.online))

        # Test set and get governos
        for gov in self.cpu.available_governors:
            self.cpu.set_governors(gov)
            self.assertEqual(self.cpu.get_governors(), dict(zip(self.online,[gov]*len(self.online))))

    def test_enable_disable(self):
        # disable_cpu, enable_cpu, enable_all_cpu
        print("Testing enable/disable")
        self.cpu.reset()
        cpus= self.cpu.get_online_cpus()
        for c in cpus:
            # print("Test cpu", c)
            if c == 0: continue
            self.cpu.disable_cpu(c)
            self.assertTrue( c not in self.cpu.get_online_cpus() )
            self.cpu.enable_cpu(c)
            self.assertTrue( c in self.cpu.get_online_cpus() )

        self.cpu.disable_cpu(range(1,len(cpus)))
        self.assertTrue(len(self.cpu.get_online_cpus()) == 1)
        self.cpu.enable_all_cpu()
        self.assertTrue(len(self.cpu.get_online_cpus()) == len(cpus))

    def test_consistence(self):
        # reset, disable_cpu, set_frequencies, get_online_cpus
        print("Test consistence")
        self.cpu.reset()
        self.cpu.disable_hyperthread()
        self.cpu.set_governors("userspace")

        freq = self.cpu.available_frequencies
        cpus = self.cpu.get_online_cpus()

        for f in freq[1:]:
            for thr in cpus:
                nthr= thr+1
                # print(f,nthr)
                self.cpu.reset(cpus)
                self.cpu.disable_hyperthread()
                self.cpu.set_governors("userspace")
                
                is_userspace= lambda x: "userspace" in x
                govs= self.cpu.get_governors().values()
                self.assertTrue(all(map(is_userspace,govs)))

                self.cpu.disable_cpu(cpus[nthr:])
                notset= len(self.cpu.get_online_cpus()) != nthr
                if notset:
                    print("Problem trying to set the self.cpu online")
                    print("Online cpus ", self.cpu.get_online_cpus())
                    print("Nthreads ", nthr)
                self.assertFalse(notset)

                self.cpu.set_frequencies(f)
                for c in self.cpu.get_online_cpus():
                    with open(f"/sys/devices/system/cpu/cpu{c}/cpufreq/scaling_setspeed","rb") as fx:
                        data= fx.read().decode()
                    data= int(data)
                    if data != int(f):
                        print("Problem trying to set cpu frequency")
                        print(c, data, f)
                        self.assertFalse(data != int(f))
    

if __name__ == "__main__":
    unittest.main()