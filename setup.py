#!/usr/bin/env python
from setuptools import setup, find_packages
import sys

# quick hack, will probably do something better later.
install_requires = [
        "DecoratorTools==1.8",
        ]

setup(name='mockbuild',
      description='mock is a simple chroot manager for building RPMs',
      version='1.1.36dev',
      install_requires=install_requires,
      long_description=open("README").read(),
      author='Alan Franzoni',
      license='GPL',
      keywords='RPM packaging',
      author_email='username@franzoni.eu',
      url='http://fedoraproject.org/wiki/Projects/Mock',
      entry_points = {
        "console_scripts":["mock=mockbuild.cmdline:cmdline_mock" ]
        },

      )
