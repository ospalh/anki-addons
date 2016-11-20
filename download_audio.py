# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–16 Roland Sieker <ospalh@gmail.com>
# Copyright © 2013 Albert Lyubarsky <albert.lyubarsky@gmail.com>
# Copyright © 2014 Daniel Eriksson, p.e.d.eriksson@gmail.com
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Copyright: Damien Elmes <anki@ichi2.net>
# Check files in the downloadaudio directory for who wrote what.
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Download audio

An add-on for Anki 2 srs to download audio from Google TTS and
Japanese audio from Japanesepod.
"""

# Flake8 complains, but that is OK. We need the imports here. RAS 2012-10-17
import downloadaudio.conflanguage
import downloadaudio.download
import downloadaudio.model
from downloadaudio import __version__
