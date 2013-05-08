# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

u"""
Move and normalise audio files.
"""

from pydub import AudioSegment
import os
import pysox
import tempfile

from .audio_processor import AudioProcessor


class AudioNormaliser(AudioProcessor):
    u"""
    Class that moves and normalises audio files.
    """
    def __init__(self):
        AudioProcessor.__init__(self)
        self.output_format = ".flac"
        self.useful = True

    def process_and_move(self, in_name, base_name):
        """
        Make new audio file in the media directory.

        Take the audio file with in_name, normalize, convert to
        self.output_format, put in the media folder with a suitable
        file name, delete the old file and return the new name.
        """
        # NB. We don't check the sox import *here*. We only use this
        # when the import worked in __init.py__.
        suffix = os.path.splitext(in_name)[1]
        try:
            sox_in_file = pysox.CSoxStream(in_name)
        except IOError:
            if not '.mp3' == suffix:
                # We can't do anything about the error after all.  (We
                # CAN save mp3 files with pydub. Some soxes can't
                # handle mp3s. Those that can should not raise the
                # IOError.)
                raise
            # So use pydub to convert mp3s to wavs.
            segments = AudioSegment.from_mp3(in_name)
            wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            wav_file.close()
            segments.export(wav_file.name, format='wav')
            os.remove(in_name)
            in_name = wav_file.name
            sox_in_file = pysox.CSoxStream(in_name)
            # Now we should be pretty much at the point we were at the
            # except IOError. With the data in the sox_in_file object.
        # Now do the processing with pysox.
        tof = tempfile.NamedTemporaryFile(delete=False,
                                          suffix=self.output_format)
        # Use a(nother) temp file here, because pysox seemst to have
        # problems with files with non-ASCII names.
        temp_out_file_name = tof.name
        tof.close()
        sox_signal = sox_in_file.get_signal()
        # An old version did some more effects:
        # * Upmixing from mono to stereo: To work around a problem
        #   with an mp3-player that didn't do that. Not needed. And
        #   broken in pysox.
        # * Doing a processing where we removed silence at the
        #   beginning and the end. That kind-of worked, but tended to
        #   either clip bits of speech or to not remove anything.
        # Those are gone now.
        sox_out_file = pysox.CSoxStream(
            temp_out_file_name, 'w', sox_signal)
        sox_chain = pysox.CEffectsChain(sox_in_file, sox_out_file)
        sox_chain.add_effect(pysox.CEffect('gain', [b'-n']))
        sox_chain.flow_effects()
        sox_out_file.close()
        os.remove(in_name)
        return self.unmunge_to_mediafile(
            temp_out_file_name, base_name, self.output_format)
