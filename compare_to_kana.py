# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
#
# Based in part on code by Damien Elmes <anki@ichi2.net>
# and Kieran Clancy
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/licenses/agpl.html

"""
Add-on for Anki 2 to compare typed-in text to just the kana.
"""

import re

from anki.hooks import wrap
from anki.template.furigana import kana
from aqt.reviewer import Reviewer


# First code word to look for in the field name to decide whether to
# do the kanji removal.
reading_field = 'reading'

# Second code word to look for in the note model name.
japanese_model = 'japanese'

### End of configuration block.

__version__ = "2.0.1"


def correct_kana(reviewer, given, correct, showBad=True, _old=None):
    u"""Filter to compare the typed text to just the kana."""
    try:
        crd = reviewer.card
        fld = re.search(r'\[\[type:([^\]]+)\]\]', crd.a()).group(1)
    except AttributeError:
        # No typed answer to show at all.
        return _old(reviewer, given, correct, showBad)
    if not reading_field in fld.lower() or fld.startswith("cq:"):
        return _old(reviewer, given, correct, showBad)
    if not japanese_model in crd.model()[u'name'].lower():
        return _old(reviewer, given, correct, showBad)
    return _old(reviewer, given, kana(correct), showBad)


Reviewer.correct = wrap(Reviewer.correct, correct_kana, "around")
