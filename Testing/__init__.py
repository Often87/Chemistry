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

from . import test_CML
from . import test_CML2
from . import test_compound_graphs
from . import test_graphs3
from . import test_reactions
from . import test_periodic_helpers

import os
import logging
import sys


logging.basicConfig(stream=sys.stdout, 
                    filename=os.getcwd()+"/testLog.log",
                    level=logging.DEBUG)
cur_dir = os.getcwd()
try:
    try:
        os.chdir(os.getcwd() + "/desktop/programming/github/chemistry/Testing")
    except Exception:
        try: 
            os.chdir(os.getcwd() + "/Testing")
        except Exception:
            print 1
            os.chdir(cur_dir)
    finally:
        for path in os.listdir(os.getcwd()):
            if (path.startswith('test_') and 
                (path.endswith('.py') or path.endswith('.pyc'))):
                cut_path = path.split('.')[0]
                if cut_path not in globals():
                    try:
                        globals()[cut_path] = __import__(cut_path)
                    except ImportError as e:
                        print e
                    finally:
                        logging.warn(
                            "{} was not imported for testing".format(cut_path))
finally:
    os.chdir(cur_dir)
