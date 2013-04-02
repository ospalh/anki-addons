# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to show information on kanji."""

import os
from lxml import html
import unicodedata

from anki.hooks import addHook

# Tips are only shown for elements that match this selector, that is
# have this class. So, in your template use something like <span
# class="showtips">{{Back}}</span> instead of just {{Back}}.
tips_selector = '.showtips'
# tips_selector = 'rb'  # Or only show tips for rb (ruby base) elements,
                      # that is, for characters with furigana above.

# all should show stroke orders for latin characters/rōmaji as well.
show_all_stroke_order = False
show_kana_stroke_order = False
show_kanji_stroke_order = True
show_variant_stroke_order = True

kanji_diagram_size = 200
kanji_variant_diagram_size = 120



tip_kanji_diagram_template = u"""\
<object width="{size}" height="{size}" title="{title}" \
data="{kanji}.svg"type="image/svg+xml">{kanji}</object>"""
tip_base_template = u"""{}"""

bad_unicode_categories = 'C'  # Don’t even ask for the name of control
                              # characters.
kanji_code = 'CJK UNIFIED IDEOGRAPH'
katakana_code = 'KATAKANA'
hiragana_code = 'HIRAGANA'


# debug: rememeber:
#pp(mw.reviewer.web.page().mainFrame().toHtml())

character_data_list = {}
character_data_file_name = u'character_data.txt'
cd_separator = '\r'

def read_character_data():
    global character_data_list
    print __file__
    fname = os.path.join(os.path.dirname(__file__), character_data_file_name)
    try:
        with open(fname) as kanji_data:
            for l in unicode(kanji_data.readlines(), 'utf-8'):
                ls = l.split(cd_separator)
                if len(ls) > 1 and len(ls[0]) == 1:
                    character_data_list[ls[0]] = ls[1:]
    except IOError:
        pass


def do_this(c):
    try:
        c = unicode(c, 'utf-8')
    except TypeError:
        pass  # already unicode
    if unicodedata.category(c)[0] in bad_unicode_categories:
        # Never show for control characters.
        return False
    if show_all_stroke_order:
        return True
    c_name = unicodedata.name(c)
    if show_kana_stroke_order:
        if katakana_code in c_name or hiragana_code in c_name:
            return True
    if show_kanji_stroke_order and kanji_code in c_name:
        return True
    return False


def maybe_make_tip(glyph):
    if not do_this(glyph):
        return None
    glyph_element = html.fragment_fromstring(glyph, create_parent='span')

    print(u'Turning “{}” into “{}”.'.format(
            glyph, html.tostring(glyph_element, encoding='unicode')))
    return glyph_element

def show_tip_filter(qa, card):
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
                new_el = None
                new_el_count = 0
                print(u'text: ‘{}’ (length: {}'.format(
                        sub_el.text, len(sub_el.text)))
                tip_text = u''
                sub_e_t = sub_el.text
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        if not new_el:
                            sub_el.text = tip_text
                        else:
                            # new_el is the old new element...
                            new_el.tail = tip_text
                        sub_el.insert(new_el_count, ge)
                        new_el = ge
                        tip_text = u''
                        new_el_count += 1
                    else:
                        tip_text += g
                if new_el is not None:
                    new_el.tail = tip_text
            if sub_el.tail is not None:
                new_el = None
                print(u'tail: ‘{}’ (length: {}'.format(
                        sub_el.tail, len(sub_el.tail)))
                tip_tail = u''
                sub_e_t = sub_el.tail
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        if not new_el:
                            sub_el.tail = tip_tail
                        else:
                            new_el.tail = tip_tail
                        sub_el.insert(-1, ge)
                        new_el = ge
                        tip_tail = u''
                    else:
                        tip_tail += g
                if new_el is not None:
                    new_el.tail = tip_text
    return html.tostring(doc, encoding='unicode')

def setup_tips():
    read_character_data()
    addHook("filterAnswerText", show_tip_filter)
    addHook("filterQuestionText", show_tip_filter)
