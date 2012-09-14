#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
import os
from aqt import mw
from aqt.qt import *

#from anki.cards import Card
#from anki.notes import Note
from anki.hooks import addHook

#from forvo import get_word_from_forvo
#from google_tts import get_word_from_google
from japansepod  import get_word_from_jpod

from rewiew_gui import store_or_blacklist

# debug:
#from aqt.utils import showText

"""
Anki2 add-on to download pronunciations.

This add-on downloads pronunciations from up to three sites:
Japanese-pod: This looks for a field called reading(*) and triss to
              get a pronunciation from the languagepod website. As the
              name suggests, these are only Japanese words. The
              pronunciations that are there are rather high-quality,
              though.
Google TTS: Get pronunciations from the Google Text-To-Speech service. These are
            robot voices, so be a bit suspicous about them.
Forvo: Try to get pronunciations from the crowd-sourced forvo.com.
       Pronunciations are often noisy and may turn out to be wrong. To
       use this service, you need to register at forvo.com and get a
       “developer” key. The free service is limited to 1000 requests
       per day.

There are three ways to download: Current card, current note and
manual.
 * The current card download looks at audio field in what is
   currently shown and tries to download only for those. This should
   limit the information leaked before you answer a card.
 * Current note tries to fill all audio fields of the current
   note. This may reveal, that information that you tried to remember,
   potentially ahead of time.
 * Manual works like current note, but shows a list of candidate
   strings that can be modified before the requests are sent.
"""


## Change these to mach the field names of your decks. Make sure to
## not use capital letters. We compare these to lower-case only
## versions of the field names. When these lists contain upper-case
## letters, no field will ever be matched and nothing will be
## downloaded.
expression_fields = ['expression', 'front', 'back']
japanese_reading_keys = ["reading", "kana", u'かな',u'仮名']
audio_field_keys = ["audio", "sound"]



## End configuration area

icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')

# Change this at your own risk.
field_name_re = '{{(?:[/^#]|[^:}]+:|)([^:}{]*%s[^:}{]*)}}'


def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes

def field_source_name(note, fname, readings=False):
    """
    Return a suitable source field name.

    Look for a suitable field to get the source text from and return it.
    If no suitable field is found, a KeyError is raised.

    There are four ways the source field is determined:
    * readings is False:
      * when fname is in one of the strings is audio_field_key,
        expression_fields is used as list of candidates
      * when the audio_field_key is only a substring of fname, that substring
        and a trailing or leading ' ' or '_' is removed and that used
        as the candidate.
    * readings is True:
      * when fname is in one of the strings is audio_field_key,
        japanese_reading_keys is used as list of candidates
      * when the audio_field_key is only a substring, that substring
        is replaced by the strings from japanese_reading_keys

    The first field that matches the candidate is used.  Comparisions
    are done with lowercase strings, the uppercase name is returned.
    """
    t_name = fname.lower()
    field_names = [item[0] for item in note.items()]
    f_names = [fn.lower() for fn in field_names]
    for afk in audio_field_keys:
        if t_name == afk:
            if readings:
                sources_list = japanese_reading_keys
            else:
                sources_list = expression_fields
            for cnd in sources_list:
                for idx, lname in enumerate(f_names):
                    if cnd == lname:
                        return field_names[idx]
            # At this point: The target name is good, but we found no
            # source name.
            raise KeyError("No source name found (case 1)")
        # This point: target name is not exactly the field name
        if not afk in t_name:
            # And not a substring either
            continue
        # Here: the field name contains an audio or sound.
        # Mangle the name as described. For the readings case we get a
        # list. So do a list for the other case as well.
        if readings:
            sources_list = [t_name.replace(afk, rk)
                            for rk in japanese_reading_keys]
        else:
            # Here the tricky bit is to remove the right number of '_'
            # or ' ' characters, 0 or 1, but not 2. What we want is:
            # ExampleAudio -> Example
            # Example_Audio -> Example
            # Audio_Example -> Example
            # but
            # Another_Audio_Example -> Another_Example, not Another_Example
            # While a bit tricky, this is not THAT hard to do. (Not
            # lookbehind needed.)
            sources_list = [re.sub('[\s_]{0}|{0}[\s_]?'.format(re.escape(afk)),
                                   '', t_name, count=1)]
        for cnd in sources_list:
            for idx, lname in enumerate(f_names):
                if cnd == lname:
                    return field_names[idx]
        # We do have audio or sound as sub-string but did not find a
        # maching field.
        raise KeyError("No source field found. (case 2)")
    # No audio field at all.
    raise KeyError("No source field found. (case 3)")





def get_side_fields(card, note, japanese=False):
    """
    Get a list of field name pairs for "visible" download fields.

    Check the visible side of the current card for fields that contain
    a string from audio_field_keys.
    Then check the
    """
    if 'question' == mw.reviewer.state:
        template = card.template()[u'qfmt']
    else:
        template = card.template()[u'afmt']
    audio_field_name_list = []
    for afk in audio_field_keys:
        # Append all fields in the current template/side that contain
        # 'audio' or 'sound'
        audio_field_name_list += re.findall(field_name_re % (re.escape(afk), ),
                                            template, flags=re.IGNORECASE)
    audio_field_name_list = uniqify_list(audio_field_name_list)
    all_field_names = [item[0] for item in note.items()]
    # Filter out non-existing fields.
    audio_field_name_list = [fn for fn in audio_field_name_list
                             if fn in all_field_names]
    field_pairs_list = []
    for fname in audio_field_name_list:
        try:
            field_pairs_list.append((field_source_name(note, fname,
                                                       readings=japanese),
                                     fname))
        except KeyError:
            pass
    return field_pairs_list



def get_note_fields(note, japanese=False):
    field_names = [item[0] for item in note.items()]
    field_pairs_list = []
    for afk in audio_field_keys:
        for fn in field_names:
            if afk in fn.lower():
                try:
                    field_pairs_list.append((field_source_name(note, fn,\
                                                      readings=japanese),
                                             fn))
                except KeyError:
                    pass
    return field_pairs_list

def download_fields(note, general_pairs, japanese_pairs):
    # debug. just look that we get the right fields for now
    retrieved_files_list = []
    for source, dest in general_pairs:
        text = note['source']
        print 'Get pronunciation from ', text, ' (field ', source,\
            ') and put it in field ' , dest
    #    try:
    #        dl_fname, dl_hash = get_word_from_forvo(text, dest)
    #    else:
    #        retrieved_files_list.append((source, dest, text, dl_fname, dl_hash))
    #    try:
    #        dl_fname, dl_hash = get_word_from_google(text, dest)
    #    else:
    #        retrieved_files_list.append((source, dest, text, dl_fname, dl_hash))
    for source, dest in japanese_pairs:
        text = note['source']
        print 'Get Japanese pronunciation from ', text, ' (field ', source,\
            ') and put it in field ' , dest
        try:
            dl_fname, dl_hash = get_word_from_jpod(text, dest)
        else:
            # That is, no exception
            retrieved_files_list.append((source, dest, text, dl_fname, dl_hash))
    if retrieved_files_list:
        store_or_blacklist(note, retrieved_files_list)


def download_for_side():
    card = mw.reviewer.card
    if not card:
        return
    note = card.note()
    # Brainstorm: things to use:
    # note.items()
    # note.model()
    # field_names = [item[0] for item in note.items()]
    # field_contents_1 = [item[1] for item in note.items()]
    # field_contents_2 = note.values()
    general_field_pairs = get_side_fields(card, note)
    if "japanese" in note.model()['name'].lower():
        japanese_field_pairs = get_side_fields(card, note, japanese=True)
    else:
        japanese_field_pairs = []
    download_fields(note, general_field_pairs, japanese_field_pairs)

def download_for_note():
    note = mw.reviewer.card.note()
    if not note:
        return
    general_field_pairs = get_note_fields(note)
    if "japanese" in note.model()['name'].lower():
        japanese_field_pairs = get_note_fields(note, japanese=True)
    else:
        japanese_field_pairs = []
    download_fields(note, general_field_pairs, japanese_field_pairs)



def download_off():
    note_download_action.setEnabled(False)
    side_download_action.setEnabled(False)

def download_on():
    note_download_action.setEnabled(True)
    side_download_action.setEnabled(True)


note_download_action = QAction(mw)
note_download_action.setText(u"Note audio")
note_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_note_audio.png')))
note_download_action.setToolTip("Download audio for all audio fields " + \
                                "of this note.")
mw.connect(note_download_action, SIGNAL("triggered()"), download_for_note)

side_download_action = QAction(mw)
side_download_action.setText(u"Side audio")
side_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_side_audio.png')))
side_download_action.setToolTip("Download audio for audio fields " + \
                                "currently visible.")
mw.connect(side_download_action, SIGNAL("triggered()"), download_for_side)

mw.form.menuTools.addAction(note_download_action)
mw.form.menuTools.addAction(side_download_action)
