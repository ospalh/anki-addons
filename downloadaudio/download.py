# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–16 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
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

from .downloaders import downloaders
from .download_entry import DownloadEntry, Action
from .get_fields import get_note_fields, get_side_fields
from .language import language_code_from_card, language_code_from_editor
from .processors import processor
from .review_gui import review_entries
from .update_gui import update_data

DOWNLOAD_NOTE_SHORTCUT = "q"
DOWNLOAD_SIDE_SHORTCUT = "t"
DOWNLOAD_MANUAL_SHORTCUT = "Ctrl+t"

icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')
# Place were we keep our megaphone icon.


def do_download(note, field_data_list, language, hide_text=False):
    """
    Download audio data.

    Go through the list of words and list of sites and download each
    word from each site. Then call a function that asks the user what
    to do.
    """
    retrieved_entries = []
    for field_data in field_data_list:
        if field_data.empty:
            continue
        for dloader in downloaders:
            # Use a public variable to set the language.
            dloader.language = language
            try:
                # Make it easer inside the downloader. If anything
                # goes wrong, don't catch, or raise whatever you want.
                dloader.download_files(field_data)
            except:
                #  # Uncomment this raise while testing a new
                #  # downloaders.  Also use the “For testing”
                #  # downloaders list with your downloader in
                #  # downloaders.__init__
                # raise
                continue
            retrieved_entries += dloader.downloads_list
    # Significantly changed the logic. Put all entries in one
    # list, do stuff with that list of DownloadEntries.
    for entry in retrieved_entries:
        # Do the processing before the reviewing now.
        entry.process()
    try:
        retrieved_entries = review_entries(note, retrieved_entries, hide_text)
        # Now just the dialog, which sets the fields in the entries
    except ValueError as ve:
        tooltip(str(ve))
    except RuntimeError as rte:
        if 'cancel' in str(rte):
            for entry in retrieved_entries:
                entry.action = Action.Delete
        else:
            raise
    for entry in retrieved_entries:
        entry.dispatch(note)
    if any(entry.action == Action.Add for entry in retrieved_entries):
        note.flush()
        # We have to do different things here, for download during
        # review, we should reload the card and replay. When we are in
        # the add dialog, we do a field update there.
        rnote = None
        try:
            rnote = mw.reviewer.card.note()
        except AttributeError:
            # Could not get the note of the reviewer's card. Probably
            # not reviewing at all.
            return
        if note == rnote:
            # The note we have is the one we were reviewing, so,
            # reload and replay
            mw.reviewer.card.load()
            mw.reviewer.replayAudio()


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
    do_download(
        note, field_data, language_code_from_card(card), hide_text=True)


def download_for_note(ask_user=False, note=None, editor=None):
    """
    Download audio for all fields.

    Download audio for all fields of the note passed in or the current
    note. When ask_user is true, show a dialog that lets the user
    modify these texts.
    """
    if not note:
        try:
            card = mw.reviewer.card
            note = card.note()
        except AttributeError:
            return
        language_code = language_code_from_card(card)
    else:
        language_code = language_code_from_editor(note, editor)
    field_data = get_note_fields(note)
    if not field_data:
        # Complain before we show the empty dialog.
        tooltip(u'Nothing to download.')
        return

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
    u"""Do the download with the dialog before we go."""
    download_for_note(ask_user=True)


def download_off():
    u"""Deactivate the download menus."""
    mw.note_download_action.setEnabled(False)
    mw.side_download_action.setEnabled(False)
    mw.manual_download_action.setEnabled(False)


def download_on():
    u"""Activate the download menus."""
    mw.note_download_action.setEnabled(True)
    mw.side_download_action.setEnabled(True)
    mw.manual_download_action.setEnabled(True)


def editor_download_editing(self):
    u"""Do the download when we are in the note editor."""
    self.saveNow()
    download_for_note(ask_user=True, note=self.note, editor=self)
    # Fix for issue #10.
    self.stealFocus = True
    self.loadNote()
    self.stealFocus = False


def editor_add_download_editing_button(self):
    """Add the download button to the editor"""
    dl_button = self._addButton(
        "download_audio",
        lambda self=self: editor_download_editing(self),
        tip=u"Download audio…")
    dl_button.setIcon(
        QIcon(os.path.join(icons_dir, 'download_note_audio.png')))


# Either reuse an edit-media sub-menu created by another add-on
# (probably the mhwave (ex sweep) add-on by Y.T.) or create that
# menu. When we already have that menu, add a separator, otherwise
# create that menu.
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
mw.note_download_action.setShortcut(DOWNLOAD_NOTE_SHORTCUT)
mw.connect(mw.note_download_action, SIGNAL("triggered()"), download_for_note)

mw.side_download_action = QAction(mw)
mw.side_download_action.setText(u"Side audio")
mw.side_download_action.setIcon(
    QIcon(os.path.join(icons_dir, 'download_side_audio.png')))
mw.side_download_action.setToolTip(
    "Download audio for audio fields currently visible.")
mw.side_download_action.setShortcut(DOWNLOAD_SIDE_SHORTCUT)
mw.connect(mw.side_download_action, SIGNAL("triggered()"), download_for_side)

mw.manual_download_action = QAction(mw)
mw.manual_download_action.setText(u"Manual audio")
mw.manual_download_action.setIcon(
    QIcon(os.path.join(icons_dir, 'download_audio_manual.png')))
mw.manual_download_action.setToolTip(
    "Download audio, editing the information first.")
mw.manual_download_action.setShortcut(DOWNLOAD_MANUAL_SHORTCUT)
mw.connect(mw.manual_download_action, SIGNAL("triggered()"), download_manual)


mw.edit_media_submenu.addAction(mw.note_download_action)
mw.edit_media_submenu.addAction(mw.side_download_action)
mw.edit_media_submenu.addAction(mw.manual_download_action)

# Todo: switch off at start and on when we get to reviewing.
# # And start with the acitons off.
# download_off()


addHook("setupEditorButtons", editor_add_download_editing_button)
