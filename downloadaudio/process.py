# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

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



def process_audio(file_name, silence_percent=0.1, silence_end_percent = None):
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
        segments.write(wav_file_name, format='wav')
        os.remove(file_name)
        file_name = wav_file_name
        sox_in_file = pysox.CSoxStream(file_name)
        # Now we should be pretty much at the point we were at the
        # except IOError. With the data in the sox_in_file object.
    # Now do the processing with pysox.
    sox_out_file = free_media_name(file_base_name_noext, output_format)
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
    return file_name
