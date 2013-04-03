# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to show information on kanji."""

import os
import gzip
from lxml import html, etree
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
# tips_selector = '*'  # Everywhere. NB: This WILL mess up audio/video
                       # with kanji in the file name

# all should show stroke orders for latin characters/rōmaji as well.
show_all_stroke_order = False
show_kana_stroke_order = False
show_kanji_stroke_order = True
show_variant_stroke_order = True

kanji_diagram_size = 200
kanji_variant_diagram_size = 120

# We do use a few file-wide variables. (I don't really want to put all
# this in a class. Sholud work OK.
do_show = False
current_script = u''

tip_kanji_diagram_template = u"""\
<object width="{size}" height="{size}" title="{title}" \
data="{kanji}.svg"type="image/svg+xml">{kanji}</object>"""
tip_base_template = u"""{}"""


# None for English
# lang_code = None
lang_code = 'de'

# jq_path =  'jquery-1.9.1.js'
# jqui_path =  'jquery-ui.1.10.2.js'
# tip_script_path = 'show_tips.js'
# tip_style_path = 'show_tips.css'
jq_path = os.path.join(os.path.dirname(__file__), 'jquery-1.9.1.js')
jqui_path = os.path.join(os.path.dirname(__file__), 'jquery-ui.1.10.2.js')
tips_script_path = os.path.join(os.path.dirname(__file__), 'show_tips.js')

jqui_style_path = u'file://' + os.path.join(
    os.path.dirname(__file__), 'jquery-ui.css')
jqui_theme_style_path = u'file://' + os.path.join(
    os.path.dirname(__file__), 'jquery.ui.theme.css')
tips_style_path = u'file://' + os.path.join(
    os.path.dirname(__file__), 'show_tips.css')

kanjidic_path = os.path.join(os.path.dirname(__file__), 'kanjidic2.xml.gz')
jdic2_root = None

jquery_script = u''
jquery_ui_script = u''
show_tips_script = u''

character_script_template = u'''
$(function() {{
    $( '.{hex_code}' ).tooltip({{
        track: true,
        hide: {{
            effect: "fade",
        }},
        content: function() {{
          {content}
        }}
    }});
}});

'''

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
    global jdic2_root
    utf8_parser = etree.XMLParser(encoding='utf-8')
    with gzip.open(kanjidic_path, 'rb') as kjdf:
        s = kjdf.read()
    jdic2_tree = etree.fromstring(s, parser=utf8_parser)
    jdic2_root = jdic2_tree
    fname = os.path.join(os.path.dirname(__file__), character_data_file_name)
    try:
        with open(fname) as kanji_data:
            for l in unicode(kanji_data.readlines(), 'utf-8'):
                ls = l.split(cd_separator)
                if len(ls) > 1 and len(ls[0]) == 1:
                    character_data_list[ls[0]] = ls[1:]
    except IOError:
        pass


def base_name(c):
    """Return the base mame of the  svg"""
    if not c.isalnum():
        return '{:05x}'.format(ord(c))
    if c.islower():
        return c + '_'
    return c


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
    global current_script
    if not do_this(glyph):
        return None
    glyph_element = html.Element('span')
    glyph_element.set('title', glyph)
    hex_code = 'hex_{h:05x}'.format(h=ord(glyph))
    glyph_element.set(
        'class', format(u'kanjitip {g} {h}'.format(g=glyph, h=hex_code)))
    glyph_element.text = glyph
    if not hex_code in current_script:
        ct = u''
        kd_lit = jdic2_root.xpath(
            u'character/literal[text()="{}"]'.format(glyph))
        try:
            kd_element = kd_lit[0].getparent()
        except IndexError:
            ct = u'return "{c} ({h})";'.format(c=glyph, h=hex_code)
        else:
            mgs = u''
            for mg in kd_element.findall('.//meaning'):
                try:
                    if mg.get('m_lang') == lang_code:
                        mgs += "{}, ".format(mg.text)
                except TypeError:
                    # Deal with the case that exactly one of the two
                    # sides in the if is None. (Above, we may compare
                    # None == None instead of None is None, which is
                    # not recommendet, but works (at least in Python
                    # 2.7 and 3.3) EAFP
                    pass
            mgs = mgs.rstrip(', ')
            if mgs:
                ct = u'return "{mgs}";'.format(mgs=mgs)
        current_script += character_script_template.format(
            content=ct, hex_code=hex_code)
    return glyph_element

def show_tip_filter(qa, card):
    """
    Filter the questions and answers to add the kanji diagram pop-ups.

    When certain conditions are met, return the typed-in answer in
    red, yellow or green, depending how close the given answer was to
    the correct one.
    """
    global do_show
    global current_script
    do_show = False
    current_script = show_tips_script
    doc = html.fromstring(qa)
    for el in doc.cssselect(tips_selector):
        for sub_el in el.iter():
            if sub_el.text is not None:
                new_index = 0
                new_element = None
                tip_text = u''
                sub_e_t = sub_el.text
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        do_show = True
                        if new_element is None:
                            sub_el.text = tip_text
                        else:
                            # new_element is the old new element...
                            new_element.tail = tip_text
                        sub_el.insert(new_index, ge)
                        new_index += 1
                        new_element = ge
                        tip_text = u''
                    else:
                        tip_text += g
                if new_element is not None:
                    new_element.tail = tip_text
            if sub_el is not el and sub_el.tail is not None:
                # We have to skip the tail of the element that
                # trigered the selector. That is *not* in the
                # selector.
                parent = sub_el.getparent()
                new_index = parent.index(sub_el) + 1
                new_element = None
                tip_tail = u''
                sub_e_t = sub_el.tail
                for g in sub_e_t:
                    ge = maybe_make_tip(g)
                    if ge is not None:
                        do_show = True
                        if new_element is None:
                            sub_el.tail = tip_tail
                        else:
                            new_element.tail = tip_tail
                        # We have to inser this into the parent, not
                        # into this sub_el.
                        parent.insert(new_index, ge)
                        new_index += 1
                        new_element = ge
                        tip_tail = u''
                    else:
                        tip_tail += g
                if new_element is not None:
                    new_element.tail = tip_tail
    if do_show:
        head = doc[1]
        jqui_style = html.Element('link')
        jqui_style.set('type','text/css')
        jqui_style.set('rel', 'stylesheet')
        jqui_style.set('href', jqui_style_path)
        jqui_style.tail = '\n'
        head.append(jqui_style)
        jqui_theme_style = html.Element('link')
        jqui_theme_style.set('type','text/css')
        jqui_theme_style.set('rel', 'stylesheet')
        jqui_theme_style.set('href', jqui_theme_style_path)
        jqui_theme_style.tail = '\n'
        head.append(jqui_theme_style)
        tt_style = html.Element('link')
        tt_style.set('type','text/css')
        tt_style.set('rel', 'stylesheet')
        tt_style.set('href', tips_style_path)
        tt_style.tail = '\n'
        head.append(tt_style)
    return html.tostring(doc, encoding='unicode')


def do_scripts():
    if not do_show:
        return
    mw.reviewer.web.eval(jquery_script)
    mw.reviewer.web.eval(jquery_ui_script)
    mw.reviewer.web.eval(current_script)


def setup_tips():
    read_character_data()
    read_scripts()
    addHook("filterAnswerText", show_tip_filter)
    addHook("filterQuestionText", show_tip_filter)
    # Looks like we cant just load scripts. So eval them after we've
    # done the rest of the card.
    addHook("showAnswer", do_scripts)
    addHook("showQuestion", do_scripts)
