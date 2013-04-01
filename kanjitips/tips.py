# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to show information on kanji."""

import re
from lxml import html

from anki.hooks import addHook

# Tips are only shown for elements that match this selecotr, that is
# have this class. So, in your template use something like <span
# class="showtips">{{Back}}</span> instead of just {{Back}}.
tips_selector = '.showtips'

# all should show stroke orders for latin characters/rōmaji as well.
show_all_stroke_order = False
show_kana_stroke_order = True
show_kanji_stroke_order = True
show_variant_stroke_order = True

kanji_diagram_size = 200
kanji_variant_diagram_size = 200




tip_kanji_diagram_template = u"""\
<object width="{size}" height="{size}" title="{title}" \
data="{kanji}.svg"type="image/svg+xml">{kanji}</object>"""
tip_base_template = u"""{}"""


kanji_code = 'CJK UNIFIED IDEOGRAPH'
katakana_code = 'KATAKANA'
hiragana_code = 'HIRAGANA'


# debug: rememeber:
# pp(mw.reviewer.web.page().mainFrame().toHtml())



def do_this(c):
    if show_all_stroke_order:
        return True
    c_name = unicodedata.name(c)
    if show_kana_stroke_order:
        if katakana_code in c_name or hiragana_code in c_name:
            return True
    if show_kanji_stroke_order and kanji_code in c_name:
        return True
    return False


def add_tip(glyph):
    if not do_this(glyph):
        return glyph
    return html.fragment_fromstring(glyph, create_parent='span')

def show_tip_filter(res, qa, card):
    """
    Filter the questions and answers to add the kanji diagram pop-ups.

    When certain conditions are met, return the typed-in answer in
    red, yellow or green, depending how close the given answer was to
    the correct one.
    """
    doc = html.fromstring(qa)
    for el in doc.cssselect(tips_selector):
        for sub_el in el.iter():
            if sub_el.text is not None:
                tip_text = u''
                for g in sel.text:
                    tip_text += add_tip(g)
                sub_el.text = tip_text
    return html.tostring(doc, encoding='unicode')

def setup_tips():
    addHook("profileLoaded", deploy.maybe_deploy)
    addHook("filterAnswerText", show_tip_filter)
    addHook("filterQuestionText", show_tip_filter)
