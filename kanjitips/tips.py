# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to show information on kanji."""

from lxml import html, etree
import codecs
import glob
import gzip
import os
import re
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

# None for English
lang_code = None
# lang_code = 'fr'

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
jdic2_twigs = {}

character_data_path = os.path.join(
    os.path.dirname(__file__), u'kanji_info.txt')
character_data_dict = {}

kanjivg_path = os.path.join(os.path.dirname(__file__), 'kanji_vg')

bad_unicode_categories = 'C'  # Don’t even ask for the name of control
                              # characters.
kanji_code = 'CJK UNIFIED IDEOGRAPH'
katakana_code = 'KATAKANA'
hiragana_code = 'HIRAGANA'

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
          var content = "";
          {content}
          return content;
        }}
    }});
}});

'''

plain_kanji_template = u'''
            content += "<div class=\\"kanjivg standard\\">";
            content += kanji_object("{fn}", {size});
            content += "</div>\\n";
'''

variant_kanji_wrapper_template = u'''
            content += "<div class=\\"kanjivg variants\\">";\
{vrs}\
            content += "</div>\\n";

'''

single_variant_kanji_template = u'''
            content += kanji_object("{fn}", {size}, "{var}");
'''

do_show = False
current_script = u''

# debug: rememeber:
#pp(mw.reviewer.web.page().mainFrame().toHtml())


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
    global character_data_dict
    global jdic2_twigs
    utf8_parser = etree.XMLParser(encoding='utf-8')
    with gzip.open(kanjidic_path, 'rb') as kjdf:
        s = kjdf.read()
    jdic2_tree = etree.fromstring(s, parser=utf8_parser)
    for el in jdic2_tree.findall('character'):
        jdic2_twigs[el.find('literal').text] = el
        # We turn the tree not into a loose-leaf collection, but a
        # collcetion of the character-'twigs', (small sub-trees)

    try:
        with codecs.open(character_data_path, 'r', encoding='utf-8') \
                as kanji_data:
            for l in kanji_data.readlines():
                l = l.rstrip()
                try:
                    if l[1] == ' ':
                        character_data_dict[l[0]] = l[2:]
                except IndexError:
                    pass
    except IOError:
        raise


def base_name(c):
    """Return the base mame of the  svg"""
    if not c.isalnum():
        return '{:05x}'.format(ord(c))
    if c.islower():
        return c + '_'
    return c


def do_this(c):
    """Return whether we should do something for this character."""
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


def stroke_order_tip(c):
    """Show the plain kanji c, it we have a file for it"""
    fname = os.path.join(kanjivg_path, base_name(c) + '.svg')
    if os.path.exists(fname):
        return plain_kanji_template.format(
            fn=fname, size=kanji_diagram_size)
    return u''


def stroke_order_variant_tip(c):
    var_scriptext = u''
    for fname in glob.glob(os.path.join(
            kanjivg_path, base_name(c) + u'-*.svg')):
        try:
            variant = re.search(
                u'/{0}-([^/]+).svg$'.format(re.escape(c)), fname).group(1)
        except (AttributeError, KeyError):
            # Shouldn't happen. We just got the names that match this
            # pattern.
            variant = 'Unknown'
        var_scriptext += single_variant_kanji_template.format(
            fn=fname, size=kanji_variant_diagram_size, var=variant)
    if var_scriptext:
        return variant_kanji_wrapper_template.format(vrs=var_scriptext)
    return u''


def characterdata_tip(c):
    """Add the string from the character data file or throw a KeyError."""
    return u'            content += "<h3>{cd}</h3>";\n'.format(
        cd=character_data_dict[c])


def kanjidic_tip(c):
    kd_element = jdic2_twigs[c]
    # This may throw. we catch one level higher
    meanings = u''
    for meaning_element in kd_element.findall('.//meaning'):
        try:
            if meaning_element.get('m_lang') == lang_code:
                meanings += "{}, ".format(meaning_element.text)
        except TypeError:
            # Deal with the case that exactly one of the two sides in
            # the if is None. (Above, we may compare None == None
            # instead of None is None, which is not recommendet, but
            # works (at least in Python 2.7 and 3.3) EAFP
            pass
    meanings = meanings.rstrip(', ')
    if meanings:
        return u'            content += "<div>{mgs}</div>";\n'.format(
            mgs=meanings)
    return u''


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
        try:
            ct += characterdata_tip(glyph)
        except KeyError:
            pass
        try:
            ct += kanjidic_tip(glyph)
        except KeyError:
            pass
        if show_kanji_stroke_order:
            try:
                ct += stroke_order_tip(glyph)
            except:
                pass
        if show_variant_stroke_order:
            try:
                ct += stroke_order_variant_tip(glyph)
            except:
                pass
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
        jqui_style.set('type', 'text/css')
        jqui_style.set('rel', 'stylesheet')
        jqui_style.set('href', jqui_style_path)
        jqui_style.tail = '\n'
        head.append(jqui_style)
        jqui_theme_style = html.Element('link')
        jqui_theme_style.set('type', 'text/css')
        jqui_theme_style.set('rel', 'stylesheet')
        jqui_theme_style.set('href', jqui_theme_style_path)
        jqui_theme_style.tail = '\n'
        head.append(jqui_theme_style)
        tt_style = html.Element('link')
        tt_style.set('type', 'text/css')
        tt_style.set('rel', 'stylesheet')
        tt_style.set('href', tips_style_path)
        tt_style.tail = '\n'
        head.append(tt_style)
    return html.tostring(doc, encoding='unicode', method='xml')


def do_scripts():
    if not do_show:
        return
    mw.reviewer.web.eval(jquery_script)
    mw.reviewer.web.eval(jquery_ui_script)
    mw.reviewer.web.eval(current_script)


def setup_tips():
    read_character_data()
    read_scripts()
    # addHook("filterQuestionText", show_tip_filter)
    ## Uncomment the line above to also show tips on the question.
    addHook("filterAnswerText", show_tip_filter)

    ## Looks like we cant just load scripts. So eval them after we've
    ## done the rest of the card.
    # addHook("showQuestion", do_scripts)
    ## Uncomment the line above to also show tips on the question.
    addHook("showAnswer", do_scripts)
