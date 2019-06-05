import unittest
import cpufreq


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

        self.cpu= cpufreq.cpuFreq()
        self.cpu.reset()
        self.online= self.cpu.get_online_cpus()

    def test_set_governos(self):
        govs= self.cpu.get_governors()

        self.assertEqual(len(govs), len(self.online))

        # Test set and get governos
        for gov in self.cpu.available_governors:
            self.cpu.set_governors(gov)
            self.assertEqual(self.cpu.get_governors(), dict(zip(self.online,[gov]*len(self.online))))
        
        # TODO: Test set and get governos in range
        for gov in self.cpu.available_governors:
            self.cpu.set_governors(gov)
            self.assertEqual(self.cpu.get_governors(), dict(zip(self.online,[gov]*len(self.online))))


    def test_set_frequencies(self):
        pass
    
    def test_online_cpu(self):
        pass
    

if __name__ == "__main__":
    unittest.main()