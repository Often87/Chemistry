"""
Copyright (c) 2014 Dan Obermiller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

You should have received a copy of the MIT License along with this program.
If not, see <http://opensource.org/licenses/MIT>
"""

import itertools
import os
import tempfile
import unittest

from Chemistry import compounds
from Chemistry.parsing import CheML as cml


class test_cml_parser(unittest.TestCase):
    primary = os.getcwd()

    def setUp(self):
        os.chdir(os.path.join(self.primary, "Chemistry", "Testing",
                              "test_molecules", "CML"))
        self.molecule = {'atoms': {'a1': 'H',
                                   'a2': 'H',
                                   'a3': 'O'},
                         'bonds': {'b1': ('a1', 'a3', {'order': 1,
                                                       'chirality': None}),
                                   'b2': ('a2', 'a3', {'order': 1,
                                                       'chirality': None})},
                         'other_info': {'id': 'Water'}}

    def test_parse(self):
        with open('CML_1.cml', 'r') as CML_file:
            Parser = cml.CMLParser(CML_file)
        self.assertEqual(Parser.molecule,
                         self.molecule)

    def tearDown(self):
        os.chdir(self.primary)


class test_cml_builder(unittest.TestCase):
    primary = os.getcwd()

    def setUp(self):
        os.chdir(os.path.join(self.primary, "Chemistry", "Testing",
                              "test_molecules", "CML"))
        with open('CML_1.cml', 'r') as cml_file:
            self.molecule = cml.CMLParser(cml_file)
            cml_file.seek(0)
            self.cml = cml_file.read()
        self.Builder1 = cml.CMLBuilder(
                {'atoms': {'a1': 'H',
                           'a2': 'H',
                           'a3': 'O'},
                 'bonds': {'b1': ['a1', 'a3', {'order':1,
                                               'chirality': None}],
                           'b2': ['a2', 'a3', {'order':1,
                                               'chirality': None}]},
                 'other_info': {'id': 'Water'}})
        self.Builder2 = cml.CMLBuilder(self.molecule.molecule)

    def test_to_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.cml',
                                         dir=self.primary) as tfile:
            self.Builder1.to_file(tfile)
            tfile.seek(0)
            Builder3 = cml.CMLBuilder(cml.CMLParser(tfile).molecule)
            self.assertEqual(str(self.Builder1), str(Builder3))

    def test_build(self):
        for line1, line2 in itertools.izip(
                                            str(self.Builder1).split('\n'),
                                            self.cml.split('\n')
                                           ):
            self.assertEqual(line1.lstrip(), line2.lstrip())

    def test_from_Compound(self):
        Builder = cml.CMLBuilder.from_Compound(
                    compounds.Compound.from_CML("CML_1.cml"))

        with tempfile.NamedTemporaryFile(
                                          mode='r+',
                                          suffix='.cml',
                                          dir=os.getcwd()
                                         ) as tfile:
            Builder.to_file(tfile)
            tfile.seek(0)
            self.assertEqual(compounds.Compound.from_CML("CML_1.cml").molecule,
                             compounds.Compound.from_CML(tfile).molecule)


if __name__ == '__main__':
    import types
    import sys


    test_classes_to_run = [value for key, value in globals().items()
                           if (isinstance(value, (type, types.ClassType)) and
                               issubclass(value, unittest.TestCase))]

    loader = unittest.TestLoader()
    big_suite = unittest.TestSuite(loader.loadTestsFromTestCase(test_class)
                                   for test_class in test_classes_to_run)

    runner = unittest.TextTestRunner(sys.stdout, verbosity=1)
    runner.run(big_suite)