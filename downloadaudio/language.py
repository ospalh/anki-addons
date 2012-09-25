#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
import os
from aqt import mw


## Set the two-letter language code for the language you are learning
## here. (This is typically not your native language.)
default_audio_language_code = "ja"

"""
Return a two-letter language code.
"""


def get_language_code(card=None, note=None):
    if not card and not note:
        return default_audio_language_code
    # Test. Always return ja.
    return default_audio_language_code
