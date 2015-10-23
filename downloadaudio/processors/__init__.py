# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

u"""
One just moves files and isn’t used. The other does simple audio
processing and nmoves the files.
"""

try:
    from pydub.silence import detect_nonsilent
    # Look for a reasonable new pydub
except ImportError:
    processor = None
else:
    from .audio_processor import AudioProcessor
    processor = AudioProcessor()
