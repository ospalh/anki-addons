title: Modified furigana
id: furiganamod
main_file: Furigana%20mod.py
type: addon
status: for desktop use only
status_color: yellow
status_text_color: black
abstract: Improved way to parse kanji and readings, a way to render kanji the kana and a few other display hacks.
first_image: furikanji.png
first_alt: Furikanji demo

This add-on adds support for furikanji, adds two other templates and
slightly changes the way kanji and readings are parsed.

<blockquote class=nb>
This addon is for use with the desktop
client only. Using features of this add-on with mobile clients or
AnkiWeb may result in suboptimal layout.
</blockquote>

### Furikanji

The template `furikanji` uses a standard reading field to
render kanji *above* the kana. This is useful for listening comprehension.

To use this, put  `{{furikanji:Field name}}` instead of
`{{furigana:Field name}}` in the template.

The ruby element has the additional class `furikanji`. So special
styling can be added. For example, markers that show the beginning and
end of a specific block.

<figure style="width:277px;">
<img src="images/furikanji-desktop.png"
    alt="起きなよいい加減お きなよいいかげん">
<figcaption>Example use of furigana and
    furikanji. The source of the text is an Anki-2-ified version of the
    <a href="http://subs2srs.sourceforge.net/">sub2srs</a> example deck 「時を掛ける少女」.
</figcaption></figure>

For the example, i used
<blockquote><pre><code>.redish { color: #a00;}
.furikanji:before, .furikanji:after {
    font-size: 50%;
    position: relative;
    bottom: 2 rem;
    width: 0px;
    z-index: -10;
    vertical-align: baseline;
}
.furikanji:before { content : "|"}
.furikanji:after { content : "|"}</code></pre></blockquote>
as styling and
<blockquote><pre><code>&lt;div>{{Image}}&lt;/div>
{{Audio}}
&lt;div class="nhg lnsz">{{furigana:Reading}}&lt;/div>
&lt;div class="nhg redish lnsz">{{furikanji:Reading}}&lt;/div></code></pre></blockquote>
as back template.

<figure style="width:411px;"><img src="images/furikanji-web.png" alt="起きなよいい加減お
起[お]きなよいい 加減[かげん]"><figcaption>On AnkiWeb, the furikanji
don’t work.</figcaption></figure>

As the furikanji rendering is done on the fly by the desktop client,
it naturally does not work with AnkiWeb or AnkiDroid (or, presumably,
the iOS client). Here the text is rendered as it is seen in the edit
screen, with the square brackets.


### Boxed and boxkana

<figure style="width:125px;"><img src="images/boxed.png"
alt="ausruhen やすむ"><img src="images/boxkana.png"
alt="ausruhen やすむ"><figcaption>Two ways to show the reading of a
kanji you want to learn.
</figcaption></figure>

The `boxed` template surrounds the field text with a dashed box. The
`boxkana` template creates an empty box and sets the field text as
ruby above the box. A typical use for the latter is learning kanji,
when the reading is given as a hint. For the figure,
`{{boxed:Lesung}}` and `{{boxkana:Lesung}}` has been used in the front
template of a
„[Die Kanji Lernen und Behalten](http://www.kanji-lernen.de/)“ deck,
the German version of “Remembering the Kanji”.

### Furigana, kanji and reading templates

The `{{furigana:Field NN}}`, `{{kanji:Field NN}}` and `{{reading:Field
NN}}` templates have been modified. The standard templates use ASCII
spaces (“ ”) and “>” characters to determine the beginning of the
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
* As the other functions, this works only on the desktop client.
