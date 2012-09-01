#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

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
       use this serivec, you need to register at forvo.com and gat a
       “developer” key. The free service is limited to 1000 requests
       per day.

There are two ways to download: Current card and current note. The
current card download looks at audio field in what is currently
shown and tries to download only for those. This should limit the
information leaked before you answer a card. Current note tries to
fill all audio fields of the current note. This may reveal, that
information that you tried to remember, potentially ahead of time.
"""


## Do not download when a fact has any of these tags. (List may be empty.)
exclusion_tags = ['nodownload']
# exclusion_tags = []

## Try to not downolad things unseen:
hide_download_not_on_question = True

## Change these to mach the field names of your decks. Make sure to
## not use capital letters. We do a tolower() on the field names.
expression_fields = ['expression', 'front']
japanese_reading_keys = ["reading", "kana", u'かな',u'仮名']
audio_field_keys = ["audio", "sound"]


def get_fields(card=None, note=None, japanese=False):

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
