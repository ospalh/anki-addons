# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

u"""
Class to move audio files from point a to point b.
"""

import os

from .audio_processor import AudioProcessor


class AudioMover(AudioProcessor):
    u"""
    Class to move audio files from point a to point b.

    The point is that this has the same interface as the
    AudoNormaliser that does something useful.
    """

    def __init__(self):
        # Sets up that this is actually sort-of useless. (The point of
        # this class is that we have AudioNormaliser, that may or may
        # not work.)
        AudioProcessor.__init__(self)

    def process_and_move(self, in_name, base_name):
        """
        Copy content of temp_file_name to a file in the media directory.

        Copy content of temp_file_name to a file in the media directory
        with a name based on . media_base_name and suffix.
        """
        suffix = os.path.splitext(in_name)[1]
        self.unmunge_to_mediafile(in_name, base_name, suffix)
