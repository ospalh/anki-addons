# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
Anki 2 add-on that changes the way sound and videos are played.
"""

import copy
import os
import re
import subprocess
import sys

from anki.sound import playFromText, play
from aqt import utils, reviewer

__version__ = "1.1.2"
sound_re = '\[sound:(.*?)\]'
command_list = ['mplayer', '-really-quiet']

fse = sys.getfilesystemencoding()

def patched_play_from_text(text):
    matches = re.findall(sound_re, text)
    if not matches:
        # Avoid any problems with calling the programs with zero
        # files.
        return
    matches = [mtch.encode(fse) for mtch in matches]
    if command_list:
            play_with_mplayer(matches)
            return
    # Still here: no command list. I guess we didn't find
    # mplayer. Good luck playing it with play...
    for match in matches:
        play(match)


def play_with_mplayer(files):
    # We don't do the file name fixing. The point of this is to play
    # it quickly. When there is no easy way to do it on Windows, than
    # remove this add-on. So, just throw the names at mplayer.
    tmp_play_list = copy.copy(command_list)
    tmp_play_list.extend(files)
    try:
        subprocess.Popen(tmp_play_list,
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


def find_mplayer():
    """
    Try to find mplayer

    Look if we have mplayer. Fix it by adding an .exe on
    windows first. Clear the commands when we don't have one.
    """
    global command_list
    if command_list:
        if sys.platform.startswith("win32"):
            command_list[0] += '.exe'
        if not which(command_list[0]):
            # Complain,
            warn_string = u'''Replay with mplayer add-on: Could not find {0} \
in path. Please download and install it.'''
            utils.showWarning(warn_string.format(command_list[0]))
            # and clear the list
            command_list = None


# We don't really need the old_play_from_text. We have copied the
# central point of the old, the findall. Anyway.
old_play_from_text = playFromText
playFromText = patched_play_from_text

# One more monkey patch. The reviewer loads the playFromText before we
# get to it.
reviewer.playFromText = patched_play_from_text

find_mplayer()
