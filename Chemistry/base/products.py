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

import types


class Product(object):
    _compound = None

    def __init__(self, comp, percentage):
        self._compound = comp
        self.percentage = percentage

    def __getattr__(self, attr):
        return getattr(self._compound, attr)

    def __eq__(self, other):
        try:
            return self._compound == other._compound
        except AttributeError:
            return self._compound == other

    def __str__(self):
        return str(self._compound)

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self._compound)

    def __getitem__(self, key):
        return self._compound[key]


class Products(object):

    def __init__(self, maj, min_):
        self._major, self._minor = (), ()
        self.major = maj
        self.minor = min_

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, products):
        if not isinstance(products, types.NoneType):
            for prod in products:
                if isinstance(prod, Product):
                    if isinstance(prod._compound, types.NoneType):
                        continue
                    self._major += (prod,)
                elif isinstance(prod, types.NoneType):
                    continue
                else:
                    raise TypeError(
                            "Should be a Product, not a {}".format(type(prod)))
        else:
            return

    @property
    def minor(self):
        return self._minor

    @minor.setter
    def minor(self, products):
        if not isinstance(products, types.NoneType):
            for prod in products:
                if isinstance(prod, Product):
                    if isinstance(prod._compound, types.NoneType):
                        continue
                    self._minor += (prod,)
                elif isinstance(prod, types.NoneType):
                    continue
                else:
                    raise TypeError(
                            "Should be a Product, not a {}".format(type(prod)))
        else:
            return

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return not self == other


class EquilibriumProducts(object):
    _reactants = None
    _products = None

    def __init__(self, reactants, products):
        self.reactants = reactants
        self.products = products

    @property
    def products(self):
        return self._products

    @products.setter
    def products(self, prod):
        self._products = Products(*prod)

    @property
    def reactants(self):
        return self._reactants

    @reactants.setter
    def reactants(self, reactant):
        self._reactants = reactant