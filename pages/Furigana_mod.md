title: Modified furigana
id: furigana_mod
main_file: Furikanji_mod.py
date: 2012-06-08
tags: [Japanese, template, kanji, furigana, rubi]
type: addon
status: limited usefulness
status_color: yellow
status_text_color: black
abstract: Improved way to parse kanji and readings, a way to rendder kanji the kana and a few other display hacks.
first_image: furikanji.png
first_alt: Furikanji demo

This add-on adds support for Furikanji, adds two other templates and
slightly changes the way kanji and readings are parsed.

<blockquote class=nb>
This addon is for use with the desktop
client only. Using features of this add-on with mobile clients or
AnkiWeb may result in suboptimal layout.
</blockquote>

### Furikanji

<figure><img src="images/furikanji_setup.png" alt="Use furikanji as
the field template in the card template"><figcaption>Use
`{{furikanji:NN}}` in the card template.
</figcaption></figure> 

The template `furikanji` uses a standard reading field to 
render kanji *above* the kana. This is useful for listening comprehension.

To use this, put  `{{furikanji:Field name}}` instead of
`{{furigana:Field name}}` in the template.

The ruby element has the aditional class `furikanji`. So special
styling w


### Furigana, kanji and reading templates

The `{{furigana:Field NN}}`, `{{kanji:Field NN}}` and `{{reading:Field
NN}}` templates have been modified. The standard templates use ASCII
spaces, “ ”, and “>” characters to determine the beginning of the
kanji text. The modified version treats only characters in the word
character class as kanji.

This means that commas, newlines,
[CJK](http://en.wikipedia.org/wiki/CJK characters)
[spaces](http://www.fileformat.info/info/unicode/char/3000/index.htm)
&c. can be used as separators between kanji and other, preceding text.

The addon also adds the class `furigana` to the ruby element.
#### Limitations

* Leading kana are not automatically separated. For example the
  reading for 「お釣り」 must still be written with an ASCII space or
  other separator between the 「お」 and 「釣」: 「お 釣[つ]り」.
* This mechanism only work with Python version 2.7.

