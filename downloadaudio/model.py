# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
# Inspired by the Japanese Support add-on,
# Copyright: Damien Elmes <anki@ichi2.net>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html
#

u"""
Standard models that work reasonably well with the add-on.
"""

import os

import anki.stdmodels
from aqt import mw

remove_arial = True
# Personally, i think Arial is ugly. So just don’t set a standard font
# and let the user use eir system font.


def add_standard_model(col):
    """
    Add a models.

    This adds a model with audio fields and cards, so users should
    have less problems getting started.
    """
    mm = col.models
    m = mm.new(_("Standard with audio fields"))
    fm = mm.newField(_("Word"))
    mm.addField(m, fm)
    fm = mm.newField(_("Meaning"))
    mm.addField(m, fm)
    fm = mm.newField(_("Audio"))
    mm.addField(m, fm)
    # css
    if remove_arial:
        # Arial is ugly.
        m['css'] = m['css'].replace(
            'font-family: arial;', '/* font-family: arial; */')
    # Recognition card
    t = mm.newTemplate(_("Recognition"))
    t['qfmt'] = "<div>{{Word}}</div>"
    t['afmt'] = """{{FrontSide}}

<hr id=answer>

{{Meaning}}
{{Audio}}"""
    mm.addTemplate(m, t)
    # Recall card
    rev = mm.newTemplate(_("Recall"))
    rev['qfmt'] = "{{Meaning}}"
    rev['afmt'] = """\
{{FrontSide}}

<hr id=answer>

<div> {{Word}} </div>
{{Audio}}"""
    mm.addTemplate(m, rev)
    # Audio card
    aud = mm.newTemplate(_("Audio"))
    aud['qfmt'] = """Listen.
{{Audio}}"""
    aud['afmt'] = """\
{{Audio}}
<span id=answer></span>
<div>{{Word}}</div>
{{Meaning}}
"""
    mm.addTemplate(m, aud)
    mm.add(m)
    return m


def add_japanese_model(col):
    """
    Add a Japanese models.

    This adds a Japanese model with audio fields and cards, so users should
    have less problems getting started.
    """
    mm = col.models
    m = mm.new(_("Japanese with audio fields"))
    fm = mm.newField(_("Expression"))
    mm.addField(m, fm)
    fm = mm.newField(_("Meaning"))
    mm.addField(m, fm)
    fm = mm.newField(_("Reading"))
    mm.addField(m, fm)
    fm = mm.newField(_("Audio"))
    mm.addField(m, fm)
    # css
    m['css'] += u"""\
.jp { font-size: 30px }
.win .jp { font-family: "MS Mincho", "ＭＳ 明朝"; }
.mac .jp { font-family: "Hiragino Mincho Pro", "ヒラギノ明朝 Pro"; }
.linux .jp { font-family: "Kochi Mincho", "東風明朝"; }
.mobile .jp { font-family: "Hiragino Mincho ProN"; }"""
    if remove_arial:
        # Arial is ugly.
        m['css'] = m['css'].replace(
            'font-family: arial;', '/* font-family: arial; */')
    # Recognition card
    t = mm.newTemplate(_("Recognition"))
    t['qfmt'] = "<div class=jp>{{Expression}}</div>"
    t['afmt'] = """{{FrontSide}}

<hr id=answer>

<div class=jp>{{furigana:Reading}}</div>
{{Meaning}}
{{Audio}}"""
    mm.addTemplate(m, t)
    # Recall card
    rev = mm.newTemplate(_("Recall"))
    rev['qfmt'] = "{{Meaning}}"
    rev['afmt'] = """\
{{FrontSide}}

<hr id=answer>

<div class=jp> {{Expression}} </div>
<div class=jp> {{furigana:Reading}} </div>
{{Audio}}"""
    mm.addTemplate(m, rev)
    # Audio card
    aud = mm.newTemplate(_("Audio"))
    aud['qfmt'] = """Listen.
{{Audio}}"""
    aud['afmt'] = """\
{{Audio}}
<span id=answer></span>
<div class=jp> {{Expression}} </div>
<div class=jp> {{furigana:Reading}} </div>
{{Meaning}}
"""
    mm.addTemplate(m, aud)
    mm.add(m)
    return m



anki.stdmodels.models.append(
    (_("Standard with audio fields"), add_standard_model))
if os.path.exists(
        os.path.join(mw.pm.addonFolder(), 'japanese', 'reading.py')):
    anki.stdmodels.models.append(
        (_("Japanese with audio fields"), add_japanese_model))
