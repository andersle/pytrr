#####
pytrr
#####

pytrr is a python package for reading .trr files from GROMACS.

Example
=======

.. code:: python

   from pytrr import GroTrrReader

   with GroTrrReader('traj.trr') as trrfile:
       for frame in trrfile:
           print(frame['step'])
           frame_data = trrfile.get_data()
           print(frame_data['x'][0])
