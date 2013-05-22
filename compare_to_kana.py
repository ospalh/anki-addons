# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# and Kieran Clancy
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Add-on for Anki 2 to compare typed-in text to just the kana.
"""

import re

from anki.hooks import addHook
from anki.template.furigana import kana
from aqt import mw


# First code word to look for in the field name to decide whether to
# do the kanji removal.
reading_field = 'reading'

# Second code word to look for in the note model name.
japanese_model = 'japanese'

### End of configuration block.

__version__ = "2.0.0"


def correct_kana(res, typed, right, card):
    u"""Filter to compare the typed text to just the kana."""
    try:
        fld = re.search(r'\[\[type:([^\]]+)\]\]', card.a()).group(1)
    except AttributeError:
        print (u'no type in {}'.format(card.a()))
        # No typed answer to show at all.
        return res
    if not reading_field in fld.lower() or fld.startswith("cq:"):
        print 'cloze  or not reading'
        return res
    if not japanese_model in card.model()[u'name'].lower():
        print 'not japanese'
        return res
    print (u'do the compare with {}, not with {}'.format(kana(right), right))
    return mw.reviewer.correct(u'', typed, kana(right), card, showBad=True)


addHook("filterTypedAnswer", correct_kana)
