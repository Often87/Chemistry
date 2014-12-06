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

import abc


class Conditions(object):
    acidic = False
    basic = False
    _neutral = True
    pka = 16
    pka_molecule = None
    pka_location = ''

    def __init__(self, conditions):
        if 'acidic' in conditions and 'basic' in conditions:
            raise ValueError(' '.join(['A molecule is either acidic',
                                         'or basic, not both']))
        if (('acidic' in conditions or 'basic' in conditions) and
                any(item not in conditions
                    for item in ['pka', 'pka_molecule', 'pka_location'])):
            raise ValueError(' '.join(["If conditions aren't neutral the pka",
                                         "must be specified as well as the",
                                         "molecule in question and the",
                                         "specific location (key)"]))
        if 'acidic' in conditions:
            self.acidic = conditions['acidic']
            self.basic = not self.acidic
        elif 'basic' in conditions:
            self.basic = conditions['basic']
            self.acidic = not self.basic
        for k, v in conditions.iteritems():
            if not k in ['acidic', 'basic']:
                setattr(self, k, v)
        self._neutral = not (self.acidic or self.basic)

    @property
    def neutral(self):
        return self._neutral

    def __contains__(self, key):
        return key in self.__dict__

    def __str__(self):
        return "Reaction conditions"

    def __repr__(self):
        return str(self)


class Reaction(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def react(self):
        pass

    @classmethod
    def _remove_node(cls, compound, rem_key):
        compound.atoms.pop(rem_key)
        compound.remove_node(rem_key)

        for k, v in compound.bonds.items():
            if v[0] not in compound.atoms or v[1] not in compound.atoms:
                compound.bonds.pop(k)

        a_ref = cls._rebuild_dict(compound.atoms, 'a')
        new_atoms, new_bonds = {}, {}

        for atom in compound.node:
            new_atoms[a_ref[atom]] = compound.node[atom]['symbol']

        for i, (first, second) in enumerate(compound.edges(), 1):
            endpoints = tuple(sorted((a_ref[first], a_ref[second])))
            rest = ({k:v for k, v in compound.edge[first][second].iteritems()
                     if k != 'key'},)
            new_bonds['b{}'.format(i)] = endpoints + rest

        return new_atoms, new_bonds

    @staticmethod
    def _rebuild_dict(dict_, letter):
        return {key:'{}{}'.format(letter, i)
                 for i, key in enumerate(sorted(dict_), 1)}


if __name__ == '__main__':
    pass