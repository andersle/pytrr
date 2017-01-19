# -*- coding: utf-8 -*-
# Copyright (c) 2017, AL.
# Distributed under the LGPLv3 License. See LICENSE for more info.
"""
pytrr - A package for reading GROMACS .trr files.
Copyright (C) 2017, AL.

This file only generates the verison info.
"""
import os
import subprocess


# For setting version. This is copied from Numpy's setup.py.
MAJOR = 0
MINOR = 1
MICRO = 0
DEV = 0
ISRELEASED = False
if not ISRELEASED:
    VERSION = '{:d}.{:d}.{:d}.dev{:d}'.format(MAJOR, MINOR, MICRO, DEV)
else:
    VERSION = '{:d}.{:d}.{:d}'.format(MAJOR, MINOR, MICRO)
VERSION_FILE = os.path.join('pytrr', 'version.py')
VERSION_TXT = '''# -*- coding: utf-8 -*-
# Copyright (c) 2017, AL.
# Distributed under the LGPLv3 License. See LICENSE for more info.
"""Version information for pytrr.

This file is generated by the script ``setup_version.py``.
"""
SHORT_VERSION = '{0:s}'
VERSION = '{0:s}'
FULL_VERSION = '{1:s}'
GIT_REVISION = '{2:s}'
GIT_VERSION = '{3:s}'
RELEASE = {4:}

if not RELEASE:
    VERSION = GIT_VERSION
'''


def get_git_version():
    """Method to obtain the git revision as a string.

    This method is adapted from Numpy's setup.py

    Returns
    -------
    git_revision : string
        The git revision, it the git revision could not be determined,
        a 'Unknown' will be returned.
    """
    git_revision = 'Unknown'
    try:
        env = {}
        for key in ('SYSTEMROOT', 'PATH'):
            val = os.environ.get(key)
            if val is not None:
                env[key] = val
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(['git', 'rev-parse', 'HEAD'],
                               stdout=subprocess.PIPE,
                               env=env).communicate()[0]
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = 'Unknown'
    return git_revision


def get_version_info():
    """Return the version number for pytrr.

    This method is adapted from Numpy's setup.py.

    Returns
    -------
    full_version : string
        The full version string for this release.
    git_revision : string
        The git revision number.
    """
    if os.path.exists('.git'):
        git_revision = get_git_version()
    elif os.path.exists(VERSION_FILE):
        try:
            from pytrr.version import git_revision
        except ImportError:
            raise ImportError('Unable to import git_revision. Try removing '
                              'pytrr/version.py and the build directory '
                              'before building.')
    else:
        git_revision = 'Unknown'
    if not ISRELEASED:
        git_version = ''.join([VERSION.split('dev')[0],
                               'dev{:d}+'.format(DEV),
                               git_revision[:7]])
    else:
        git_version = VERSION
    full_version = VERSION
    return full_version, git_revision, git_version


def write_version_py():
    """Create a file with the version info for pytrr.

    This method is adapted from Numpy's setup.py.
    """
    full_version, git_revision, git_version = get_version_info()
    version_txt = VERSION_TXT.format(VERSION, full_version,
                                     git_revision, git_version, ISRELEASED)
    with open(VERSION_FILE, 'wt') as vfile:
        try:  # will work in python 3
            vfile.write(version_txt)
        except UnicodeEncodeError:  # for python 2
            vfile.write(version_txt.encode('utf-8'))
    return full_version

if __name__ == '__main__':
    fullversion = write_version_py()
    print('Setting version to: {}'.format(fullversion))
