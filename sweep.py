# -*- mode: Python ; coding: utf-8 -*-
# © 2012–3: Roland Sieker <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
Anki 2 add-on that opens sweep to edit the audio files.
"""

import copy
import os
import re
import subprocess
import sys

from aqt import utils
from aqt import mw
from PyQt4.QtGui import QAction, QIcon, QMenu
from PyQt4.QtCore import SIGNAL

__version__ = "1.1.0"

sound_re = ur'\[sound:(.*?)\]'

command_list = ['sweep-audio-editor']
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


def sweep_files(note):
    """
    Call sweep with all sounds from the note.
    """
    # First, join all fields. Use some random field delimiter. (Could
    # be '', i guess.) EAFP, raise stuff when we don't have a note.
    text = '@'.join(note.fields)
    matches = [fn for fn in re.findall(sound_re, text) if sound_ending(fn)]
    if command_list and matches:
        call_sweep(matches)


def call_sweep(files):
    u"""Start the programme sweep to edit files."""
    # We don't do the file name fixing. The point of this is to edit
    # the files in place. I don't think there is a sweep version for
    # windows. Maybe for cygwin. As this is a quick hack for me, i
    # don't really mind.
    tmp_sweep_list = copy.copy(command_list)
    tmp_sweep_list.extend(files)
    try:
        subprocess.Popen(tmp_sweep_list,
                         shell=False, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         close_fds=True)
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


def find_sweep():
    """
    Try to find sweep

    Look if we have sweep. Fix it by adding an .exe on
    windows first. Clear the commands when we don't have one.
    """
    global command_list
    if command_list:
        if sys.platform.startswith("win32"):
            command_list[0] += '.exe'
        if not which(command_list[0]):
            # Complain,
            warn_string = u'''Replay with sweep add-on: Could not find {0} \
in path. Please download and install it.'''
            utils.showWarning(warn_string.format(command_list[0]))
            # and clear the list
            command_list = None
    return command_list


def sweep_current_note():
    u"""Call the action to edit the sound files of the current note."""
    try:
        sweep_files(mw.reviewer.card.note())
    except AttributeError:
        # No note.
        pass


if find_sweep():
    # Either reuse an edit-media sub-menu created by another add-on
    # (probably by Y.T., notably the download audio add-on) r create
    # that menu. When we already have that menu, add a separator,
    # otherwise create that menu.
    try:
        mw.edit_media_submenu.addSeparator()
    except AttributeError:
        mw.edit_media_submenu = QMenu(u"&Media", mw)
        mw.form.menuEdit.addSeparator()
        mw.form.menuEdit.addMenu(mw.edit_media_submenu)
    # Now add to that menu
    mw.sweep_audio_fiels_action = QAction(mw)
    mw.sweep_audio_fiels_action.setText(u"Edit audio")
    icons_dir = os.path.join(mw.pm.addonFolder(), 'color_icons')
    try:
        # Bad hack. Use the icon brought along from another add-on and
        # nicked from the program we use. That program is GPLed, so we
        # should be OK with that.
        mw.sweep_audio_fiels_action.setIcon(
            QIcon(os.path.join(icons_dir, 'scrubby.xpm')))
    except:
        pass
    mw.sweep_audio_fiels_action.setToolTip(
        "Edit audio files of the current note with sweep-audio-editor.")
    mw.connect(mw.sweep_audio_fiels_action, SIGNAL("triggered()"),
               sweep_current_note)
    mw.edit_media_submenu.addAction(mw.sweep_audio_fiels_action)
