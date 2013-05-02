# -*- mode: Python ; coding: utf-8 -*-
# © 2012–3: Roland Sieker <ospalh@gmail.com>
# Bits contributed by Yichao Zhou
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html

"""
Anki 2 add-on that changes the way sound and videos are played.
"""

import copy
import os
import re
import subprocess
import sys

from anki.sound import playFromText, play
from anki.utils import isWin
from aqt import moduleDir, utils, reviewer

__version__ = "1.2.0"

if isWin:
    # Looks like we should use these to hide the CMD/shell
    # window. From a patch by Yichao Zhou. Thanks.
    subprocess.STARTUPINFO.wShowWindow = subprocess.SW_HIDE
    subprocess.STARTUPINFO.dwFlags = subprocess.STARTF_USESHOWWINDOW

sound_re = ur'\[sound:(.*?)\]'
command_list = ['mplayer', '-really-quiet']
if isWin:
    command_list += ['-ao', 'win32']

fse = sys.getfilesystemencoding()

def patched_play_from_text(text):
    u"""Play the list of files directly without play queue."""
    matches = re.findall(sound_re, text)
    if not matches:
        # Avoid any problems with calling the programs with zero
        # files.
        return
    matches = [mtch.encode(fse) for mtch in matches]
    if command_list:
        play_with_mplayer(matches)
    else:
        # No command list. I guess we didn't find mplayer. Good luck
        # playing it with play...
        for match in matches:
            play(match)


def play_with_mplayer(files):
    """
    Play files with mplayer.

    This is the piece-de-resistance of the add-on. We take the file
    names in files an throw them at mplayer, without using the audio
    queue. We don't do the file name fixing, either.. The point of
    this is to play it quickly. There have been a few additions so
    presumably it works on windows now.
    """
    tmp_play_list = copy.copy(command_list) + files
    if isWin:
        subprocess.Popen(
            tmp_play_list, shell=False, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=False)
    else:
        try:
            subprocess.Popen(
                tmp_play_list, shell=False, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        except OSError:
            # On Macs, we get ‘Interruppted system call’s. Just
            # ignore, like anki’s sound module does.
            pass


def which(program):
    """
    Return path of command.

    Return path of command program. We add the path of Anki because
    the binary install brings along an mplayer of its own.
    """
    def is_exe(fpath):
        u"""Return whether fpath is executable."""
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname_dummy = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep) + [moduleDir, ]:
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def find_mplayer():
    """
    Try to find mplayer

    Look if we have mplayer. Fix it by adding an .exe on windows first. Clear
    the commands when we don't have one.
    """
    global command_list
    if command_list:
        if isWin:
            command_list[0] += '.exe'
        if not which(command_list[0]):
            # Complain,
            warn_string = u'''Quick replay add-on: Could not find {0} \
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
