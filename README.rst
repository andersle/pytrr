#####
pytrr
#####

``pytrr`` is a python package for reading .trr [1]_ files from GROMACS [2]_.

``pytrr`` is intended as a lightweight, pure python, library for reading .trr
trajectories and it gives access to positions, velocities, etc.
as numpy arrays.

Example
=======

.. code:: python

   from pytrr import GroTrrReader

   with GroTrrReader('traj.trr') as trrfile:
       for frame in trrfile:
           print(frame['step'])
           frame_data = trrfile.get_data()
           print(frame_data['x'][0])


Installation
============

pytrr can be installed via pip:

``pip install pytrr``


References
==========

.. [1] http://www.gromacs.org/Developer_Zone/Programming_Guide/XTC_Library
.. [2] http://www.gromacs.org/
