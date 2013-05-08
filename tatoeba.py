# -*- mode: python ; coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright © 2013 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""
Tatoeba download.

An add-on for Anki 2 to download example sentences from Tatoeba.org.
"""


# Flake8 complains, but that is OK. We need the imports here. RAS 2012-10-17
import downloadtatoeba.conflanguage
import downloadtatoeba.download
from downloadtatoeba import __version__
