#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Anki2 add-on to download pronunciations.

This add-on downloads pronunciations from a number of sites
Japanese-pod: This looks for a field called reading(*) and tries to
              get a pronunciation from the languagepod website. As the
              name suggests, these are only Japanese words. The
              pronunciations that are there are rather high-quality,
              though.

Google TTS: Get pronunciations from the Google Text-To-Speech
            service. These are robot voices, so be a bit suspicous
            about them. Can speak whole sentences.
Merriam-Webster: American English. Just single words.
BeoLingus: Planned. May download English, German and Spanish words.

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

import os
from PyQt4.QtGui import QAction, QIcon, QMenu
from PyQt4.QtCore import SIGNAL

from aqt import mw
from aqt.utils import tooltip
from anki.hooks import addHook

from .blacklist import get_hash
from .downloaders import downloaders
from .get_fields import get_note_fields, get_side_fields
from .language import get_language_code
from .processors import processor
from .review_gui import store_or_blacklist
from .update_gui import update_data


icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')
"""Place were we keep our megaphone icon.."""

# A bit of set-up
for downloader in downloaders:
    # We have two audio "processors". One that is actually processing,
    # and one where we would have to move files around, but where we
    # can skip that step. Let the downloaders know which one we have.
    downloader.use_temp_files = processor.useful


def do_download(note, field_data, language):
    """
    Download audio data.

    Go through the list of words and list of sites and download each
    word from each site. Then call a function that asks the user what
    to do.
    """
    retrieved_files_list = []
    for (source, dest, text, base, ruby, dummy_split) in field_data:
        for downloader in downloaders:
            # Use a public variable to set the language.
            downloader.language = language
            try:
                # Make it easer inside the downloader. If anything
                # goes wrong, don't catch or rais whatever you want.
                downloader.download_files(text, base, ruby)
            except:
                # Uncomment this raise while testing new downloaders.
                # raise
                continue
            for word_path, file_name, extras in downloader.downloads_list:
                try:
                    item_hash = get_hash(word_path)
                except ValueError:
                    # Now the downloader downloads, doesn't remove
                    # files with bad hashes. So do it here.
                    # print 'bad hash'
                    os.remove(word_path)
                    continue
                if processor.useful:
                    # if not processor.useful we write directly to the
                    # media dir.
                    try:
                        # Dto. audio processing/file moving. The
                        # downloader downloads to a temp file, so move
                        # here.
                        file_name = processor.process_and_move(
                            word_path, downloader.base_name)
                    except Exception:
                        raise
                        os.remove(word_path)
                        continue
                # else:
                #    file_name = file_name
                # We pass the file name around for this case.
                retrieved_files_list.append((
                    source, dest, downloader.display_text,
                    file_name, item_hash, extras, downloader.site_icon))
    try:
        store_or_blacklist(note, retrieved_files_list)
    except ValueError as ve:
        tooltip(str(ve))
    except RuntimeError as rte:
        if not 'cancel' in str(rte):
            raise
        # else: quietly drop out on user cancel


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
    field_data = get_side_fields(card, note)
    do_download(note, field_data, get_language_code(card))


def download_for_note(note=False, ask_user=False):
    """
    Download audio for all fields.

    Download audio for all fields of the note passed in or the current
    note. When ask_user is true, show a dialog that lets the user
    modify these texts.
    """
    card = None
    if not note:
        try:
            card = mw.reviewer.card
            note = card.note()
        except:
            return
    field_data = get_note_fields(note, get_empty=ask_user)
    language_code = get_language_code(card=card, note=note)
    if ask_user:
        try:
            field_data, language_code = update_data(field_data, language_code)
        except RuntimeError as rte:
            if 'cancel' in str(rte):
                # User canceled. No need for the "Nothing downloaded"
                # message.
                return
            else:
                # Don't know how to handle this after all
                raise
    do_download(note, field_data, language_code)


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


def editor_download_editing(self):
    self.saveNow()
    download_for_note(ask_user=True, note=self.note)
    self.loadNote()


def editor_add_download_editing_button(self):
    """Add the download button to the editor"""
    dl_button = self._addButton("download_audio",
                                lambda self=self:
                                    editor_download_editing(self),
                                tip=u"Download audio...", text=" ")
    dl_button.setIcon(QIcon(os.path.join(icons_dir,
                                         'download_note_audio.png')))


# Either reuse an edit-media sub-menu created by another add-on
# (probably by Y.T., notably the external edit add-on that is in the
# works) or create that menu. When we already have that menu, add a
# separator, otherwise create that menu.
try:
    mw.edit_media_submenu.addSeparator()
except AttributeError:
    mw.edit_media_submenu = QMenu(u"&Media", mw)
    mw.form.menuEdit.addSeparator()
    mw.form.menuEdit.addMenu(mw.edit_media_submenu)


mw.note_download_action = QAction(mw)
mw.note_download_action.setText(u"Note audio")
mw.note_download_action.setIcon(QIcon(os.path.join(icons_dir,
                                                   'download_note_audio.png')))
mw.note_download_action.setToolTip(
    "Download audio for all audio fields of this note.")
mw.connect(mw.note_download_action, SIGNAL("triggered()"), download_for_note)

mw.side_download_action = QAction(mw)
mw.side_download_action.setText(u"Side audio")
mw.side_download_action.setIcon(
    QIcon(os.path.join(icons_dir, 'download_side_audio.png')))
mw.side_download_action.setToolTip(
    "Download audio for audio fields currently visible.")
mw.connect(mw.side_download_action, SIGNAL("triggered()"), download_for_side)

mw.manual_download_action = QAction(mw)
mw.manual_download_action.setText(u"Manual audio")
mw.manual_download_action.setIcon(
    QIcon(os.path.join(icons_dir, 'download_audio_manual.png')))
mw.manual_download_action.setToolTip(
    "Download audio, editing the information first.")
mw.connect(mw.manual_download_action, SIGNAL("triggered()"), download_manual)


mw.edit_media_submenu.addAction(mw.note_download_action)
mw.edit_media_submenu.addAction(mw.side_download_action)
mw.edit_media_submenu.addAction(mw.manual_download_action)

# Todo: switch off at start and on when we get to reviewing.
# # And start with the acitons off.
# download_off()


addHook("setupEditorButtons", editor_add_download_editing_button)
