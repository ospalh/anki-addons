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
import urllib

from aqt import mw
from anki.hooks import addHook

# Tips are only shown for elements that match any of these selectors, that is
# have this class. So, in your template use something like <span
# class="showtips">{{Back}}</span> instead of just {{Back}}.
tip_selectors = ['.showtips', '.furigana', '.furikanji rt', '.kanji']
# tip_selectors = ['rb', '.showtips']
tip_selectors = ['*']  # Everything

question_tips = False
# Set this to True to show tips on the question side as well.

skip_selectors = [
    'script', 'style', 'link', '.notip', '.shd', '.furigana rt']
# Everything that should not get a tip. It is important to skip
# scripts &c., especially when the tip_selectors are rather general.

# all should show stroke orders for latin characters/rōmaji as well.
show_all_stroke_order = False
show_kana_stroke_order = False
show_kanji_stroke_order = True
show_variant_stroke_order = True

kanji_diagram_size = 200
kanji_variant_diagram_size = 120

# None for English
lang_code = None
# There is no German, so use English

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
kanji_code = 'IDEOGRAPH'
katakana_code = 'KATAKANA'
hiragana_code = 'HIRAGANA'

jquery_script = u''
jquery_ui_script = u''
show_tips_script = u''

character_script_template = u'''
$(function() {{
    $( '.{hex_code}' ).tooltip( $.extend({{}}, shared, {{
        content: function() {{
          var content = "";
          {content}
          return content;
        }}
    }}));
}});

'''

plain_kanji_template = u'''
            content += kanji_object("{fn}", {size});
'''

variant_kanji_wrapper_template = u'''
            content += "<figure class=\\"kanjivg variants\\">";\
{vrs}\
            content += "<figcaption>{fc}</figcaption>\\n";
            content += "</figure>\\n";

'''

single_variant_kanji_template = u'''
            content += kanji_variant_object("{fn}", {size});
'''

do_show = False
current_script = u''

# debug: rememeber:
#pp(mw.reviewer.web.page().mainFrame().toHtml())

skip_re = ur"\[(:?sound|type):(:?.*?)\]"


def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes


def read_scripts():
    u"""Read standard scripts."""
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
    u"""Read data files containing information on characters."""
    global character_data_dict
    global jdic2_twigs
    utf8_parser = etree.XMLParser(encoding='utf-8')
    with gzip.open(kanjidic_path, 'rb') as kjdf:
        kjd_string = kjdf.read()
    jdic2_tree = etree.fromstring(kjd_string, parser=utf8_parser)
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
        pass


def base_name(c):
    """Return the base mame of the  svg"""
    if not c.isalnum():
        return '{:05x}'.format(ord(c))
    if c.islower():
        return c + '_'
    return c


def do_this(c, all_non_control):
    """Return whether we should do something for this character."""
    try:
        c = unicode(c, 'utf-8')
    except TypeError:
        pass  # already unicode
    if unicodedata.category(c)[0] in bad_unicode_categories:
        # Never show for control characters.
        return False
    if all_non_control:
        return True
    c_name = unicodedata.name(c)
    if show_kana_stroke_order:
        if katakana_code in c_name or hiragana_code in c_name:
            return True
    if show_kanji_stroke_order and kanji_code in c_name:
        return True
    return False


def stroke_order_tip(c):
    """
    Show plain stroke order diagram.

    Show the plain stroke order diagram for kanji c, it we have a file
    for it
    """
    if not do_this(c, all_non_control=False):
        return u''
    fname = os.path.join(kanjivg_path, base_name(c) + '.svg')
    if os.path.exists(fname):
        return plain_kanji_template.format(
            fn=fname, size=kanji_diagram_size)
    return u''


def stroke_order_variant_tip(c):
    u"""Return bits of a tooltip with stroke order diagrams."""
    if not do_this(c, all_non_control=show_all_stroke_order):
        return u''
    var_scriptext = u''
    captions = []
    for fname in glob.glob(os.path.join(
            kanjivg_path, base_name(c) + u'-*.svg')):
        try:
            variant = re.search(
                u'/{0}-([^/]+).svg$'.format(re.escape(c)), fname).group(1)
        except (AttributeError, KeyError):
            # Shouldn't happen. We just got the names that match this
            # pattern.
            variant = u'Unknown'
        # Replace two variants that are quite common.
        variant = variant.replace(
            'Kaisho', u'<ruby class=nhg><rb>楷書</rb><rt>かいしょ</rt></ruby>')
        variant = variant.replace(
            'Jinmei', u'<ruby class=nhg><rb>人名</rb><rt>じんめい</rt></ruby>')
        var_scriptext += single_variant_kanji_template.format(
            fn=fname, size=kanji_variant_diagram_size)
        captions.append(variant)

    if var_scriptext:
        caption = u''
        if len(captions) > 1:
            for i, v in enumerate(captions):
                caption += u'{l}:&nbsp;{c}, '.format(
                    l=unichr(ord('a') + i), c=v)
        else:
            caption = captions[0]
        caption = caption.rstrip(', ')
        return variant_kanji_wrapper_template.format(
            vrs=var_scriptext, fc=caption)
    return u''


def characterdata_tip(c):
    """Add the string from the character data file or throw a KeyError."""
    return u'            content += "<h3>{cd}</h3>";\n'.format(
        cd=character_data_dict[c])


def kanjidic_tip(c):
    u"""Return bits of a tooltip containing kanjidic information."""
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
    u"""Make a script to show tooltips, when we find suitable characters."""
    global current_script
    if not do_this(glyph, all_non_control=show_all_stroke_order):
        return None
    glyph_element = html.Element('span')
    glyph_element.set('title', glyph)
    hex_code = 'hex_{h:05x}'.format(h=ord(glyph))
    glyph_element.set(
        'class', format(u'kanjitip {g} {h}'.format(g=glyph, h=hex_code)))
    glyph_element.text = glyph
    ct = u''
    if not hex_code in current_script:
        try:
            ct += characterdata_tip(glyph)
        except KeyError:
            pass
        try:
            ct += kanjidic_tip(glyph)
        except KeyError:
            pass
        if show_kanji_stroke_order:
            ct += stroke_order_tip(glyph)
        if show_variant_stroke_order:
            ct += stroke_order_variant_tip(glyph)
    else:
        # We already have a tip, so just return the decorated element.
        return glyph_element
    if ct:
        # We have nothing to put in the tip, so don't return anything.
        current_script += character_script_template.format(
            content=ct, hex_code=hex_code)
        return glyph_element
    # Fall out at the bottom: return None.


def media_characters(s):
    u"""Return positions of characters inside  media file."""
    mc = []
    for m in re.finditer(skip_re, s):
        b, l = m.span()
        mc += range(b, l)
    return mc


def show_tip_filter(qa_html, qa, dummy_fields, dummy_model, dummy_data,
                    dummy_col):
    """
    Filter the answers to add the kanji diagram pop-ups.
    """
    if not question_tips and not qa == 'a':
        return qa_html
    global do_show
    global current_script
    do_show = False
    current_script = show_tips_script
    try:
        doc = html.fromstring(qa_html)
    except:
        return qa_html
    elements = []
    for ts in tip_selectors:
        elements += doc.cssselect(ts)
    elements = uniqify_list(elements)
    for el in elements:
        skip_elements = []
        for skip_sel in skip_selectors:
            skip_elements += el.cssselect(skip_sel)
        skip_elements = uniqify_list(skip_elements)
        for sub_el in el.iter():
            if sub_el in skip_elements:
                continue
            if sub_el.text is not None:
                bad_chars = media_characters(sub_el.text)
                new_index = 0
                new_element = None
                tip_text = u''
                sub_e_t = sub_el.text
                for i, g in enumerate(sub_e_t):
                    if i in bad_chars:
                        tip_text += g
                        continue
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
                bad_chars = media_characters(sub_el.tail)
                parent = sub_el.getparent()
                new_index = parent.index(sub_el) + 1
                new_element = None
                tip_tail = u''
                sub_e_t = sub_el.tail
                for i, g in enumerate(sub_e_t):
                    if i in bad_chars:
                        tip_tail += g
                        continue
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
    return unicode(
        urllib.unquote(html.tostring(doc, encoding='utf-8')), 'utf-8')


def do_scripts():
    u"""When we have something to show, eval the scripts that do so."""
    if not do_show:
        return
    mw.reviewer.web.eval(jquery_script)
    mw.reviewer.web.eval(jquery_ui_script)
    mw.reviewer.web.eval(current_script)


def setup_tips():
    u"""
    Set up the kanjitp mechanism.

    Load the character data.
    Read the global scripts.
    add the hooks.
    """
    read_character_data()
    read_scripts()
    addHook("mungeQA", show_tip_filter)
    if question_tips:
        addHook("showQuestion", do_scripts)
    addHook("showAnswer", do_scripts)
