title: Audio downloader sites
layout: subpage
ankiweb_id: 3100585138
parent: Download audio
extra_jq_script: audio_tips.js

These sites are tried to retrieve audio clips:

## Beolingus

[Beolingus](http://dict.tu-chemnitz.de/doc/about.en.html) is an online
dictionary provided by the
[<span class="qtbase tu" lang="de">TU</span> Chemnitz](http://www.tu-chemnitz.de/en/).

The site provides German↔English, German↔Portuguese and German↔Spanish
dictionaries and pronunciations in English, German and Spanish. Some
of the English pronunciations appear to be wrong, so the non-German
words are deleted by default. (The delete button is preselected and the
user has to click the add button to keep the file).

## Collins

[Collins Dictoonaries](http://www.collinsdictionary.com/) are used for
French, German, Italian and Spanish. Here, too, the quality of the
pronunciations didn’t really convince me, so the files will be deleted
by default, too.

## Duden

The [Duden](http://www.duden.de) is pretty much the reference
dictionary for Germany. Many of the audio files are from the
[Aussprachedatenbank der ARD](http://www.ard.de/intern/abc/-/id=1643802/nid=1643802/did=1666544/2b9hfd/index.html#abcListItem_1666544).
It looks like these are used as the reference by the German [newscast
of record](http://www.tagesschau.de).

## <span id='gtts'>Google TTS</span>

Goole TTS is the text-to-speech part of
[Google Translate](http://translate.google.com/#auto/en/).  It is the
only text-to-speech services among the downloaders. The advantage is
that this will almost always get you an audio version of the text
entered – when Google TTS works for your language at all – and can be
used to get an audio version of whole sentences, not just single
words.

The disadvantage is that that this will almost always get you an audio
version of the text entered, even when it is misspelled.

Another disadvantage is that it is a robot voice. It may hide
idiosyncrasies of the phrase or word. Because of this, Google TTS
files are deleted by default, too.

For Chinese, the Google TTS download is skipped by default, because
the [Chinese support](https://ankiweb.net/shared/info/3448800906)
add-on downloads those, too. When you don’t use that add-on or want to
download from Google TTS with this add-on anyway, you can switch it
back on by changing the `False` in the `get_chinese` line near the
head of the
[`googl_tts.py`](https://github.com/ospalh/anki-addons/blob/master/downloadaudio/downloaders/google_tts.py)
file to `True`.

## Howjsay

Requests for English words are sent to [howjsay.com](http://howjsay.com/).

## <span id="jpod">JapanesePod</span>

Downloads audio provided by
[JapanesePod101](http://www.japanesepod101.com/).  This is the same
data source as
[Jim Breen's WWWJDIC](http://www.csse.monash.edu.au/~jwb/cgi-bin/wwwjdic.cgi?1C)
uses for its Japanese audio. WWWJDIC
is the dictionary called <q>edict</q> by the
[Japanese Support add-on](https://ankiweb.net/shared/info/3918629684).

The JapanesePod101 collection has several files for words that are
usually written with kana alone, like <q lang="ja">ください</q>, but
written with kanji, <q lang="ja">下さい</q>. In cases like these the
add-on asks the WWWJDIC site for the kanji version of the word, based
on the reading.

This site was the main motivation for writing this add-on. By
providing a way to download these pronunciations this add-on is a
replacement for the Anki 1 plugins <q>Audio Download</q> and <q>Audio
Download (Extension)</q>.

### <span id="blacklist">Blacklist</span>

The download mechanism at JapanesePod can’t really say
[<q>no</q>](nopagehere.html) in the usual way. Instead it sends you an
audio clip that tells you <q>The audio for this clip is currently not
available. It will be recorded and uploaded shortly. Thank you for
your patience.</q>. While that is a nice gesture, after hearing that
message two or three times the voice starts sounding a bit like <span
class="qtbase sonya">Sonya</span>.


<figure>
<img src="images/blacklist.png"
alt="Review dialog with a skull-and-bones button">
<figcaption>Use the skull-and-bones button to blacklist a file.</figcaption>
</figure>
To deal with this phenomenon, this add-on provides another button in
the download review dialog, called <q>blacklist</q>. Click this for
each file where you get the <q>… currently not available…</q>
spiel. The add-on will then store a
[hash](http://en.wikipedia.org/wiki/Cryptographic_hash_function) for
this file. When the same file is seen again, it is quietly dropped and
you may receive a <q>Nothing downloaded</q> message.

## Leo

These audio files come from
[LEO GmbH](http://www.leo.org/index_en.html), originaly founded by the
[Department of Informatics](http://www.in.tum.de/en.html) of the
[<span class="qtbase tu">TU</span> München](http://www.tum.de/en/homepage/).
They offer several German↔NN dictionaries, with audio files for
English, French, German and Spanish. Some other pronunciations at the site are TTS, and are not downloaded.


## Lexin

Swedish pronunciation from the
[lexikon för invandrare](http://lexin.nada.kth.se/lexin/) of the
[Institutet för språk och folkminnen](http://www.sprakochfolkminnen.se/)
and the [Kungliga Tekniska högskolan](https://www.kth.se/).

## Macmillan

This downloader gets  pronunciations from the
[Macmillan Dictionary](http://www.macmillandictionary.com/) site.

Apart from the pronunciation, for some words that name sounds or
noises, the dictionary offers sound effects, that are also
downloaded. Try downloading
<q>[house](http://en.wikipedia.org/wiki/House_music)</q> or
<q>thunder</q>. The sound effects should be marked in the bubble help
text in the review.

Macmillan Dictionary is available in a British English and an American
English version. To counterbalance the American English of
oher downloaders, the standard install of the add-on uses the British
version. See [below](#sitesonoff) how to turn on the American English
version instead.

## Merriam-Webster

American English pronunciations from the
[Merriam-Webster](http://www.merriam-webster.com/info/index.htm)
online dictionary.

## Oxford Advanced American Dictionary

American English pronunciations from
[Oxford Advanced American Dictionary](http://oaadonline.oxfordlearnersdictionaries.com/).

## Wiktionary

[Wiktionary](http://www.wiktionary.org) is the dictionary branch of Wikipedia.

The add-on tries to download words for every language. Where you get
any results is hard to say.

As these sound files are all uploaded by users, it is possible (even
if unlikely) that some files do not contain what the should. They
*might* even contain obscenities. The
[content disclaimer](http://en.wikipedia.org/wiki/Wikipedia:Content_disclaimer)
from Wikipedia applies. If you encounter an incorrect file, the best
way to proceed is to clean up the Wiktionary page in
question.

The different language versions of Wiktionary add audio clips in
different ways to their word pages. When the add-on did not download a
pronunciation that is present on a specific Wiktionary page, please
[report this](https://github.com/ospalh/anki-addons/issues?state=open). I
will then try to find a way to extract that word, so that it should be
downloaded with an updated version of the add-on.

## <span id="not_forvo">*Not* Forvo</span>

A number of people have asked for the crowd-sourced pronunciation site
[Forvo](http://forvo.com) to be added. While the pronunciations
offered are usually quite useful (even if sometimes of a low audio
quality), adding the site to this add-on does *not* work. Downloading
from Forvo requires what is called <span class="qtbase
onlyone">an</span> <q>API-key</q>. This key would have to be both kept
secret and included in the published add-on source. A contardiction.

(The way Forvo apparently intends this kind of key to be used is to
add a service to a web site, rather than to a bit of free, published
software. The web service owner would than keep eir hands on the key
and hand out just the pronunciations. This add-on does not work this
way.)

My <q lang="de">[Nachschlagen](Nachschlagen.html)</q> add-on adds a
menu item too look up, but not download, words at Forvo.

## <span id="sitesonoff">Using different sites</span>

The add-on loads the different downloaders through the list
<q>`downloaders`</q> in the file “<a
href="https://github.com/ospalh/anki-addons/blob/master/downloadaudio/downloaders/__init__.py">
`downloadaudio/downloaders/__init__.py`</a>”. To get to the file, use
the <q>Tools/Add-ons/Open Add-ons Folder...</q>  menu item, then open the
folder <q>`downloadaudio`</q> and in there <q>`downloaders`</q>.

The downloaders are tried in the order they appear there. To change
this order or to switch on or off downloaders, rearrange the list
entries, or add or remove <q>`#`</q> characters before the name. Lines
starting with a <q>`#`</q> are comments in Python. Those lines are not
used, nothing will be downloaded from these sites.

For example, to change the Macmillan downloads from British English to
American English, add a <q>`#`</q> character to the line
<q>`MacmillanBritishDownloader(),`</q> and remove it from the line
<q>`# MacmillanAmericanDownloader(),`</q>. (Do not remove the comma or
parentheses. Do not make other changes unless you know what you are
doing.)

After you have made changes to the file and saved it, you need to
restart Anki for the changes to take effect.
