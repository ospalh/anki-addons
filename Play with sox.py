# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""A simple plugin that throws ogg and flac files at sox to play,
rather than let them through to the mplayer, which, at least on
windows, can’t handle them.
"""

import sys, os, subprocess, tempfile

from anki import sound
from anki.hooks import addHook

## Just play flac, ogg, vorbis with sox:
fileFormatsToSox = ['.ogg', '.flac', '.vorbis']

## These are the ‘AUDIO FILE FORMATS’ the sox.exe of the windows anki
## install knows about, with a ‘.’ added. Use this list instead or add
## to the list above, to taste. You may want to exclude mp3, wav, from
## the list, because mplayer can handle those.
#fileFormatsToSox = \
#    ['.8svx', '.aif', '.aifc', '.aiff', '.aiffc', '.al', '.amb', '.amr-nb',\
#         '.amr-wb', '.anb', '.au', '.avr', '.awb', '.caf', '.cdda', '.cdr',\
#         '.cvs', '.cvsd', '.cvu', '.dat', '.dvms', '.f32', '.f4', '.f64',\
#         '.f8', '.fap', '.flac', '.fssd', '.gsm', '.gsrt', '.hcom', '.htk',\
#         '.ima',\ '.ircam', '.la', '.lpc', '.lpc10', '.lu', '.mat',\
#         '.mat4', '.mat5', '.maud', '.mp2', '.mp3', '.nist', '.ogg', '.paf',\
#         '.prc', '.pvf', '.raw', '.s1', '.s16', '.s2', '.s24', '.s3', '.s32',\
#         '.s4', '.s8', '.sb', '.sd2', '.sds', '.sf', '.sl', '.smp', '.snd',\
#         '.sndfile', '.sndr', '.sndt', '.sou', '.sox', '.sph', '.sw', '.txw',\
#         '.u1', '.u16', '.u2', '.u24', '.u3', '.u32', '.u4', '.u8', '.ub',\
#         '.ul', '.uw', '.vms', '.voc', '.vorbis', '.vox', '.w64', '.wav',\
#         '.wavpcm', '.wv', '.wve', '.xa', '.xi']



soxBaseName = u'sox'
oldPlay = sound.play


DETACHED_PROCESS = 0x00000008

def soxyEnding(fname):
    for ffts in fileFormatsToSox:
        if fname.endswith(ffts):
            return ffts
    return None


def playSomeSoundsWithSox(path):
    if not soxBaseName:
        oldPlay(path)
        return
    fending = soxyEnding(path)
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
            subprocess.Popen([soxBaseName, "-q", tname, "-d"],
                             shell=False, stdin=None, stdout=None,
                             stderr=None, close_fds=True)
            os.remove(tname)
        else:
            try:
                subprocess.Popen([soxBaseName, "-q", path, "-d"],
                                 shell=False, stdin=None, stdout=None,
                                 stderr=None,close_fds=True)
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


def findSox():
    global soxBaseName
    if sys.platform.startswith("win32"):
        soxBaseName += '.exe'
    soxPath = which(soxBaseName)
    if not soxPath:
        # set the base name to empty, used as a test later
        soxBaseName = None
        # and complain.
        utils.showInfo(u'Play with sox plugin: Could not find sox in path. Please download and install it.')

sound.play = playSomeSoundsWithSox




addHook("init", findSox)
