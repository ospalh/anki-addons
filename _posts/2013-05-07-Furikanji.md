---
layout: addon
title: Furikanji
permalink: Furikanji.html
source_file: furikanji.py
categories:
 - yellow
 - addon
status: for desktop use only
abstract: >
 Display text as furikanji, that is, show kana on the base line, with
 the kanji above. This adds a few other display hacks, too.
first_image: furikanji.png
first_alt: "Sceenshot of text ふりかんじ with 振り漢字 as ruby."
first_caption: Furikanji demo
ankiweb_id: 2327947748
---
{% raw %}This add-on adds support for furikanji and slightly changes the way
kanji and readings are parsed.

<blockquote class="nb">
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

### <span id="droid">Furikanji and AnkiDroid</span>

<figure> <img src="images/furikanji-mydroid.png" alt="Text: 起きなよい
い加減おwith きなよいいかげん as ruby and きなよいいかげん with 起きな
よいい加減お as ruby. The kanji of the ruby are marked in orange.">
<figcaption> AnkiDroid can be patched to use furikanji.  </figcaption>
</figure> Daring spirits can take a look at my version of the
[`FuriganaFilters.java`](https://github.com/ospalh/Anki-Android/blob/develop-ospalh-special/AnkiDroid/src/main/java/com/ichi2/libanki/hooks/FuriganaFilters.java)
file and add furikanji to their own version of AnkiDroid

This may not work with Android versions < 3.0

## CSS classes

Text that uses the now four templates `furigana`, `furikanji`, `kana`
and `kanji` gets appropriate CSS classes. The `ruby` elements have the
additional classes  `furigana` and `furikanji`; the kana and kanji
texts get wrapped in spans with classes `kana`  and
`kanji`.

See the [complex classes](Complex%20classes.html) page for examples on
how to use these classes.


## Furigana, kanji and reading templates

The `{{furigana:Field NN}}`, `{{kanji:Field NN}}` and `{{kana:Field
NN}}` templates have been modified. The standard templates use ASCII
spaces (<q> </q>) and <q>></q> characters to determine the beginning of the
kanji text. The modified version treats only characters in the word
character class as ruby base.

This means that commas, newlines,
[CJK](http://en.wikipedia.org/wiki/CJK_characters)
[spaces](http://www.fileformat.info/info/unicode/char/3000/index.htm)
&c. can be used as separators between kanji and other, preceding text.

### Limitations

* Leading kana are not automatically separated. For example the
  reading for <q lang="ja">お釣り</q> must still be written with an ASCII space or
  other separator between the <q lang="ja">お</q> and the <q lang="ja">釣</q>: <q lang="ja">お 釣[つ]り</q>.
* This mechanism only work with Python version 2.7.
* As the other functions, this works only on the desktop client.{% endraw %}
