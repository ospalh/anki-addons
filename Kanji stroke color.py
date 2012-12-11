# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
#
# Origianl code: Damien Elmes <anki@ichi2.net>, Cayenne Boyer
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Show colored stroke order diagrams.

Add-on for Anki2 to show colored stroke order diagrams for kanji. The
diagrams have to be provided as svg is the right directories.
"""

import glob
import os
import re
from anki import hooks
from aqt import mw

__version__ = '2.1.0'
kanji_size = 200
"""The size the svg is scaled to"""

rest_size = 120
"""Size used for the other variants."""

kanji_directory = 'stroke-order-kanji'
"""Where the kanji are stored.

Where the kanji svgs are stored in the add-ons folder, before they are
copied to the media folder.
"""

variant_display_names = {
    '': 'title="Standard"', '-Jinmei': 'title="Jinmei"',
    '-Kaisho': 'title="Kaisho"'}
"""Mapping file name variants to display variants."""


def ascii_basename(c, var=''):
    u"""
    An SVG filename in ASCII using the same format KanjiVG uses.

    May raise TypeError for some kinds of invalid
    character/variant combinations
    """
    code = '%05x' % ord(c)
    # except TypeError:  # character not a character
    if not var:
        return code + u'.svg'
    else:
        return u'{0}-{1}.svg'.format(code, var)


def character_basename(c, var=''):
    u"""
    An SVG filename that uses the unicode character

    There are two exceptions:
    * non-alphanumeric characters use the ascii_filename
    * lower-case letters get an extra underscore at the end.
    to avoid some (potential) file system problems.
    """
    if not c.isalnum():
        return ascii_basename(c, var)
    if c.islower():
        # This should trigger only for romaji, for kanji isupper()
        # and islower() are both False.
        c = c + u'_'
    if not var:
        return u'{0}.svg'.format(c)
    else:
        return u'{0}-{1}.svg'.format(c, var)


# I don't know how to do a lamba with the *args. So unroll the four.
def kanji_svg_jinmei(txt, *args):
    u"""
    Display the text as colored stroke order diagram.

    Display the text as colored stroke order svg diagram. This version
    uses the Jinmei (人名 or name, i guess) variant, if available.
    """
    return kanji_svg_var(txt, variant='-Jinmei')


def kanji_svg_kaisho(txt, *args):
    u"""
    Display the text as colored stroke order diagram.

    Display the text as colored stroke order svg diagram. This version
    uses the Kaisho (楷書 or square style) variant, if available.
    """
    return kanji_svg_var(txt, variant='-Kaisho')


def kanji_svg_kyoukasho(txt, *args):
    u"""
    Display the text as colored stroke order diagram.

    Display the text as colored stroke order svg diagram. This version
    uses the standard version, which is, as far as i know, schoolbook
    or 教科書/kyoukasho style.
    """
    return kanji_svg_var(txt)


def kanji_svg_rest(txt, *args):
    """
    Display the text as colored stroke order diagrams.

    Display the text as colored stroke order svg diagrams. This
    version shows all the diagrams that are not the standard, in a
    smaller size, wraped in a div, or nothing if there is only one
    variant.
    """
    return kanji_svg_var(txt, show_rest=True)


def kanji_svg_var(txt, variant='', show_rest=False):
    """
    Replace kanji with SVG

    For each character in txt, check if there is an svg to
    display and replace txt with this svg image.
    """
    rtxt = u''
    size = kanji_size
    if show_rest:
        size = rest_size
    for c in txt:
        # Try to get the variant
        fn_title_list = get_file_names_titles(c, variant, show_rest)
        for fname, title_attr in fn_title_list:
            rtxt += u'''<embed width="{size}" height="{size}" \
{title} src="{fname}" />''' .format(
                fname=fname, size=size, title=title_attr)
            # (The title_attr brings along the title="', the others
            # parameters don't)
        if not fn_title_list and not show_rest:
            rtxt += c
    if show_rest and rtxt:
        rtxt = u'<div class="strokevariants">' + rtxt + u'</div>'
    return rtxt


def get_file_names_titles(c, variant, show_rest):
    """ Return the file names of the svgs we should show. """
    name_title_list = []
    if not show_rest:
        fname = os.path.join(mw.addonManager.addonsFolder(),
                             kanji_directory, character_basename(c, variant))
        if variant and not os.path.exists(fname):
            # Maybe we can save this by using the standard version.
            fname = os.path.join(mw.addonManager.addonsFolder(),
                                 kanji_directory, character_basename(c))

        if os.path.exists(fname):
            try:
                title = variant_display_names[variant]
            except KeyError:
                title = ''
            name_title_list.append((fname, title))
    else:
        # The true show-all style, show stroke order variants.
        # (We cheat a bit, this can't work for upper-case romaji
        # letters and for non-alphanumeric characters. There aren't
        # any variants for those, so no harm, no foul.)
        for fname in glob.glob(os.path.join(
                mw.addonManager.addonsFolder(),
                kanji_directory, c + u'-*.svg')):
            try:
                title = re.search(
                    u'/{0}-([^/]+).svg$'.format(re.escape(c)), fname).group(1)
            except AttributeError:
                # Shouldn't happen. We just got the names that match
                # this pattern.
                title = ''
            name_title_list.append((fname, title))
    return name_title_list


hooks.addHook('fmod_kanjiColor', kanji_svg_kyoukasho)
hooks.addHook('fmod_kanjiColorJinmei', kanji_svg_jinmei)
hooks.addHook('fmod_kanjiColorKaisho', kanji_svg_kaisho)
hooks.addHook('fmod_kanjiColorRest', kanji_svg_rest)
