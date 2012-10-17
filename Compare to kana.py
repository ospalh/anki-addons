# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net> and Kieran
# Clancy
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""Add-on for Anki 2 to compare typed-in text to just the kana.
"""

import re
from aqt.reviewer import Reviewer
from anki.utils import stripHTML

# First code word to look for in the field name to decide whether to
# do the kanji removal.
reading_field = 'reading'

# Second code word to look for in the note model name.
japanese_model = 'japanese'

### End of configuration block.

__version__ = "1.0.1"

kanji_kana_re = r' ?([^ ]+?)\[(.+?)\]'


def no_sound(repl):
    def func(match):
        if match.group(2).startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            return re.sub(kanji_kana_re, repl, match.group(0))

    return func


def kana(txt, *args):
    # We have to be careful when we get a str ('', i guess), not a
    # unicode object. We pass what we return on to Reviewer.correct, and
    # that expects unicode.
    try:
        # EAFP: convert the str or unicode to unicode ...
        txt = unicode(txt, 'utf-8')
    except TypeError:
        # which will not work when this is already unicode
        pass
    return re.sub(kanji_kana_re, no_sound(r'\2'), txt, flags=re.UNICODE)


def kana_type_ans_answer_filter(self, buf):
    # Redo bits of typeQuesAnswerFilter to get the field name typed in
    # and most of the old typeAnsAnswerFilter.
    m = re.search(self.typeAnsPat, buf)
    if not self.typeCorrect:
        return re.sub(self.typeAnsPat, "", buf)
    # tell webview to call us back with the input content
    # Copy-and-pasted. I guess it’s harmless
    self.web.eval("_getTypedText();")
    # munge correct value
    model_name = self.card.model()[u'name']
    # Cascade of tests
    if m:
        fld = m.group(1)
        # if not fld.startswith("cq:") and reading_field in fld.lower():
        if not fld.startswith("cq:") and reading_field in fld.lower() \
                and japanese_model in model_name.lower():
            cor = self.mw.col.media.strip(stripHTML(self.typeCorrect))
            # The extra kana(...) here is the whole point of this plugin.
            res = self.correct(kana(cor), self.typedAnswer)
            return re.sub(self.typeAnsPat, """
<span id=coranskana style="font-family: '%s'; font-size: %spx">%s</span>""" %
                          (self.typeFont, self.typeSize, res), buf)
    # Still here: we failed one of our tests. So do it the old way.
    return old_type_ans_answer_filter(self, buf)


old_type_ans_answer_filter = Reviewer.typeAnsAnswerFilter
Reviewer.typeAnsAnswerFilter = kana_type_ans_answer_filter
