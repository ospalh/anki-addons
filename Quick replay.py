# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
Anki 2 add-on to play sound with mpg321 or play (sox).
"""

import copy
import os
import re
import subprocess
import sys
import tempfile

from anki.sound import playFromText
from aqt import utils, reviewer

sound_re = '\[sound:(.*?)\]'

# mp3_command_list = ['mpg123'  '-q', '-b 4m']
mp3_command_list = ['mpg321',  '-q', '-b 4m', '--stereo']
play_command_list = ['play', '-q']
play_endings_list = ['.ogg', '.flac']


def patched_play_from_text(text):
    matches = re.findall(sound_re, text)
    if not matches:
        # Avoid any problems with calling the programs with zero
        # files.
        return
    # Check if we have mpg321
    if mp3_command_list:
        # Isolate the mp3s. Play with our command if that is all the
        # sounds.
        mp3_files = [mp for mp in matches if mp.lower().endswith('.mp3')]
        if len(mp3_files) == len(matches):
            play_with_mpg321(mp3_files)
            return
    # The same for ogg and flac
    if play_command_list:
        play_files = [pf for pf in matches \
                          for ending in play_endings_list \
                          if pf.lower().endswith(ending)]
        if len(play_files) == len(matches):
            play_with_play(play_files)
            return
    # Still here, neither all mp3 nor all playable with play. The
    # classical sound.play.
    for match in matches:
        sound.play(match)


def play_with_mpg321(files):
    # We don't do the file name fixing. The point of this is to play
    # it quickly. When there is no easy way to do it on Windows, than
    # remove this add-on. So, just throw the names at mpg321.
    tmp_play_list = copy.copy(mp3_command_list)
    tmp_play_list.extend(files)
    try:
        subprocess.Popen(tmp_play_list,
                         shell=False, stdin=None, stdout=None,
                         stderr=None,close_fds=True)
    except OSError:
        # On Macs, we get ‘Interruppted system call’s. Just
        # ignore, like anki’s sound module does.
        pass

def play_with_play(files):
    # The same, only use other command name.
    tmp_play_list = copy.copy(play_command_list)
    tmp_play_list.extend(files)
    try:
        subprocess.Popen(tmp_play_list,
                         shell=False, stdin=None, stdout=None,
                         stderr=None,close_fds=True)
    except OSError:
        pass


def which(program):
    """Return path of command."""
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def fix_commands():
    """
    Try to find the play commands.

    Look if we have mpg321 and play. Fix it by adding an .exe on
    windows first. Clear the commands when we don't have one.
    """
    global mp3_command_list
    global play_command_list
    if mp3_command_list:
        if sys.platform.startswith("win32"):
            mp3_command_list[0] += '.exe'
        if not which(mp3_command_list[0]):
            # Complain,
            utils.showWarning(u'Quick replay add-on: Could not find {} '\
                                  'in path. Please download and install it.'
                              .format(mp3_command_list[0]))
            # and clear the list
            mp3_command_list = None
    if play_command_list:
        if sys.platform.startswith("win32"):
            play_command_list[0] += '.exe'
        if not which(play_command_list[0]):
            # Complain,
            utils.showWarning(u'Quick replay add-on:: Could not find {} '\
                                  'in path. Please download and install it.'
                              .format(play_command_list[0]))
            # and clear the list
            play_command_list = None
        

# We don't really need the old_play_from_text. We have copied the
# central point of the old, the findall. Anyway.

old_play_from_text = playFromText
playFromText = patched_play_from_text

# One more monkey patch. The reviewer loads the playFromText before we
# get to it.
reviewer.playFromText = patched_play_from_text

fix_commands()
