# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
import os

from .exists import free_media_name


class AudioMover(AudioProcessor):

    def __init__(self):
        # Just pro forma
        AudioProcessor.__init__(self)

    def process_and_move(self, in_name, base_name):
        """
        Copy content of temp_file_name to a file in the media directory.

        Copy content of temp_file_name to a file in the media directory
        with a name based on . media_base_name and suffix.
        """
        # (This is the ex-unmunge_to_mediafile)
        suffix = os.path.splitext(in_name)[1]
        mdir = mw.col.media.dir()
        media_file_name = free_media_name(base_name, suffix)
        with open(temp_file_name, "rb") as tfile:
            with open(os.path.join(mdir, media_file_name), 'wb') as mfile:
                mfile.write(tfile.read())
        os.remove(in_name)
        return media_file_name
