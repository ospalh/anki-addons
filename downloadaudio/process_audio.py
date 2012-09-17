# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

from aqt import mw
import os
import tempfile

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
    try:
        file_base_name_noext, file_extension = file_base_name.rsplit(".", 1)
        file_extension = '.' + file_extension
    except ValueError:
        file_base_name_noext = file_base_name
        file_extension = ''
    # Note: Typical errors of the from_NNs: EOFError: file is not mp3
    # IOError: no such file
    # Typical error of CSoxSTream constructur: UnicodeEncodeError:
    # File is perfectly all right, but not English (i.e., with a pure
    # ASCII name). We have to work around files with non-ascii names.
    temp_file_name = munge_to_tempfile(file_name, file_extension)
    print u'processing from ' + temp_file_name
    try:
        sox_in_file = pysox.CSoxStream(temp_file_name)
    except IOError:
        if pydub_fail or not '.mp3' == file_extension:
            # We can't do anything about the error after all.  (We CAN
            # save mp3 files with pydub. Some soxes can't handle
            # mp3s. Those that can should not raise the IOError.)
            raise
        # So use pydub to convert mp3s to wavs.
        segments = AudioSegment.from_mp3(temp_file_name)
        wav_file_name = free_media_name(file_base_name_noext, '.wav')
        segments.export(wav_file_name, format='wav')
        os.remove(temp_file_name)
        temp_file_name = munge_to_tempfile(wav_file_name, ".wav")
        print u'actually processing from ' + temp_file_name
        sox_in_file = pysox.CSoxStream(temp_file_name)
        # Now we should be pretty much at the point we were at the
        # except IOError. With the data in the sox_in_file object.
    # Now do the processing with pysox.
    tof = tempfile.NamedTemporaryFile(delete=False, suffix=output_format)
    temp_out_file_name = tof.name
    print u'processing to ' + temp_out_file_name
    tof.close()
    sox_signal = sox_in_file.get_signal()
    # We want to pull up mono to stereo, but not downmix more-channel
    # stuff to two channels.  Looks like we have to change the signal
    # as well as use the channels effect.
    in_channels = sox_signal.get_signalinfo()['channels']
    if 1 == in_channels:
        sox_signal.set_param(channels=2)
    sox_out_file = pysox.CSoxStream(temp_out_file_name, 'w', sox_signal)
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
    os.remove(temp_file_name)
    return unmunge_to_mediafile(temp_out_file_name,
                                file_base_name_noext, output_format)

def munge_to_tempfile(file_name, suffix):
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    ufile = open(file_name, "rb")
    tfile.write(ufile.read())
    tfile.close()
    ufile.close()
    os.remove(file_name)
    return tfile.name


def unmunge_to_mediafile(temp_file_name, media_base_name, suffix):
    mdir = mw.col.media.dir()
    media_file_name = free_media_name(media_base_name, suffix)
    tfile = open(temp_file_name, "rb")
    mfile = open(os.path.join(mdir, media_file_name), 'wb')
    mfile.write(tfile.read())
    tfile.close()
    mfile.close()
    os.remove(temp_file_name)
    return media_file_name
