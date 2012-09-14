# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
import os

# IAR. Variables before imports. The packages we import are rather
# obscure. Don't fail when they aren't there.
sox_fail = None
pydub_fail = None

try:
    import pysox
except ImportError as ie:
    sox_fail = ie

try:
    from pydub import AudioSegment
except ImportError as ie:
    pydub_fail = ie


from  exists import free_media_name

### Use a format here that sox can write and that Anki can play. Only
### formats that your Anki can read are useful. If in doubt, use
### ".wav".(Typically sox can write about any audio file format, or
### any audio file format but mp3.)
## Small, lossy, otherwise nice but may not work with your Anki
output_format = ".ogg"
## Save, but large files.
# output_format = ".wav"
## Lossy. Should work with Anki. May not work with your sox
# output_format = ".mp3"
## Not quite as big as .wav, lossless, rather nice but may not work
## with your Anki
# output_format = ".flac"



def process_audio(file_name, silence_percent=0.1, silence_end_percent=None):
    if sox_fail:
        raise sox_fail
    file_base_name = os.path.basename(file_name)
    file_base_name_noext = file_base_name.rsplit(".", 1)[0]
    # Note: Typical errors of the from_NNs: EOFError: file is not mp3
    # IOError: no such file
    try:
        sox_in_file = pysox.CSoxStream(file_name)
    except IOError:
        if pydub_fail or not file_name.endswith('.mp3'):
            # We can't do anything about the error after all.  (We CAN
            # save mp3 files with pydub. Some soxes can't handle
            # mp3s. Those that can should not raise the IOError.)
            raise
        # So use pydub to convert mp3s to wavs.
        segments = AudioSegment.from_mp3(file_name)
        wav_file_name = free_media_name(file_base_name_noext, '.wav')
        segments.export(wav_file_name, format='wav')
        os.remove(file_name)
        file_name = wav_file_name
        sox_in_file = pysox.CSoxStream(file_name)
        # Now we should be pretty much at the point we were at the
        # except IOError. With the data in the sox_in_file object.
    # Now do the processing with pysox.
    out_file_name = os.path.join(mw.col.media.dir(),
                                 free_media_name(file_base_name_noext,
                                                 output_format)
    sox_signal = sox_in_file.get_signal()
    # We want to pull up mono to stereo, but not downmix more-channel
    # stuff to two channels.  Looks like we have to change the signal
    # as well as use the channels effect.
    in_channels = sox_signal.get_signalinfo()['channels']
    if 1 == in_channels:
        sox_signal.set_param(channels=2)
    sox_out_file = pysox.CSoxStream(out_file_name, 'w', sox_signal)
    sox_chain = pysox.CEffectsChain(sox_in_file, sox_out_file)
    sox_chain.add_effect(pysox.CEffect(
            'silence',[b'1', b'0', '{}%'.format(silence_percent)]))
    # Trick: to automatically remove silence at the end, reverse,
    # remove at the front and reverse.
    sox_chain.add_effect(pysox.CEffect('reverse',[]))
    if not silence_end_percent:
        silence_end_percent = silence_percent
    sox_chain.add_effect(pysox.CEffect(
            'silence',[b'1', b'0', '{}%'.format(silence_end_percent)]))
    sox_chain.add_effect(pysox.CEffect('reverse',[]))
    sox_chain.add_effect(pysox.CEffect('gain',[b'-n']))
    if 1 == in_channels:
        # Work around what appears a bug in pysox. Looks like we need
        # to duplicate the samples. And to do that, we have to pretend
        # to go from 2 channels to 4 channels. In reality we go from 1
        # channel to 2. (pysox's development status is alpha, so i'm
        # not complaining)
        sox_chain.add_effect(pysox.CEffect('channels',[b'4']))
    sox_chain.flow_effects()
    sox_out_file.close()
    os.remove(file_name)
    return os.path.basename(out_file_name)
