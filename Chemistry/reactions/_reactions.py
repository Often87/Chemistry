# pyCAOS - An organic chemistry reaction simulator, written in Python
# Copyright (C) 2014 Dan Obermiller
#
# The full license is available in the root directory of the repository

"""Underlying mechanisms and utility classes for chemical reactions."""

__author__ = "Dan Obermiller"


import abc

from Chemistry.base.compounds import _CompoundWrapper


class Conditions(object):
    """Represents the conditions under which the reaction is occurring.

    Parameters
    ----------
    conditions : dict
        Dictionary storing all of the important information.

    Attributes
    ----------
    acidic : bool
        Whether or not the conditions are acidic.
    basic : bool
        Whether or not the conditions are basic.
    neutral
    pka : float
        The pKa of the conditions.
    pka_molecule : Compound
        The compound responsible for the pKa value.
    pka_location : string
        The key ('m*') for the aforementioned pka_molecule.
    """

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
            if k not in ['acidic', 'basic']:
                setattr(self, k, v)
        self._neutral = not (self.acidic or self.basic)

    @property
    def neutral(self):
        """The neutrality of the Conditions.

        Notes
        -----
        A read-only property in order to minimize the danger of creating
        conditions that are False for each of acidity, basicity, and neutrality.
        """

        return self._neutral

    def __contains__(self, key):
        return key in vars(self)

    def __str__(self):
        return "_Reaction conditions"

    def __repr__(self):
        return str(self)


class Solvent(_CompoundWrapper):
    """The solvent in which a reaction occurs.

    Parameters
    ----------
    compound : Compound, _CompoundWrapper
        The compound the solvent consists of
    pka : float
        The pka of the solvent

    Attributes
    ----------
    pka
    """

    _pka = None

    def __init__(self, compound, pka):
        super(Solvent, self).__init__(compound)
        self.pka = pka
        # nucleophilicity and electrophilicity

    @property
    def pka(self):
        """The pka of the solvent.

        Returns
        -------
        self._pka
            The pka of either the compound being wrapped (if already known) or
            the pka passed to the constructor.
        """

        return self._pka

    @pka.setter
    def pka(self, pka):
        cur_pka = getattr(self._compound, 'pka')
        if cur_pka is not None:
            if cur_pka == pka:
                self._pka = cur_pka
                return
            raise ValueError("The pka of a compound does not change")
        self._pka = pka


class _Reaction(object):
    """The abstract base `_Reaction` object.

    Notes
    -----
    Reactions are treated as first class citizens (somewhat like functions).
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def react(self):
        """The specific mechanics of how any given reaction progresses.

        Returns
        -------
        Products, EquilibriumProducts
            The products of the reaction.
        """

        raise NotImplementedError

    @classmethod
    def _remove_node(cls, compound, rem_key):
        """Removes a node from a compound and make a new one based on it.

        Parameters
        ----------
        compound : Compound
            The molecule that needs an atom removed.
        rem_key : string
            The key of the atom.
        """

        compound.atoms.pop(rem_key)
        compound.remove_node(rem_key)

        for k, v in compound.bonds.items():
            if v[0] not in compound.atoms or v[1] not in compound.atoms:
                compound.bonds.pop(k)

        a_ref = cls._generate_new_keys(compound.atoms, 'a')
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
    def _generate_new_keys(dict_, letter):
        """Figures out the new keys necessary after a reaction occurs.

        Returns
        -------
        dict
            A reference dictionary mapping the old keys to the new ones.

        For example,

        >>> _Reaction._generate_new_keys({'a2': 1, 'a3': 2}, 'a')
        {'a3': 'a2', 'a2': 'a1'}
        """

        return {key:'{}{}'.format(letter, i)
                 for i, key in enumerate(sorted(dict_), 1)}


if __name__ == '__main__':
    pass
