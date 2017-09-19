# -*- coding: utf-8 -*-
# Copyright (c) 2017, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
pytrr - A library for reading GROMACS .trr files.
Copyright (C) 2017, Anders Lervik.

This file is part of pytrr.

pytrr is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 2.1 of the License, or
(at your option) any later version.

pytrr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with pytrr. If not, see <http://www.gnu.org/licenses/>
"""
import ast
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


def get_version():
    """Read the version from version.py"""
    here = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(here, 'pytrr', 'version.py')
    with openc(filename, encoding='utf-8') as fileh:
        for lines in fileh:
            if lines.startswith('FULL_VERSION ='):
                version = ast.literal_eval(lines.split('=')[1].strip())
                return version
    return 'unknown'


def get_requirements():
    """Read requirements.txt"""
    here = os.path.abspath(os.path.dirname(__file__))
    requirements = []
    filename = os.path.join(here, 'requirements.txt')
    with openc(filename, encoding='utf-8') as fileh:
        for lines in fileh:
            package = lines.split('>=')[1].strip()
            requirements.append(lines.strip())
    return requirements


setup(
    name='pytrr',
    version=get_version(),
    description='A package for reading GROMACS .trr files',
    long_description=get_long_description(),
    url='https://github.com/andersle/pytrr',
    author='Anders Lervik',
    author_email='andersle@gmail.com',
    license='LGPLv2.1+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v2 or later (LGPLv2+)'),
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords='gromacs simulation trr',
    packages=find_packages(),
    install_requires=get_requirements(),
)
