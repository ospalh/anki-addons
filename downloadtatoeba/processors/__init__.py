# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–13 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

u"""
Two classes to deal with audio files.

One just moves files and isn’t used. The other does simple audio
processing and nmoves the files.
"""

preferred_format = ".flac"
"""Ignored on normal installs."""


try:
    import pysox
    import pydub
except ImportError:
    have_pysox = False
else:
    have_pysox = True

if have_pysox:
    from .normalise import AudioNormaliser
    processor = AudioNormaliser()
else:
    from .move import AudioMover
    processor = AudioMover()
