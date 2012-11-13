# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

preferred_format = ".flac"
"""Ignored on normal installs."""

have_pysox = True
try:
    import pysox
    import pydub
except:
    have_pysox = False

if have_pysox:
    from .normalise import AudioNormaliser
    processor = AudioNormaliser()
else:
    from .move import AudioMover
    processor = AudioMover()
