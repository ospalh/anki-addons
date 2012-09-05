#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
from aqt import mw
from anki.card import Card
from anki.note import Note
from anki.hooks import addHook

from forvo import get_word_from_forvo
from google_tts import get_word_from_google
from japansepod  import get_word_from_jpod

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


# Change this at your own risk.
field_name_re = '{{(?:[/^#]|[^:}]+:|)([^:}{]*%s[^:}{]*)}}'


def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes

def candidate_field_names(fname, readings=False):
    """
    Return a list of candidate source field names derived from fname.

    When fname does not contain any string from audio_field_keys, an
    empty list is returned.

    There are four ways the candidate name is generated:
    * readings is False:
      * when fname is in one of the strings is audio_field_key,
        expression_fields is used as list of candidates
      * when the audio_field_key is only a substring, that substring
        and a trailing or leading ' ' or '_' is removed and that used
        as the candidate
    * readings is False:
      * when fname is in one of the strings is audio_field_key,
        japanese_reading_keys is used as list of candidates
      * when the audio_field_key is only a substring, that substring
        is replaced by the strings from japanese_reading_keys
    """
    fname = fname.lower()
    candidate_names = []
    for afk in audio_field_keys:
        if fname == afk:
            if reading:
                return japanese_reading_keys
            else:
                return expression_fields
        if not afk in fname:
            Continue
        todo # do the replacing described above




def fids_for_name(fname, readings=False):
    """
    Return a pair of field ids for fname.

    Return a pair of field ids when a field named fname is found in
    the current card's model and when a suitable field to get the text
    for the download from is found. When either of these fields is not
    found, a KeyError is raised. A KeyError is also raised when no
    string from audio_field_key is found in fname.

    The 'suitable' field is determined by another function.
    """
    audio_fid = fid_for_name(fname)
    candidates = candidate_field_names(fname, readings)
    for candidate in  candidates:
        try:
            source_fid = fid_for_name(candidate)
        except KeyError as ke:
            continue
        return (audio_fid, source_fid)
    # Still here. Either no candidate name at all or no field found
    # for any.
    raise KeyError("No source field found.")

def get_side_fields(japanese=False):
    """
    Get a list of field ids for "visible" download fields.

    Check the visible side of the current card for fields that contain
    a string from audio_field_keys.
    Then check the
    """
    try:
        card = mw.reviewer.card
    except:
        return []
    if not card:
        return []
    if 'question' == mw.reviewer.state:
        template = card.template()[u'qfmt']
    else:
        template = card.template()[u'afmt']
    field_name_list = []
    for afk in audio_field_keys:
        # Append all fields in the current template/side that contain
        # 'audio' or 'sound'
        field_name_list.append(re.findall(field_name_re % (afk, ), template,
                                   flags=re.IGNORECASE))
    field_name_list = uniqify_list(field_name_list)
    field_ids_list = []
    for fname in field_ids_list:
        try:
            field_ids_list.append(fids_for_name(fname, readings=japanese))
        except KeyError:
            pass
    return field_ids_list



def get_note_fields(note, japanese=False):
    return []



def download_for_side():
    card = mw.reviewer.card
    if not card:
        return
    general_fields = get_fields(card=card)
    japanese_fields = get_fields(card=card, japanese=True)

def download_for_note():
    note = mw.reviewer.card.note()
    if not note:
        return
    general_fields = get_general_fields(note=note)
    japanese_fields = get_japanese_fields(note=note, japanese=True)


def question_state():
    note_download_action.setEnabled(False)

def question_state():
    note_download_action.setEnabled(True)


note_download_action = QAction(mw)
note_download_action.setText(u"Note audio.")
note_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                'download_note_audio.png')))
note_download_action.setToolTip("Download audio for all audio fields " + \
                                "of this note.")
mw.connect(note_download_action, SIGNAL("triggered()"), download_for_note)


if hide_download_not_on_question:
    addHook('showQuestion' question_state)
    addHook('showAnswer', answer_state)
