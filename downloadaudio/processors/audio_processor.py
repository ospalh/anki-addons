# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""
Move a file to the Anki2 media folder, processing it on the way when
possible.
"""

import os

from aqt import mw

from .exists import free_media_name


class AudioProcessor(object):

    def __init__(self):
        pass

    def process_and_move(self, in_name, base_name):
        """
        Make a sound file in the Anki media directory.

        Make a sound file with the sound information in in_name in the
        Anki media directory. The new name should use base_name as the
        base of the new file name.

        For typical installations, the file
        is simply moved.

        When pysox and pydub are installed, the file is normalised and
        changed to the format set in the processor (flac).
        """
        raise NotImplementedError("Use a class derived from this.")

    def unmunge_to_mediafile(self, in_name, base_name, suffix):
        mdir = mw.col.media.dir()
        media_file_name = free_media_name(base_name, suffix)
        with open(in_name, "rb") as tfile:
            with open(os.path.join(mdir, media_file_name), 'wb') as mfile:
                mfile.write(tfile.read())
        os.remove(in_name)
        return media_file_name
