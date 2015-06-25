# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Process an audio file.
"""


from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os
import tempfile

load_functions = {
    'mp3': AudioSegment.from_mp3, 'ogg': AudioSegment.from_ogg,
    'wav': AudioSegment.from_wav}

output_format = 'flac'
output_suffix = '.' + output_format
silence_threshold = -30
# Use lower values like -40, -50 when stuff gets cut off
minimum_silence_length = 150
# Similarly, try longer values here if the silencing doesn’t work well
silence_fade_length = 100  # Quick fade in and out where we found silence
rapid_fade_length = 20
# Rapid fade in and at the beginning or end. Mostly to avoid the click
# of a DC offset.


class AudioProcessor(object):
    u"""Class to do audio processing."""
    # In the past we kept track of whether the processor was
    # “useful”. That ment that the downloaders downloaded to
    # different places depending on which processor we had. Maybe
    # useful, but somewhat Byzantine.
    #
    # That was gone temporarily. Now we do something similar
    # again. Check __init__ and DownloadEntry.process. That checks if
    # there *is* a processor, rather than ask if it is useful.

    def process(self, dl_entry):
        """Make new audio file in the media directory.

        Take the audio file pointed to by dl_entry, normalize, remove silence,
        convert to output_format.
        """
        input_format = dl_entry.file_extension.lstrip('.')
        try:
            loader = load_functions[input_format]
        except KeyError:
            loader = lambda file: AudioSegment.from_file(
                file=file, format=input_format)
        segment = loader(dl_entry.file_path) # This
        # sometimes raised a pydub.exceptions.CouldntDecodeError
        segment = segment.normalize()  # First normalize
        # Try to remove silence
        loud_pos = detect_nonsilent(
            segment, min_silence_len=minimum_silence_length,
            silence_thresh=silence_threshold)
        fade_in_length = rapid_fade_length
        fade_out_length = rapid_fade_length
        if len(loud_pos) == 1:
            loud_p = loud_pos[0]
            if loud_p[0] > silence_fade_length:
                fade_in_length = silence_fade_length
            if loud_p[1] < len(segment) - silence_fade_length:
                fade_out_length = silence_fade_length
            if loud_p[0] > 0 or loud_p[1] < len(segment):
                segment = segment[loud_p[0] : loud_p[1]]
        segment = segment.fade_in(fade_in_length).fade_out(fade_out_length)
        # Now write
        tof = tempfile.NamedTemporaryFile(
            delete=False, suffix=output_suffix, prefix=u'anki_audio_')
        temp_out_file_name = tof.name
        tof.close()
        segment.export(temp_out_file_name, output_format)
        os.unlink(dl_entry.file_path)  # Get rid of unprocessed version
        return temp_out_file_name, output_suffix
