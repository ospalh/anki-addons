title: Download audio
id: dlaudio
main_file: Download%20audio.py
status: undocumented
type: addon
status_color: yellow
status_text_color: black
abstract: Automatically download audio from talking dictionaries or from Google TTS.
first_image: Downloaded%20audio.png
first_alt: Reviewing downloaded audio files.
subtitle: Hear what you learn
ankiweb_id: 3100585138
extra_jq_script: audio_tips.js

This add-on adds three menu items,

* “Edit/Media/Note audio”
* “Edit/Media/Side audio” and
* “Edit/Media/Manual audio”,

All three try to download audio in slightly different manners from a
number of sources.
<span class="clear" />

## First start – Language

<figure style="width:410px;"><img src="images/Set%20language.png"
alt="Dialog: Set language: ">
<figcaption>Set the code of the language you are learning on
startup.</figcaption>
</figure>
The <span class="qtbase nolangcode">first time</span> you <span
class="qtbase profload">start</span> Anki after downloading the
add-on, a dialog will appear asking for a language code. Here you
should select the language you are learning, not your native language.

<blockquote class="nb">When setting the language, use language
codes. Do <em>not</em> use country domain names. For example, use
<code>zh</code> for Chinese, <em>not</em>
<code>cn</code>.</blockquote>

A list of audio codes can – unsprprisingly – be found at
[Wikipedia](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).


## Setup – Fields

This add-on adds the pronunciation to a field named “Audio”. You will
probably have to [add this field](Add%20audio%20field.html) to your notes
and cards.

More sophisticated uses are also possible. Interested users can look
at the [detailed rules](Detailed%20audio%20field%20rules.html) on field
selection for hints on how to use more then one pronunciation per
note.

## Setup – Cards

To use the downloaded data, you have to add [add the field](Add%20audio%20to%20cards.html) to a card.

Here, too, more ore sophisticated uses are described on an
[extra page](More%20audio%20cards.html).
## Downloading

When reviewing, select one of the three “Edit/Media/Note audio”,
“Edit/Media/Side audio” and “Edit/Media/Manual audio” menu items to
download.

When editing or adding cards, click the megaphone button above the field edit
list to do a manual download.

### Side audio

Side audio loads audio that will appear on the currently visible
side. During the [review](#Review), it will hide the text it used to
get the sounds. Use this while learning from your native language to
the foreign language, or when trying to recoginize spoken words.

### Note audio

Note audio fetches sounds for all audio fields of the current note.
During the (review)[#Review], the texts used to
retrieve the sounds are shown.


### Manual audio

<figure style="width:286px;">
<img src="images/update_annex.png" alt="Anki Download audio dialog
window. Text: Requestst send to the download sites. Front. Edit text:
to annex. The to is marked..">
<figcaption>Edit the request before it is send.</figcaption>
</figure>
Manual audio mode opens a dialog showing all fields where files can be
downloaded. The texts, as well as the language to use, can be changed
before the request is send.

<figure style="width:457px;">
<img src="images/update_kanji_kana.png" alt="Anki Download audio dialog
window. Text: Requestst send to the download sites. Reading. Edit texts:
夫 おっと, Text: Expression. Edit text 夫.">
<figcaption>Edit Japanese text.</figcaption>
</figure>

When learning Japanese or Chinese, when there is a “Reading” field,

As a little hint, in the example you should use the “Note audio” mode:
most dictionaries have pronunciations for verbs without “to” and for
nouns without article. In the note audio dialog delete the
“to&nbsp;”. Download for  “annex”, not for “to annex”. The
Merriam-Webster downloader should fetch two pronunciations, `\ə-ˈneks,\`
as in the verb and `\ˈa-ˌneks\` like the noun.

For most downloads, the dialog has one edit field for the text and one
edit field for the language code. Use this to change what is sent to
fetch the audio. In the exapmle, you will get more re

## Review

After the download, click here, here, or here.

“” “” “” “” “”


## Languages

### Changing languages

After the start, the language code can be
[changed in the deck options](Setting%20deck%20options.html),
under the general tab. This can be done for separately for each
options group. Like this, it is possible to use different download
languages with different decks. See also the
[Anki manual](http://ankisrs.net/docs/dev/manual.html#deckoptions).

### Using tags

When a note has a tag in the form “`lang_<NN>`” (e.g. “`lang_en`” for
English, “`lang_zh`” Chinese), this language code (that is “`en`” or
 “`zh`”) is used for the download.
 words fo


### Multilingual notes

For single notes that should use more then one language, there are two
possibilities:

* Put cards for different languages in different decks

### Manual download

For manual downloads, the language for the current request can be set
at the same time the text is changed.


### Supported languages

The languages this add-on supports depends on the languages of the
dictionaries used.

At the moment, you can get pronunciations for

* Chinese (Mandarin, i think) (`zh`)  from [LEO.org](http://leo.org),
* English (`en`) from [BeoLingus](http://beolingus.org),
  [LEO.org](http://leo.org),
  [Macmillan Dictionary](http://www.macmillandictionary.com/dictionary/) and
  [Merriam-Webster](http://merriam-webster.com)
* French (`fr`) from [LEO.org](http://leo.org)
* German (`de`) from [BeoLingus](http://beolingus.org) and
  [LEO.org](http://leo.org)
* Japanese (`ja`) fram [JapanesePod](japanesepod101.com)
* Spanish (`es`) from [BeoLingus](http://beolingus.org)

There is the potential for

* Italian  (`it`) and
* Russian  (`ru`),

but i think [LEO](http://leo.org) is only offering a text dictionary
for those two languages, not their own audio files.

Google TTS works only with number of languages. They offer
translations for over 60 languages. For other languages no audio will
be generated.

Lastly, [Wiktionary](wiktionary.org) is asked with any language
code. The add-on may or may not find anything useful.



## Site specific

### Japanesepod

Blacklist

### Google TTS

Caveat emptor robot voice

### Macmillan

Gimick: get "house" UmtsUmtsUmtsUmtsUmtsUmtsUmtsUmtsUmtsUmtsUmts

### Wiktionary

Beware! User content. You *might* get obsecnities. Please clean up
wiktionary in that case.

## Private use

These audio files can be freely downloaded without registering or
agreeing to a license, but they keep the copyright of those providing
them. While i see no problem with using them privately, re-publishing,
for example by uploading a shared deck to AnkiWeb, is most likely
prohibited by those rights.


## Tips

Some ideas on getting the most out of this:

### Multilingual decks

tags

### Multilingual cards

Different decks

## Pysox and Pydub

Get them.

## Ideas for improvements
While this add-on works as it is, a few things would be nice.

* Switch off the menu items when not reviewing.
* Automatically edit the information before the request is sent. I use
  what i call “electric” cards for Japanese verbs, where the different
  forms are formed automatically. That means that the whole word
  doesn’t actually appear on the card. While it is no big problem to
  complete the word in the “Manual audio” dialog, the add-on could
  automatically add the 「る」 for 一段動詞.  This will most likely
  not by implemented any time soon.
* More talking dictionaries. Links welcome. Python files welcome.
