# -*- mode: Python ; coding: utf-8 -*-
# © 2012–2016 Roland Sieker <ospalh@gmail.com>
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
u"""Anki 2 add-on that opens an audio editor."""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QIcon, QMenu
import copy
import os
import re
import subprocess
import sys

from anki.hooks import addHook
from aqt import mw, utils
from aqt.editor import Editor

__version__ = "2.0.0"

sound_re = ur'\[sound:(.*?)\]'

command_list = ['mhwaveedit']
sound_ending_list = ['.mp3', '.wav', '.flac', '.ogg']


def sound_ending(fname):
    u"""
    Return the sound-file-like ending of fname or None.

    Check whether fname looks like the name of a sound file and return
    the file ending if it does or None if it doesn’t.
    """
    for ffts in sound_ending_list:
        if fname.lower().endswith(ffts):
            return ffts
    return None


def edit_files(note=None, text=None):
    u"""Edit files of a note or for a given text

    Call the audio editor with all sounds from the note, or for a given
    text"""
    # First, join all fields. Use some random field delimiter. (Could
    # be '', i guess.) EAFP, raise stuff when we don't have a note.
    if text is None:
        try:
            text = '@'.join(note.fields)
        except AttributeError:
            # Maybe we don’t have a note
            print('debug: editfiles w/o note')
            return
    matches = [fn for fn in re.findall(sound_re, text) if sound_ending(fn)]
    if command_list and matches:
        call_edit(matches)


def call_edit(files):
    u"""Start the audio editor to edit files."""
    # We don't do the file name fixing. The point of this is to edit
    # the files in place.
    tmp_edit_list = copy.copy(command_list)
    tmp_edit_list.extend(files)
    try:
        subprocess.Popen(
            tmp_edit_list, shell=False, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    except OSError:
        # On Macs, we get ‘Interruppted system call’s. Just
        # ignore, like anki’s sound module does.
        pass


def which(program):
    """Return path of command."""
    def is_exe(fpath):
        u"""Return whether fpath points to an executable file."""
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, dummy_fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def find_editor():
    u"""Try to find the audio editor

    Look if we have the audio ediotr. Fix it by adding an .exe on
    windows first. Clear the commands when we don't have one.
    """
    global command_list
    if command_list:
        if sys.platform.startswith("win32"):
            command_list[0] += '.exe'
        if not which(command_list[0]):
            # Complain,
            warn_string = u'''Audio editor add-on: Could not find {0} \
in path. Please download and install it.'''
            utils.showWarning(warn_string.format(command_list[0]))
            # and clear the list
            command_list = None
    return command_list


def edit_current_note():
    u"""Call the action to edit the sound files of the current note."""
    try:
        edit_files(note=mw.reviewer.card.note())
    except AttributeError:
        # No note.
        pass


def edit_from_editor(editor):
    u"""Edit audio of the field currently being edited."""
    edit_files(text=editor.note.fields[editor.currentField])


def setup_button(editor):
    u"""Add the buttons to the editor."""
    editor._addButton(
        "wave_button", lambda ed=editor: edit_from_editor(ed),
        tip=u"wave", text='W')


if find_editor():
    # Either reuse an edit-media sub-menu created by another add-on
    # (probably by Y.T., notably the download audio add-on) or create
    # that menu. When we already have that menu, add a separator,
    # otherwise create that menu.
    try:
        mw.edit_media_submenu.addSeparator()
    except AttributeError:
        mw.edit_media_submenu = QMenu(u"&Media", mw)
        mw.form.menuEdit.addSeparator()
        mw.form.menuEdit.addMenu(mw.edit_media_submenu)
    # Now add to that menu
    mw.edit_audio_fiels_action = QAction(mw)
    mw.edit_audio_fiels_action.setText(u"Edit audio")
    icons_dir = os.path.join(mw.pm.addonFolder(), 'color_icons')
    addHook("setupEditorButtons", setup_button)
    try:
        # Bad hack. Use the icon brought along from another add-on and
        # nicked from the program we use. That program is GPLed, so we
        # should be OK with that.
        mw.edit_audio_fiels_action.setIcon(
            QIcon(os.path.join(icons_dir, 'mhwaveedit.png')))
    except:
        pass
    mw.edit_audio_fiels_action.setToolTip(
        "Edit audio files of the current note with mhwave.")
    mw.connect(mw.edit_audio_fiels_action, SIGNAL("triggered()"),
               edit_current_note)
    mw.edit_media_submenu.addAction(mw.edit_audio_fiels_action)
