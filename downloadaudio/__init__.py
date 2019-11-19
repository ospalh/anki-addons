# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–19 Roland Sieker <ospalh@gmail.com>
# Copyright © 2013 Albert Lyubarsky <albert.lyubarsky@gmail.com>
# Copyright © 2014 Daniel Eriksson, p.e.d.eriksson@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Copyright © 2019 Alastair Murray
# Copyright © 2018 Kyle Mills
# Copyright © 2018 Simone Gaiari
# Copyright: Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Anki-2 add-on to download audio.

This is an add-on for Anki-2 that downloads spoken version of the
words in the cards.
"""

__version__ = "6.0.0"

from . import conflanguage
from . import download
from . import model
