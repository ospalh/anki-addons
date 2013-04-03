# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to show information on kanji."""

import os
from lxml import html
import unicodedata

from aqt import mw
from anki.hooks import addHook


# Tips are only shown for elements that match this selector, that is
# have this class. So, in your template use something like <span
# class="showtips">{{Back}}</span> instead of just {{Back}}.
tips_selector = '.showtips'

## This string is used as a "css selector". Pretty much everything
## that works in a CSS3 file should work as well. Some ideas:
# tips_selector = 'rb'  # Or only show tips for rb (ruby base) elements,
                        # that is, for characters with furigana above.
# tips_selector = '*'  # Everywhere

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


# jq_path =  'jquery-1.9.1.js'
# jqui_path =  'jquery-ui.1.10.2.js'
# tip_script_path = 'show_tips.js'
# tip_style_path = 'show_tips.css'
jq_path = os.path.join(os.path.dirname(__file__), 'jquery-1.9.1.js')
jqui_path = os.path.join(os.path.dirname(__file__), 'jquery-ui.1.10.2.js')
tips_script_path = os.path.join(os.path.dirname(__file__), 'show_tips.js')
tips_style_path = u'file://' + os.path.join(
    os.path.dirname(__file__), 'show_tips.css')

jquery_script = u''
jquery_ui_script = u''
show_tips_script = u''

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


def read_scripts():
    global jquery_script
    global jquery_ui_script
    global show_tips_script
    with open(jq_path) as jqf:
        jquery_script = jqf.read()
    with open(jqui_path) as jqf:
        jquery_ui_script = jqf.read()
    with open(tips_script_path) as tf:
        show_tips_script = tf.read()



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
    glyph_element.set('title', glyph)
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
    added_tip = False
    for el in doc.cssselect(tips_selector):
        for sub_el in el.iter():
            if sub_el.text is not None:
                new_el = None
                new_el_count = 0
                tip_text = u''
                sub_e_t = sub_el.text
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        added_tip = True
                        if new_el is None:
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
            if sub_el is not el and sub_el.tail is not None:
                # We have to skip the tail of the element that
                # trigered the selector. That is *not* in the
                # selector.
                new_el = None
                tip_tail = u''
                sub_e_t = sub_el.tail
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        added_tip = True
                        if new_el is None:
                            sub_el.tail = tip_tail
                        else:
                            new_el.tail = tip_tail
                        # We have to inser this into the parent, not
                        # this sub_el.
                        par = sub_el.getparent()
                        par.insert(par.index(sub_el) + 1, ge)
                        new_el = ge
                        tip_tail = u''
                    else:
                        tip_tail += g
                if new_el is not None:
                    new_el.tail = tip_tail
    tt_style = html.Element('link')
    tt_style.set('type','text/css')
    tt_style.set('rel', 'stylesheet')
    tt_style.set('href', tips_style_path)
    tt_style.tail = '\n'
    doc[1].append(tt_style)
    return html.tostring(doc, encoding='unicode')


def do_scripts():
    mw.reviewer.web.eval(jquery_script)
    mw.reviewer.web.eval(jquery_ui_script)
    mw.reviewer.web.eval(show_tips_script)


def setup_tips():
    read_character_data()
    read_scripts()
    addHook("filterAnswerText", show_tip_filter)
    addHook("filterQuestionText", show_tip_filter)
    # Looks like we cant just load scripts. So eval them after we've
    # done the rest of the card.
    addHook("showAnswer", do_scripts)
    addHook("showQuestion", do_scripts)
