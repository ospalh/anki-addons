title: Audio downloader sites
id: sites
type: subpage
ankiweb_id: 3100585138
parent: Download audio
extra_jq_script: audio_tips.js

These sites are tried to rerieve audio clips:

## Beolingus

[Beolingus](http://dict.tu-chemnitz.de/doc/about.en.html) is an online
dictionary provided by the
[<span class="qtbase tu">TU</span> Chemnitz](http://www.tu-chemnitz.de/en/).

The site provides German↔English, German↔Portuguese and German↔Spanish
dictionaries and pronuctiations in English, German and Spanish.

### <span id='gtts'>Google TTS</span>

Goole TTS is the text-to-speech part of
[Google Translate](http://translate.google.com/#auto/en/).  It is the
only text-to-speech services among the downloaders. The advantage is
that this will almost always get you an audio version of the text
enterend – when Google TTS works for your language at all – and can be
used to get an audio version of whole sentences, not just single
words.

The disadvantage is that that this will almost always get you an audio
version of the text enterend, even when it is misspelled.

Another disadvantage is that it is a robot voice. It may hide
idiosyncrasies of the phrase or word.

## <span id="jpod">Japanesepod</span>

Downloads audio provided by
[JapanesePod101](http://www.japanesepod101.com/).  This is the same
data source as
[Jim Breen's WWWJDIC](https://groups.google.com/forum/#!searchin/ankisrs/breen/ankisrs/UHGEpSkWf9k/3bFJ71AimCEJ)
uses for its Japanese audio. WWWJDIC is the dictionary called “edict”
by the
[Japanese Support add-on](https://ankiweb.net/shared/info/3918629684).

This was the main motivation for writing this add-on. By providing a
way to download these pronunciations this add-on is a replacement for
the Anki-1 plugins “Audio Download” and “Audio Download (Extension)”,
as mentioned on
[Google Groups](https://groups.google.com/forum/#!searchin/ankisrs/breen/ankisrs/UHGEpSkWf9k/3bFJ71AimCEJ).

### <span id="blacklist">Blacklist</span>

The download mechanism at Japanesepod can’t really say
[“no”](nopagehere.html) in the usual way. Instead it sends you an
audio clip that tells you “The audio for this clip is currently not
available. It will be recorded and uploaded shortly. Thank you for
your patience.”. While that is a nice gesture, after hearing that
message two or three times the voice starts sounding a bit like <span
class="qtbase sonya">Sonya</span>.


<figure style="width:412px;"><img src="images/blacklist.png"
alt="Review dialog with a skull-and-bones button">
<figcaption>Use the skull-and-bones button to blacklist a file.</figcaption>
</figure>
To deal with this phenomenon, this add-on provides another button in
the download review dialog, called “blacklist”.

“”

## Leo

it, ru
### Chinese

Pinyin format

### Macmillan

Apart from the pronunciation, for some words that name sounds or
noises, the dictionary offers “sound effects”, that are also
downloaded. Try downloading
“[house](http://en.wikipedia.org/wiki/House_music)” or “thunder”. The
sound effects should be marked in the bubble help text in the review.

Macmillan dictionary is available in a British English and an American
Engilsh version. To counterbalance the American English of
Merriam-Webster, the standard install of the add-on uses the British
version. To use the American version, edit the file
“<a
href="https://github.com/ospalh/anki-addons/blob/master/downloadaudio/downloaders/__init__.py">`downloadaudio/downloaders/__init__.py`</a>”
in the add-on directory. (Open that directory through the “Tools/Add-ons/Open
Add-ons Folder...” menu item.) Add a “`#`” character to the line
“`MacmillanBritishDownloader(),`” and remove it from the line “`#
MacmillanAmericanDownloader(),`”. Then restart Anki.

## MW

### Wiktionary


Beware! User content. You *might* get obsecnities. Please clean up
wiktionary in that case.

 When the add-on
did not download a pronunciation that is present on a specifc
wiktionary page, please
[report this](https://github.com/ospalh/anki-addons/issues?state=open).
