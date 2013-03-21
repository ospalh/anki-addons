# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# and Kieran Clancy
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Add-on for Anki 2 to compare typed-in text to just the kana.
"""

import re
from aqt import mw
from anki.hooks import addHook
from anki.template.furigana import kana

# First code word to look for in the field name to decide whether to
# do the kanji removal.
reading_field = 'reading'

# Second code word to look for in the note model name.
japanese_model = 'japanese'

### End of configuration block.

__version__ = "1.0.1"


def correct_kana(res, right, typed, card):
    try:
        fld = re.search('\[\[type:([^\]]+)\]\]', card.a()).group(1)
    except AttributeError:
        # No typed answer to show at all.
        return res
    if not reading_field in fld.lower() or fld.startswith("cq:"):
        return res
    if not japanese_model in card.model()[u'name'].lower():
        return res
    return mw.reviewer.correct(u'', kana(right), typed, card)


addHook("filterTypedAnswer", correct_kana)
