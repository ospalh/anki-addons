# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–13 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""
Move a file to the Anki2 media folder, processing it on the way when
possible.
"""

import shutil

from ..exists import free_media_name


class AudioProcessor(object):
    u"""Class to do audio processing."""
    def __init__(self):
        """
        Keep track if there is a point in using this at all.

        Only one of the audio processors is actually useful. The other
        just moves the file without changing it. So we can use this
        value and skip the step of creating a temp file and then just
        moving the content of that file.
        """
        self.useful = False

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
        u"""
        Move the data to the media folder.

        Determine a free media name and move the data there from the
        tempfile.
        """
        # New style: we now get both the path and just the file name out
        # of free_media_name.
        media_path, media_file_name = free_media_name(base_name, suffix)
        # Don't copy and delete, let the os do the work.
        shutil.move(in_name, media_path)
        return media_file_name
