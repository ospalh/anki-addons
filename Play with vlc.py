# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
Anki 2 add-on that throws media at vlc instead of mplayer.
"""

import copy
import os
import re
import subprocess
import sys

from anki.sound import playFromText, play
from aqt import utils, reviewer

__version__ = "1.0.1"

sound_re = '\[sound:(.*?)\]'

command_list = [
    'vlc',  # The program. Munged to the path on startup
    '-Idummy',  # Interface: no gui.
    '--play-and-exit'  # Pretty much says it
    ]


def patched_play_from_text(text):
    matches = re.findall(sound_re, text)
    if not matches:
        # Avoid any problems with calling the programs with zero
        # files.
        return
    if command_list:
            play_with_vlc(matches)
            return
    # Still here, neither all mp3 nor all playable with play. The
    # classical sound.play.
    for match in matches:
        play(match)


def play_with_vlc(files):
    # We don't do the file name fixing. The point of this is to play
    # it quickly. When there is no easy way to do it on Windows, than
    # remove this add-on. So, just throw the names at vlc.
    tmp_play_list = copy.copy(command_list)
    tmp_play_list.extend(files)
    print 'playing ', str(tmp_play_list)
    try:
        subprocess.Popen(tmp_play_list,
                         shell=False, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
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


def find_vlc():
    """
    Try to find vlc

    Look if we have vlc. Fix it by adding an .exe on
    windows first. Clear the commands when we don't have one.
    """
    global command_list
    if command_list:
        if sys.platform.startswith("win32"):
            command_list[0] += '.exe'
        if not which(command_list[0]):
            # Complain,
            warn_string = u'Replay with vlc add-on: Could not find {} ' \
                + u'in path. Please download and install it.'
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

find_vlc()
