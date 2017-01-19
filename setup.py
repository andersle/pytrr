# -*- coding: utf-8 -*-
# Copyright (c) 2017, AL.
# Distributed under the LGPLv3 License. See LICENSE for more info.
"""
pytrr - A simulation package for rare event simulations.
Copyright (C) 2017, AL.

This file is part of pytrr.

pytrr is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pytrr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pytrr. If not, see <http://www.gnu.org/licenses/>
"""
from codecs import open as openc
import os
from setuptools import setup, find_packages


def get_long_description():
    """Return the contents of README.rst"""
    here = os.path.abspath(os.path.dirname(__file__))
    # Get the long description from the README file
    long_description = ''
    with openc(os.path.join(here, 'README.rst'), encoding='utf-8') as fileh:
        long_description = fileh.read()
    return long_description


FULL_VERSION = '0.2.0.dev2'  # copied from version.py generated.

setup(name='pytrr',
      version=FULL_VERSION,
      description='A package for reading GROMACS .trr files',
      long_description=get_long_description(),
      url='https://github.com/andersle/pytrr',
      author='AL',
      author_email='andersle@gmail.com',
      license='LGPLv3',
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   ('License :: OSI Approved :: '
                    'GNU Lesser General Public License v3 (LGPLv3)'),
                   'Natural Language :: English',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Topic :: Scientific/Engineering :: Physics'],
      keywords='gromacs simulation trr',
      packages=find_packages(),
      install_requires=['numpy>=1.6.0',])
