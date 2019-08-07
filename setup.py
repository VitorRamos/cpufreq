import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='cpufreq',
      version='0.3.2',
      description='CPU Frequency manage tool',
      url='https://github.com/VitorRamos/cpufreq',
      author='Vitor Ramos, Alex Furtunato',
      author_email='ramos.vitor89@gmail.com, alex.furtunato@academico.ifrn.edu.br',
      license='MIT',
      packages=['cpufreq'],
      install_requires=[
      ],
      long_description=read('README.rst'),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Software Development :: Build Tools",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Scientific/Engineering",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
      ],
      entry_points={
          'console_scripts': [
              'cpufreq = cpufreq.run:main',
          ],
      },
      keywords='cpufreq tool',
      zip_safe=False)
