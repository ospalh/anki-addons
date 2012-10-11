# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""A simple plugin that throws ogg and flac files at sox to play,
rather than let them through to the mplayer, which, at least on
windows, can’t handle them.
"""

import os
import subprocess
import sys
import tempfile

from anki import sound
from anki.hooks import addHook

## Just play flac, ogg, vorbis with sox:
fileFormatsToPlay = ['.mp3']

mpgBaseName = u'mpg321'
oldPlay = sound.play

DETACHED_PROCESS = 0x00000008


def mpgyEnding(fname):
    for ffts in fileFormatsToPlay:
        if fname.endswith(ffts):
            return ffts
    return None


def playSomeSoundsWithMpg(path):
    if not mpgBaseName:
        oldPlay(path)
        return
    fending = mpgyEnding(path)
    if fending:
        if sys.platform.startswith("win32"):
            # Avoid the hassle with passing non-ascii file names to
            # the shell. Idea taken from anki's sound.py, but using
            # the standard temp directory, and deleting the file after
            # play.
            (fd, tname) = tempfile.mkstemp(fending)
            try:
                # EAFP
                f = os.fdopen(fd, "wb")
                f.write(open(path, "rb").read())
            except IOError:
                # Probably no file.
                try:
                    f.close()
                    os.remove(tname)
                except:
                    pass
                return
            f.close()
            # To reduce the danger, use tepmpath
            tname = tname.encode(sys.getfilesystemencoding())
            subprocess.Popen([mpgBaseName, "-q", "-b 4m", tname],
                             shell=False, stdin=None, stdout=None,
                             stderr=None, close_fds=True)
            os.remove(tname)
        else:
            try:
                subprocess.Popen([mpgBaseName, "-q", "-b 4m", "--stereo", path],
                                 shell=False, stdin=None, stdout=None,
                                 stderr=None, close_fds=True)
            except OSError:
                # On Macs, we get ‘Interruppted system call’s. Just
                # ignore, like anki’s sound module does.
                pass
    else:
        oldPlay(path)


def which(program):
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


def findMpg():
    global mpgBaseName
    if sys.platform.startswith("win32"):
        mpgBaseName += '.exe'
    mpgPath = which(mpgBaseName)
    if not mpgPath:
        # set the base name to empty, used as a test later
        mpgBaseName = None
        # and complain.
        help_string = u'Play with mpg plugin: ' + \
            u'Could not find {} in path. Please download and install it.'
        utils.showInfo(help_string.format(mpgBaseName))

sound.play = playSomeSoundsWithMpg

addHook("init", findMpg)
