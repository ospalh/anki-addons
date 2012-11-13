# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""
Move a file to the Anki2 media folder, processing it on the way when
possible.
"""


class AudioProcessor(object):

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
