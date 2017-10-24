# -*- coding: utf-8 ; mode: Python -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
#
# Provenance: This file started out as files written by Damien Elmes
# <anki@ichi2.net>, and Cayenne Boyer. I think there isn't much of
# their code left, but anyway.
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Show colored stroke order diagrams.

Add-on for Anki2 to show colored stroke order diagrams for kanji. The
diagrams have to be provided as svg is the right directories.
"""


# Usually Python comes with 'batteries included', that is, with the
# Python standard library. Unfortunately, this is not the case for a
# typical Anki install. So bring along some files that are
# missing. Make sure we find them.
from aqt import mw  # We need this early to get to the path

# These *are* available with standard Anki
import os
import re
import sys

from PyQt5.QtCore import SIGNAL
from PyQt5.QtWidgets import QAction


# The rest of the anki componets.
from aqt.utils import askUser, tooltip

# Add the path, but only once. (Other add-ons by YT contain
# similar code.)
if not [pe for pe in sys.path if 'batteries' in pe]:
    sys.path.append(os.path.join(mw.pm.addonFolder(), "batteries"))

# Now this should work. Include module to search for file names.
import glob

__version__ = '2.1.0'

src_field = 'Kanji'
dst_field = 'Diagramm'
rest_field = 'Variantendiagramme'


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
    '': 'title="Standard"', 'Jinmei': 'title="Jinmei"',
    'Kaisho': 'title="Kaisho"'}
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
    Copy the variant kanji.

    ...
    """
    return kanji_svg_var(txt, show_rest=True)


def kanji_svg_var(txt, variant='', show_rest=False):
    """
    Replace kanji with SVG

    For each character in txt, check if there is an svg to
    display,
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
                title = 'title="{0}"'.format(
                    re.search(u'/{0}-([^/]+).svg$'.format(
                            re.escape(c)), fname).group(1))

            except (AttributeError, KeyError):
                # Shouldn't happen. We just got the names that match
                # this pattern.
                title = ''
            name_title_list.append((fname, title))
    return name_title_list

### Code below is originally from Cayennes


def model_is_correct_type(model):
    '''
    Returns True if model has Japanese in the name and has both src_field
    and dst_field; otherwise returns False
    '''
    # Does the model name have Japanese in it?
    model_name = model['name'].lower()
    fields = mw.col.models.fieldNames(model)
    return ('japanese' in model_name and src_field in fields and
            dst_field in fields)


def add_kanji(note, flag=False, current_field_index=None):
    '''
    Checks to see if a kanji should be added, and adds it if so.
    '''
    if not model_is_correct_type(note.model()):
        return flag
    if current_field_index is not None:  # We've left a field
        # But it isn't the relevant one
        if note.model()['flds'][current_field_index]['name'] != src_field:
            return None
    src_txt = mw.col.media.strip(note[src_field])

    if not note[dst_field]:
        note[dst_field] = kanji_svg_kyoukasho(src_txt)
    try:
        if not note[rest_field]:
            note[rest_field] = kanji_svg_rest(src_txt)
    except KeyError:
        pass
    note.flush()
    return True

# menu item to copy all


def copy_all():
    # Find the models that have the right name and fields; faster than
    # checking every note
    if not askUser("Fill with kanji diagrams references?"):
        return
    models = [m for m in mw.col.models.all() if model_is_correct_type(m)]
    # Find the notes in those models and give them kanji
    for model in models:
        for nid in mw.col.models.nids(model):
            add_kanji(mw.col.getNote(nid))
    tooltip("Done copying colorized kanji diagrams!")

# add menu item
do_copy_all = QAction("Copy diagrams", mw)
mw.connect(do_copy_all, SIGNAL("triggered()"), copy_all)
mw.form.menuTools.addAction(do_copy_all)
