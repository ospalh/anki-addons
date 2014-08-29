title: Furikanji
id: furikanji
main_file: furikanji.py
type: addon
date: 2013-05-07
status: for desktop use only
status_color: yellow
status_text_color: black
abstract: "Improved way to parse kanji and readings, a way to render
kanji the kana and a few other display hacks."
first_image: furikanji.png
first_alt: "Sceenshot of text ふりかんじ with 振り漢字 as ruby."
first_caption: Furikanji demo
ankiweb_id: 2327947748

This add-on adds support for furikanji, adds two other templates and
slightly changes the way kanji and readings are parsed.

<blockquote class=nb>
This add-on is for use with the desktop
client only. Using features of this add-on with mobile clients or
AnkiWeb may result in suboptimal layout.
</blockquote>

## Furikanji

The template `furikanji` uses a standard reading field to
render kanji *above* the kana.

To use this, put  `{{furikanji:Field name}}` instead of
`{{furigana:Field name}}` in the template.


<figure>
<img src="images/furikanji-web.png" alt="Text: 起きなよいい加減お with
きなよいいかげん as ruby and 起[お]きなよいい 加減[かげん], with
square brackets.">
<figcaption> On AnkiWeb, the furikanji don’t work. </figcaption>
</figure>
As the furikanji rendering is done on the fly by the desktop client,
it does not work with AnkiWeb, AnkiDroid or AnkiMobile. There the text
is rendered as it is seen in the edit screen, with the square
brackets.

### <span id="droid">feature-furikanji</span>

<figure> <img src="images/furikanji-mydroid.png" alt="Text: 起きなよい
い加減おwith きなよいいかげん as ruby and きなよいいかげん with 起きな
よいい加減お as ruby. The kanji of the ruby are marked in orange.">
<figcaption> AnkiDroid can be patched to use furikanji.  </figcaption>
</figure> Daring spirits can take a look at my
[furikanji branch](https://github.com/ospalh/Anki-Android/tree/feature-furikanji)
of AnkiDroid.  I have added the equivalent of this add-on, providing
furikanji on AnkiDroid. You should merge this branch into the newest
version of AnkiDroid, not just use that branch as-is.

This may not work with Android versions < 3.0

## CSS classes

Text that uses the now four templates `furigana`, `furikanji`, `kana`
and `kanji` gets appropriate CSS classes. The `ruby` elements have the
additional classes  `furigana` and `furikanji`; the kana and kanji
texts get wrapped in spans with classes `kana`  and
`kanji`. Additionally, the base of the ruby gets wrapped in spans with
the `rb` class.

See the [complex classes](Complex%20classes.html) page for examples on
how to use these classes.


## Furigana, kanji and reading templates

The `{{furigana:Field NN}}`, `{{kanji:Field NN}}` and `{{kana:Field
NN}}` templates have been modified. The standard templates use ASCII
spaces (“ ”) and “>” characters to determine the beginning of the
kanji text. The modified version treats only characters in the word
character class as ruby base.

This means that commas, newlines,
[CJK](http://en.wikipedia.org/wiki/CJK_characters)
[spaces](http://www.fileformat.info/info/unicode/char/3000/index.htm)
&c. can be used as separators between kanji and other, preceding text.

### Limitations

* Leading kana are not automatically separated. For example the
  reading for 「お釣り」 must still be written with an ASCII space or
  other separator between the 「お」 and the 「釣」: 「お 釣[つ]り」.
* This mechanism only work with Python version 2.7.
* As the other functions, this works only on the desktop client.
