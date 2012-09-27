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

from google_tts import get_word_from_google
from japanesepod  import get_word_from_jpod
from review_gui import store_or_blacklist
from update_gui import update_data
from language import get_language_code
from anki.template import furigana

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

def field_data(note, fname, readings=False):
    """
    Return a suitable source field name and the text in that field.

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

    Also returned is the text from the field, as one string when
    reading is False, As two strings, kanji and kana, when reading is
    True
    """
    def return_data(idx):
        text = note[field_names[idx]]
        if readings:
            return field_names[idx], fname,\
                furigana.kanji(text), furigana.kana(text)
        else:
            return field_names[idx], fname, text

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
                        return return_data(idx)
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
                    return return_data(idx)
        # We do have audio or sound as sub-string but did not find a
        # maching field.
        raise KeyError("No source field found. (case 2)")
    # No audio field at all.
    raise KeyError("No source field found. (case 3)")





def get_side_fields(card, note, japanese=False):
    """
    Get a list of field data for "visible" download fields.

    Check the visible side of the current card for fields that contain
    a string from audio_field_keys.  Then check the note for these
    fields and suitable data source fields.
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
    field_data_list = []
    for fname in audio_field_name_list:
        try:
            field_data_list.append(
                field_data(note, fname, readings=japanese))
        except KeyError:
            pass
    return field_data_list



def get_note_fields(note, japanese=False):
    """
    Get a list of field data for download.

    Check all field names and return source and destination fields for
    downloading audio.
    """
    field_names = [item[0] for item in note.items()]
    field_data_list = []
    for afk in audio_field_keys:
        for fn in field_names:
            if afk in fn.lower():
                try:
                    field_data_list.append(
                        field_data(note, fn, readings=japanese))
                except KeyError:
                    pass
    return field_data_list

def download_fields(note, general_data, japanese_data, language=None):
    """
    Download data for the fields provided.

    Go to the (planned three, at the moment one) site(s) and download
    for the data. Then call a function that asks the user what to do.
    """
    retrieved_files_list = []
    for source, dest, text in general_data:
        if not text:
            # EAFP code. Needed for testing.
            continue
        try:
            dl_fname, dl_hash, extras = get_word_from_google(text, language)
        except:
            # pass
            # Test: crash and burn
            raise
        else:
            retrieved_files_list.append(
                (source, dest, text, dl_fname, dl_hash, extras))
    for source, dest, kanji, kana in japanese_data:
        if not kanji and not kana:
            continue
        # testing: Catch only known problems here. Otherwise crash and
        # burn. Seeing the impact site is helpful.
        try:
            dl_fname, dl_hash, extras = get_word_from_jpod(kanji, kana)
        except ValueError as ve:
            if "blacklist" in str(ve):
                print 'Caught blacklist'
                continue
            raise
        # This text may be a bit ugly. Never mind. It's just for display
        if kanji != kana:
            text = u'{0} ({1})'.format(kanji,kana)
        else:
            text = kanji
        retrieved_files_list.append(
            (source, dest, text, dl_fname, dl_hash, extras))
    if retrieved_files_list:
        store_or_blacklist(note, retrieved_files_list)


def download_for_side():
    """
    Download audio for one side.

    Download audio for all audio fields on the currently visible card
    side.
    """
    card = mw.reviewer.card
    if not card:
        return
    note = card.note()
    general_field_data = get_side_fields(card, note)
    if "japanese" in note.model()['name'].lower():
        japanese_field_data = get_side_fields(card, note, japanese=True)
    else:
        japanese_field_data = []
    download_fields(note, general_field_data, japanese_field_data,
                    get_language_code(card))

def download_for_note(ask_user=False):
    """Download for all audio on the current card."""
    note = mw.reviewer.card.note()
    if not note:
        return
    general_field_data = get_note_fields(note)
    if "japanese" in note.model()['name'].lower():
        japanese_field_data = get_note_fields(note, japanese=True)
    else:
        japanese_field_data = []
    language_code = get_language_code(note)
    if ask_user:
        general_field_data, japanese_field_data, language_code = \
            update_data(general_field_data, japanese_field_data,
                        language_code)
    download_fields(note, general_field_data, japanese_field_data,
                    language_code)

def download_manual():
    download_for_note(ask_user=True)


def download_off():
    mw.note_download_action.setEnabled(False)
    mw.side_download_action.setEnabled(False)
    mw.manual_download_action.setEnabled(False)

def download_on():
    mw.note_download_action.setEnabled(True)
    mw.side_download_action.setEnabled(True)
    mw.manual_download_action.setEnabled(True)


mw.note_download_action = QAction(mw)
mw.note_download_action.setText(u"Note audio")
mw.note_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_note_audio.png')))
mw.note_download_action.setToolTip("Download audio for all audio fields " + \
                                "of this note.")
mw.connect(mw.note_download_action, SIGNAL("triggered()"), download_for_note)

mw.side_download_action = QAction(mw)
mw.side_download_action.setText(u"Side audio")
mw.side_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_side_audio.png')))
mw.side_download_action.setToolTip("Download audio for audio fields " + \
                                "currently visible.")
mw.connect(mw.side_download_action, SIGNAL("triggered()"), download_for_side)

mw.manual_download_action = QAction(mw)
mw.manual_download_action.setText(u"Manual audio")
mw.manual_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_audio_manual.png')))
mw.manual_download_action.setToolTip("Download audio, " + \
                                "editing the information first.")
mw.connect(mw.manual_download_action, SIGNAL("triggered()"), download_manual)


mw.form.menuTools.addAction(mw.note_download_action)
mw.form.menuTools.addAction(mw.side_download_action)
mw.form.menuTools.addAction(mw.manual_download_action)

# Todo: switch off at start and on when we get to reviewing.
# # And start with the acitons off.
# download_off()
