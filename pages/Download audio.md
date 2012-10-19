title: Download audio
id: dlaudio
main_file: Download audio.py
status: unfinished
type: addon
status_color: yellow
status_text_color: black
abstract: Automatically download audio from Google TTS and Japanesepod
first_image: dl_code.png
first_alt: Bits of the code.
extra_jq_script: audio_tips.js

Automatically download audio from Google TTS and Japanesepod.

This add-on adds three menu items, “Note audio”, “Side audio” and “Manual audio”,
that all try to download audio in slightly different manners.

## Fields
The download mechanism looks for audio fields to store the information
in, according to two rules:

* When there is a field called “<span class="qtbase
  ignorecase">Expression</span>”, “<span class="qtbase
  ignorecase">Front</span>”, or “<span class="qtbase
  ignorecase">Back</span>”, the add-on looks for a field called “<span class="qtbase
  ignorecase">Audio</span>” or “<span class="qtbase
  ignorecase">Sound</span>”.


## Not GoogleTTS
Afais, the main difference between this and the GoogleTTS add-on is
that the pronunciation is saved, which is useful for offline use.

## Ideas for improvements
While this add-on works as it is, a few things would be nice.

 * Automatically edit the information before the request is sent. I use
   what i call “electric” cards for Japanese verbs, where the
   different forms are formed automatically. That means that the whole
   word doesn’t actually appear on the card. While it is no big
   problem to complete the word in the “Manual audio” dialog, the
   add-on could automatically add the 「る」 for 一段動詞.
