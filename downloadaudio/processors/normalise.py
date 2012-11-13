# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

import tempfile
import pysox
import pydub

from .exists import free_media_name


class AudioMover(AudioProcessor):

    def __init__(self):
        AudioProcessor.__init__(self)
        self.output_format = ".flac"

    def process_and_move(self, in_name, base_name):
        """
        Make new audio file in the media directory.

        Copy content of temp_file_name to a file in the media directory
        with a name based on . media_base_name and suffix.
        """

        suffix = os.path.splitext(in_name)[1]



def process_audio(temp_file_name, base_name, suffix,
                  silence_percent=0.1, silence_end_percent=None):
    """
    Process audio.

    Take the audio file with file_name, convert mono to stereo, clip
    silence at the begining and end, normalize, convert to format
    indicated by output_format, put in the media folder with a
    suitable file name and return that base name.
    """
    if sox_fail:
        # unmunge_to_mediafile(temp_file_name, base_name, suffix)
        raise sox_fail
    # Note: Typical errors of the form_NNs: EOFError: file is not mp3
    # IOError: no such file
    # Typical error of CSoxSTream constructur: UnicodeEncodeError:
    # File is perfectly all right, but not English (i.e., with a pure
    # ASCII name). We have to work around files with non-ascii names.
    # And now we just
    try:
        sox_in_file = pysox.CSoxStream(temp_file_name)
    except IOError:
        if pydub_fail or not '.mp3' == suffix:
            # We can't do anything about the error after all.  (We CAN
            # save mp3 files with pydub. Some soxes can't handle
            # mp3s. Those that can should not raise the IOError.)
            raise
        # So use pydub to convert mp3s to wavs.
        segments = AudioSegment.from_mp3(temp_file_name)
        wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        wav_file.close()
        segments.export(wav_file.name, format='wav')
        os.remove(temp_file_name)
        temp_file_name = wav_file.name
        sox_in_file = pysox.CSoxStream(temp_file_name)
        # Now we should be pretty much at the point we were at the
        # except IOError. With the data in the sox_in_file object.
    # Now do the processing with pysox.
    tof = tempfile.NamedTemporaryFile(delete=False, suffix=output_format)
    temp_out_file_name = tof.name
    tof.close()
    sox_signal = sox_in_file.get_signal()
    # (Removed the upmixing stuff.)
    sox_out_file = pysox.CSoxStream(temp_out_file_name, 'w', sox_signal)
    sox_chain = pysox.CEffectsChain(sox_in_file, sox_out_file)
    sox_chain.add_effect(
        pysox.CEffect('silence', [b'1', b'0', '{}%'.format(silence_percent)]))
    # Trick: to automatically remove silence at the end, reverse,
    # remove at the front and reverse.
    sox_chain.add_effect(pysox.CEffect('reverse', []))
    if not silence_end_percent:
        silence_end_percent = silence_percent
    sox_chain.add_effect(
        pysox.CEffect('silence',
                      [b'1', b'0', '{}%'.format(silence_end_percent)]))
    sox_chain.add_effect(pysox.CEffect('reverse', []))
    sox_chain.add_effect(pysox.CEffect('gain', [b'-n']))
    # (Removed the upmixing stuff)
    sox_chain.flow_effects()
    sox_out_file.close()
    os.remove(temp_file_name)
    return unmunge_to_mediafile(temp_out_file_name,
                                base_name, output_format)


def unmunge_to_mediafile(temp_file_name, media_base_name, suffix):
    """
    Copy content of temp_file_name to a file in the media directory.

    Copy content of temp_file_name to a file in the media directory
    with a name based on . media_base_name and suffix.
    """
    mdir = mw.col.media.dir()
    media_file_name = free_media_name(media_base_name, suffix)
    with open(temp_file_name, "rb") as tfile:
        with open(os.path.join(mdir, media_file_name), 'wb') as mfile:
            mfile.write(tfile.read())
    os.remove(temp_file_name)
    return media_file_name
