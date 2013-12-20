#! /usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

setup(name='Bob',
      version='0.1.0',
      author='Eric Hutton',
      author_email='eric.hutton@colorado.edu',
      description='Create scripts to build packages',
      packages=['bob', ],
      entry_points={
          'console_scripts': [
              'bob = bob.cmd:main',
          ]},
     )
