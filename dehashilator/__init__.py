# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# This file: License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#
# Caveat Emptor. Different files are under different
# licences. Especially progress.py is CC-by-nc.

"""Change the names of files to more readable versions.

Go through an Anki 2 collection and detect files that alook like MD5
hashes used by Anki <1.2, look at the note for a better name and
rename the files, changing the notes as well. This module is rather
useless without Anki 2.

"""

from dehashilator import Dehashilator
from progress import progress
from romaji import *

__version__ = '0.0a5'
__all__ = ['Dehashilator', 'progress', 'roma', 'html', 'kana']
