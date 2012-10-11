#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.consts import *
from anki.hooks import addHook

__version__ = "1.0.1"


def maybe_skip_question():
    model = mw.reviewer.card.model()
    if model['type'] != MODEL_STD:
        # Not standard, (i.e., cloze): Something on the back side. So
        # don't skip.
        return
    back = model['tmpls'][mw.reviewer.card.ord]['afmt'].strip()
    print 'back:', back
    if '{{FrontSide}}' == back:
        if not mw.reviewer._bottomReady:
            # Looking at the reviewer.py source code, this may not
            # always show images. But the reviewer code uses some
            # strange voodoo, so i don't really know what to do about
            # it.
            mw.reviewer._showAnswer()
        else:
            try:
                # Currently, this seems to be the right thing to do.
                mw.reviewer._showAnswerHack()
            except NameError:
                # Maybe next week we need this again.
                mw.reviewer._showAnswer()


addHook("showQuestion", maybe_skip_question)
