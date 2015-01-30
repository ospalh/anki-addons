# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2015 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

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

    def process_and_move(self, dl_entry):
        """Move temp_file_name to a file in the media directory.

        Move to a file in the media directory with a name based on the
        data in the downolad entry.
        """
        self.unmunge_to_mediafile(
            dl_entry.file_path, dl_entry.base_name, dl_entry.file_extension)
