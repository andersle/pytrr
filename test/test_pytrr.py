# -*- coding: utf-8 -*-
# Copyright (c) 2017, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""A test module for pytrr."""
import os
import struct
import tempfile
import unittest
from pytrr.pytrr import (
    swap_integer,
    swap_endian,
    read_trr_header,
    write_trr_frame,
    GroTrrReader,
    TRR_VERSION_B,
    GROMACS_MAGIC,
)
import numpy as np


HERE = os.path.abspath(os.path.dirname(__file__))


def generate_trr_data(output, steps, natoms, double=False, endian=None):
    """Generate some random TRR data."""
    all_data = []
    for i in range(steps):
        data = {
            'natoms': natoms,
            'step': i,
            'time': 0.002*i,
            'lambda': 0.0,
            'box': np.random.ranf(size=(3, 3)),
            'x': np.random.ranf(size=(natoms, 3)),
            'v': np.random.ranf(size=(natoms, 3)),
        }
        header = write_trr_frame(output, data, double=double, append=True,
                                 endian=endian)
        all_data.append((header, data))
    return all_data


class TestGromacsTRR(unittest.TestCase):
    """Test that we can read/write TRR files."""

    def test_swap_integer(self):
        """Test the swap_integer method."""
        test = [(1, 16777216), (2, 33554432), (4, 67108864),
                (8, 134217728), (16, 268435456)]
        for i, j in test:
            self.assertEqual(i, swap_integer(j))
            self.assertEqual(j, swap_integer(i))

    def test_swap_endian(self):
        """Test the swap_endian method."""
        test = [('>', '<'), ('<', '>')]
        for i, j in test:
            self.assertEqual(j, swap_endian(i))
        with self.assertRaises(ValueError):
            swap_endian(1)
        with self.assertRaises(ValueError):
            swap_endian('^')

    def test_read_trr_header(self):
        """Test reading of a TRR header from GROMACS."""
        filename = os.path.join(HERE, 'traj1.trr')
        correct = {
            'v_size': 192,
            'endian': '>',
            'natoms': 16,
            'time': 0.0,
            'box_size': 36,
            'lambda': 0.0,
            'x_size': 192,
            'double': False,  # all others should default to zero.
        }

        with open(filename, 'rb') as inputfile:
            header = read_trr_header(inputfile)
            for key, val in header.items():
                cor = correct.get(key, 0)
                self.assertEqual(val, cor)

    def test_read_trr_file(self):
        """Test reading of several frames in a TRR file."""
        filename = os.path.join(HERE, 'traj1.trr')
        box1 = np.load(os.path.join(HERE, 'box1.npy'), allow_pickle=False)
        xyz1 = np.load(os.path.join(HERE, 'x1.npy'), allow_pickle=False)
        vel1 = np.load(os.path.join(HERE, 'v1.npy'), allow_pickle=False)
        with GroTrrReader(filename) as trrfile:
            for i, header in enumerate(trrfile):
                data = trrfile.get_data()
                self.assertEqual(i * 10, header['step'])
                self.assertEqual(16, header['natoms'])
                self.assertTrue(np.allclose(box1[i], data['box']))
                self.assertTrue(np.allclose(xyz1[i], data['x']))
                self.assertTrue(np.allclose(vel1[i], data['v']))

        with GroTrrReader(filename) as trrfile:
            header, data = trrfile.read_frame(read_data=True)
            self.assertEqual(0, header['step'])
            self.assertTrue(np.allclose(box1[0], data['box']))
            self.assertTrue(np.allclose(xyz1[0], data['x']))
            self.assertTrue(np.allclose(vel1[0], data['v']))
            header, data = trrfile.read_frame(read_data=False)
            self.assertEqual(10, header['step'])
            self.assertEqual(0, len(data))

    def test_read_double_trr(self):
        """Test that we can read double precision TRR files."""
        file1 = os.path.join(HERE, 'traj-double.trr')
        file2 = os.path.join(HERE, 'traj-single.trr')
        with GroTrrReader(file1) as trrfile1, GroTrrReader(file2) as trrfile2:
            for double, single in zip(trrfile1, trrfile2):
                self.assertAlmostEqual(double['time'], single['time'],
                                       places=5)
                self.assertTrue(double['double'])
                self.assertFalse(single['double'])
                trrfile1.get_data()
                trrfile2.get_data()

    def test_read_error_trr(self):
        """Test reading of a faulty TRR file."""
        filename = os.path.join(HERE, 'error.trr')
        with self.assertRaises(struct.error):
            with GroTrrReader(filename) as trrfile:
                for header in trrfile:
                    print(header)

    def test_write_trr(self):
        """Test that we can write simple TRR files."""
        compare_direct = {'natoms', 'vir_size', 'ir_size', 'sym_size',
                          'top_size', 'v_size', 'f_size', 'box_size',
                          'x_size', 'step', 'pres_size', 'nre', 'e_size',
                          'double'}
        cases = (
            {'double': False},
            {'double': True},
            {'double': False, 'endian': '<'},
            {'double': False, 'endian': '>'},
        )
        for case in cases:
            with tempfile.NamedTemporaryFile() as tmp:
                all_data = generate_trr_data(tmp.name, 10, 11,
                                             double=case.get('double', False),
                                             endian=case.get('endian', None))
                tmp.flush()
                with GroTrrReader(tmp.name) as gro:
                    for header, correct in zip(gro, all_data):
                        data = gro.get_data()
                        header2, data2 = correct
                        for key in compare_direct:
                            self.assertEqual(header[key], header2[key])
                        for key in ('time', 'lambda'):
                            self.assertAlmostEqual(header[key], header2[key])
                        for key, val in data.items():
                            self.assertTrue(np.allclose(val, data2[key]))
                        if header2['endian']:
                            self.assertEqual(header['endian'],
                                             header2['endian'])

    def test_overwrite_trr(self):
        """Test that we indeed can turn off the append to trr."""
        with tempfile.NamedTemporaryFile() as tmp:
            all_data = []
            for i in range(5):
                data = {
                    'natoms': 4,
                    'step': i,
                    'time': 0.002*i,
                    'lambda': 0.0,
                    'box': np.random.ranf(size=(3, 3)),
                    'x': np.random.ranf(size=(4, 3)),
                }
                header = write_trr_frame(tmp.name, data, double=False,
                                         append=False)
                all_data.append((header, data))
            tmp.flush()
            with GroTrrReader(tmp.name) as gro:
                header, data = gro.read_frame(read_data=True)
                self.assertTrue(np.allclose(data['x'],
                                            all_data[-1][1]['x']))

    def test_read_size(self):
        """Test that we can get double/float when box is missing."""
        slen = (13, 12)
        fmt = ['1i', '2i', '{}s'.format(slen[0] - 1), '13i']
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, 'wb') as outfile:
                outfile.write(struct.pack(fmt[0], GROMACS_MAGIC))
                outfile.write(struct.pack(fmt[1], *slen))
                outfile.write(struct.pack(fmt[2], TRR_VERSION_B))
                x_size = 3 * 10 * struct.calcsize('f')
                head = [0, 0, 0, 0, 0, 0, 0, x_size, 0, 0, 10, 0, 0]
                outfile.write(struct.pack(fmt[3], *head))
                outfile.write(struct.pack('1f', 0.0))
                outfile.write(struct.pack('1f', 0.0))
            with GroTrrReader(tmp.name) as gro:
                header, _ = gro.read_frame(read_data=False)
                self.assertFalse(header['double'])

    def test_read_size_fail(self):
        """Test that we fail when we can't find precision."""
        slen = (13, 12)
        fmt = ['1i', '2i', '{}s'.format(slen[0] - 1), '13i']
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, 'wb') as outfile:
                outfile.write(struct.pack(fmt[0], GROMACS_MAGIC))
                outfile.write(struct.pack(fmt[1], *slen))
                outfile.write(struct.pack(fmt[2], TRR_VERSION_B))
                x_size = 3 * 10 * (struct.calcsize('d') + 1)
                head = [0, 0, 0, 0, 0, 0, 0, x_size, 0, 0, 10, 0, 0]
                outfile.write(struct.pack(fmt[3], *head))
                outfile.write(struct.pack('1f', 0.0))
                outfile.write(struct.pack('1f', 0.0))
            with self.assertRaises(ValueError):
                with GroTrrReader(tmp.name) as gro:
                    gro.read_frame(read_data=False)

    def test_read_wrong_header(self):
        """Test that we get an error when reading wrong version of TRR"""
        slen = (13, 12)
        fmt = ['1i', '2i', '{}s'.format(slen[0] - 1), '13i']
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, 'wb') as outfile:
                outfile.write(struct.pack(fmt[0], GROMACS_MAGIC))
                outfile.write(struct.pack(fmt[1], *slen))
                outfile.write(struct.pack(fmt[2], b'NOT_GMX_FILE'))
                head = [0, 0, 26, 0, 0, 0, 0, 1000, 0, 0, 10, 0, 0]
                outfile.write(struct.pack(fmt[3], *head))
                outfile.write(struct.pack('1f', 0.0))
                outfile.write(struct.pack('1f', 0.0))
            with self.assertRaises(ValueError):
                with GroTrrReader(tmp.name) as gro:
                    gro.read_frame(read_data=False)


if __name__ == '__main__':
    unittest.main()
