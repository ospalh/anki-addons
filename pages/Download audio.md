title: Download audio
id: dlaudio
main_file: Download%20audio.py
status: undocumented
type: addon
status_color: yellow
status_text_color: black
abstract: Automatically download audio from Google TTS and Japanesepod
first_image: Downloaded%20audio.png
first_alt: Reviewing downloaded audio files.
extra_jq_script: audio_tips.js
ankiweb_id: 3100585138

Automatically download audio from Google TTS and Japanesepod.

This add-on adds three menu items, “Note audio”, “Side audio” and
“Manual audio”, that all try to download audio in slightly different
manners.

## Please be patient

While the add-on is pretty much finished, this manual page is
not. Please be patient.

## Setup – Fields

The download mechanism looks for audio fields to store the information
in, according to two rules:

* When there is a field called “<span class="qtbase
  ignorecase">Expression</span>”, “<span class="qtbase
  ignorecase">Front</span>”, or “<span class="qtbase
  ignorecase">Back</span>”, the add-on looks for a field called “<span
  class="qtbase ignorecase">Audio</span>” or “<span class="qtbase
  ignorecase">Sound</span>”.
* For other fields, the add-on looks for a second field with the same
  name with “Audio” or “Sound” added. Like this, one note can store
  different audio files for different fields. For example, a geography
  deck can have fields “Country” and “Capital”. When that note
  also has fields “Country Audio” and “Capital Audio”, the add-on can
  download pronunciation for these two fields separately.


### Japanesepod

Downloading Japanese pronunciations from Japanesepod works a little
bit different. The field must be set up in the way used by the
Japanese support addon, that is, there should be a “<span class="qtbase
  ignorecase">Reading</span>” field and an “Audio” or “Sound”
field. The reading field must contain both the kanji and kana for
the requested word, with the reading for the kanji in square
brackets. For example as 「仮定[かてい]」, which will be automatically
split into 「仮定」 and 「かてい」.

Alternative names for “Reading” are “Kana”, 「かな」and 「仮名」.

Also, when “Audio” is just a substring, that substring is replaced
with “Reading”, not removed. For example, when you have a field
“Japanese Audio”, you need another field “Japanese Reading”.

### Add fields
<blockquote class="nb">Make sure that you have a field called
“Expression” and another field named “Audio”. For Japanese, you also need
a field called “Reading”.</blockquote>

To add an “Audio” field and to rename a field to “Expression”, click
on “Edit” in the bottom left, then on “Fields”. Check if these names
appear in the list. If not, click on the field where you store your
foreign words, click on “Rename” and enter “Expression”  as the
new. name. At this point a dialog may pop up.

<blockquote class="nb">Adding fields or changing field names requires
a full sync. Make sure your collection is synced before adding the
names. Remember to sync any learning progress with mobile
devices, too.</blockquote>

When you need to sync, click on “No” and sync your collection. Then
try again, and answer “Yes” at the dialog.

Similarly, if there is no
field named “Audio”, click on “Add” and enter “Audio” as the new name.

## Setup – Language

The default download language is Japanese, when you are learning
another language, you have to change this, there are <span
class="qtbase" id="fourth">three</span> ways to do this.

<blockquote class="nb">When setting the language, use language
codes. Do <em>not</em> use country domain names. For example, use
<code>zh</code> for Chinese, <em>not</em>
<code>cn</code>.</blockquote>

Google TTS works only with a few languages. Using an unsupported or
invalid code will result in no audio downloads.

A list of audio codes can – unsprprisingly – be found at
[Wikipedia](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).

### Deck options ###

To permanently set the language change it in the new “Language code”
field in the deck options.

In the deck selector, click on the gear button to the right of the
deck name, then select “”options“”. In the dialog that opens, click on the
“”general“” tab. Enter the code for your language in the “Language
code” text field.

This setting is done by options group. Each deck has an options group,
but these goups can be shared between decks. See the
[Anki manual](http://ankisrs.net/docs/manual.html#deckoptions) for
more details.

Through the options group mechanism, different decks can use different
download languages.

### Tags ###

When a note has a tag in the form “`lang_<NN>`” (e.g. “`lang_en`” for
English, “`lang_zh`” Chinese), this language code (that is “`en`” or
 “`zh`”) is used for the download.
 words fo

### Manual download ###

For manual downloads, the language for the current request can be set
at the same time the text is changed.

## Downloading

Once the deck hes been set up, pronunciations can be downloaded in one
of three ways, called “Note audio” “Side audio” and “Manual
audio”. When reviewing, all three modes are available in the
“Edit/Media” menu. When editing cards, the “Manual audio” mode is
available through the megaphone button above the field edit list.

“” “” “” “” “” “”


### Manual audio

### Note audio

### Side audio



### Review

#### Japanesepod

Blacklist



## Language

There are up to four ways the download language is determined

* For manual downloads, the language code can be set in the dialog.
* The language code can be set as a tag on individual cards
* ... settings ...
* ... default ...

## Google TTS

Caveat emptor robot voice

## Japanesepod

Split kana kanji

## Private use

These audio files can be freely downloaded without registering or
agreeing to a license, but they keep the copyright of those providing
them. While i see no problem with using them privately, re-publishing,
for example by uploading a shared deck to AnkiWeb, is most likely
prohibited by those rights.

## Pysox and Pydub

Get them.

## Ideas for improvements
While this add-on works as it is, a few things would be nice.

 * Automatically edit the information before the request is sent. I use
   what i call “electric” cards for Japanese verbs, where the
   different forms are formed automatically. That means that the whole
   word doesn’t actually appear on the card. While it is no big
   problem to complete the word in the “Manual audio” dialog, the
   add-on could automatically add the 「る」 for 一段動詞.
