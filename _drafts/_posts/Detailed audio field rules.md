title: Detailed audio field rules
id: fieldrules
source_file: downloadaudio/get_fields.py
layout: subpage
ankiweb_id: 3100585138
parent: Download audio
extra_jq_script: audio_tips.js

In most cases – including learning Japanese or Chinese with the
[standard](https://ankiweb.net/shared/info/3918629684)
[add-ons](https://ankiweb.net/shared/info/3448800906) installed –
[adding a field](Add%20audio%20field.html) <q>Audio</q> to the note and to at
least [one side of a card](Add%20audio%20to%20cards.html) is enough, but more
sophisticated use of the add-on is also possible.

This page describes how the add-on matches audio and text fields and
gives examples on how to use more than one pronunciation per note.

## Fields rules

The download mechanism uses these rules to match audio fields to text
fields:

For most downloaders, plain text is used. The rules to find the source
fields are:

* When there is a field called
  <ul>
    <li><q>Audio</q> or</li>
    <li><q>Sound</q>,</li>
  </ul>
  the add-on looks for a field called
  <ul>
    <li><q>Expression</q> or</li>
    <li><q>Word</q></li>
  </ul>
* When there is an <q>Audio</q> or <q>Sound</q> field, but no
  <q>Expression</q> or <q>Word</q> field, the first field is used as
  the source.
* For fields where <q>Audio</q> or <q>Sound</q> is a substring, this
  word is removed and the rest used to look for a field. For example,
  to get pronunciations for a field called <q>Example</q>, you should
  add a field named <q>Example Audio</q> (or <q>Audio
  Example</q>). When downloading, the add-on will find the field
  <q>Example Audio</q>, strip the <q>Audio</q>, clean up the space to
  get <q>Example</q> and look for that field to get the text.

To get Japanese pronunciations from
[JapanesePod101.com](http://japanesepod101.com) there has to be the
reading stored in the note. The detailed rules are:

* When there is a field called
  <ul>
    <li><q>Audio</q> or</li>
    <li><q>Sound</q>,</li>
  </ul>
  the add-on looks for a field called
  <ul>
    <li><q>Reading</q>,</li>
    <li><q>Kana</q>,</li>
    <li><q lang="ja">かな</q> or</li>
    <li><q lang="ja">仮名</q></li>
  </ul>
* The substring rule is different for this case. For fields where
  <q>Audio</q> or <q>Sound</q> is a substring, this word is not
  removed, but the add-on looks for fields where that word has been
  *replaced* with one from the <q>Reading</q> list. For example, when
  there is a field called <q>Japanese Reading</q>, add a field
  <q>Japanese Audio</q> to download from the reading field.
* There is no first field rule for readings.

All of these field names are not case sensitive. For example, <q>expression</q>,
<q>auDIO</q> or <Q>SOUND</Q> will work.

The field names are defined in the lists in the file
<q>[`downloadaudio/get_fields.py`](https://github.com/ospalh/anki-addons/blob/master/downloadaudio/get_fields.py)</q>
in the add-ons folder. That folder can be displayed through the
<q>Tools/Add-ons/Open Add-ons Folder...</q> menu item, and names can be
added to the lists.

## Examples

I use complex note types with many fields in my personal
collection. Field lists from these models can be used to demonstrate
real-life use of these rules.

### Model <q>Standard — Japanese</q>

My main Japanese vocabulary model has <span class="qtbase
morefields">these fields</span>:

* Expression
* Reading
* Deutsch
* Zusatz
* Audio
* <span lang="ja">例文</span>
* <span lang="ja">例文</span> Audio

Applying the rules means that:

* The plain rule matches the field  <q>Expression</q> to the field
  <q>Audio</q>. The GoogleTTS downloader will work from the expression and
  download into the audio field.
* The readings rule matches the field <q>Reading</q> to the field
  <q>Audio</q>. The JapanesePod downloader will work from the reading
  and download into the audio field, too.
* The plain substring rule matches the field <q lang="ja">例文</q> to
  the field <q><span lang="ja">例文</span> Audio</q>
* For the fields <q lang="de">Deutsch</q> and <q lang="de">Zusatz</q>
  (and the audio fields themselves), nothing is downloaded.

### Model <q lang="de">Land, state etc.</q>

For my world-wide geography deck, i use  <span class="qtbase
morefields">the fields</span>:

* CountryName
* CountryName_Audio
* Capital
* CapitalName_Audio
* Map
* Flag
* Inhabitants_Scalar
* Area_Scalar
* NameAlternative
* NameAlternative_Audio
* CapitalAlternative
* CapitalAlternative_Audio

Here only the plain substring rule matches. The add-on tries to get
audio for these field pairs:

* CountryName → CountryName_Audio
* Capital → Capital_Audio
* NameAlternative → NameAlternative_Audio
* CapitalAlternative → CapitalAlternative_Audio


### Model <q lang="en"><span lang="ja">都道府県</span> – Japanese</q>

Here some of the  fields are:

* Präfektur_<span lang="ja">ローマ字</span>
* <span lang="ja">都道府県</span>
* <span lang="ja">都道府県</span>_Reading
* <span lang="ja">都道府県</span>_Audio
* Nummer
* Einwohner
* Fläche
* Karte

Here the plain substring and the reading substring rules match:

* The plain substring rule matches the field <q lang="ja">都道府県</q>
  to the field <q><span lang="ja">都道府県</span>_Audio</q>.
* The readings substring rule matches the field <q><span lang="ja">都道
  府県</span>_Reading</q> to the field <q><span lang="ja">都道府県
  </span>_Audio</q>.

Here, too, pronunciations from different source texts are downloaded
to the same field
