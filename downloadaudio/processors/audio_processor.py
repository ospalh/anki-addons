# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker, <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Move a file to the Anki2 media folder, processing it on the way when
possible.
"""

import shutil

from ..exists import free_media_name


class AudioProcessor(object):
    u"""Class to do audio processing."""
    # In the past we kept track of whether the processor was
    # “useful”. That ment that the downloaders downloaded to
    # different places depending on which processor we had. Maybe
    # useful, but somewhat Byzantine. Get rid of that extra
    # complexit. Now the downloaders download to temp files and
    # the processor moves the file, changed or not. So nothing
    # left to do → no __init__

    def process_and_move(self, dl_entry):
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
        # N.B.: We can’t use the DownloadEntry in here because the
        # normalizing processor may move the temp file because pysox
        # can’t handle mp3 files. (Another reason to get rid of pysox)
        media_path, media_file_name = free_media_name(base_name, suffix)
        shutil.move(in_name, media_path)
        return media_file_name
