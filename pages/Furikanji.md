title: Furikanji
id: furikanji_and
main_file: Furikanji.py
type: addon
date: 2012-12-15
status: for desktop use only
status_color: yellow
status_text_color: black
abstract: "Improved way to parse kanji and readings, a way to render
kanji the kana and a few other display hacks."
first_image: furikanji.png
first_alt: "Sceenshot of text ふりがな with 振り仮名 as ruby."
first_caption: Furikanji demo
ankiweb_id: 2327947748

This add-on adds support for furikanji, adds two other templates and
slightly changes the way kanji and readings are parsed.

<blockquote class=nb>
This addon is for use with the desktop
client only. Using features of this add-on with mobile clients or
AnkiWeb may result in suboptimal layout.
</blockquote>

## Furikanji

The template `furikanji` uses a standard reading field to
render kanji *above* the kana. This is useful for listening comprehension.

To use this, put  `{{furikanji:Field name}}` instead of
`{{furigana:Field name}}` in the template.

The ruby element has the additional class `furikanji`. So special
styling can be added. For example, markers that show the beginning and
end of a specific block.

<figure>
<img src="images/furikanji-desktop.png" alt="Text: 起きなよいい加減お
with きなよいいかげん as ruby and きなよいいかげん with 起きなよいい加
減お as ruby. The kanji of the ruby are marked with vertical bars.">
<figcaption>
Example use of furigana and furikanji. The source of the text is an
Anki-2-ified version of the <a
href="http://subs2srs.sourceforge.net/">sub2srs</a> example deck 「時
を掛ける少女」.
</figcaption>
</figure>
To use furikanji, with the markers shown, i use
<blockquote class=lsting><pre><code>.redish { color: #a00;}
body:not(.mobile) .furikanji:before, body:not(.mobile) .furikanji:after {
    font-size: 50%;
    position: relative;
    bottom: 2rem;
    width: 0px;
    vertical-align: baseline;
}
body:not(.mobile) .furikanji:before { content : "|"}
body:not(.mobile) .furikanji:after { content : "|"}
.mobile .furikanji {color: #268bd2;}</code></pre></blockquote>
as styling and
<blockquote class=lsting><pre><code>&lt;div>{{Image}}&lt;/div>
{{Audio}}
&lt;div class="nhg lnsz">{{furigana:Reading}}&lt;/div>
&lt;div class="nhg redish lnsz">{{furikanji:Reading}}&lt;/div></code></pre></blockquote>
as back template. The `body:not(.mobile)` bit of the selector and the
setting for `.mobile` can be dropped when not using the
[AnkiDroid patch](#droid).

<figure>
<img src="images/furikanji-web.png" alt="Text: 起きなよいい加減お with
with きなよいいかげん as ruby and 起[お]きなよいい 加減[かげん], with square brackets.">
<figcaption>
On AnkiWeb, the furikanji don’t work.
</figcaption>
</figure>
As the furikanji rendering is done on the fly by the desktop client,
it naturally does not work with AnkiWeb or AnkiDroid (or, presumably,
the iOS client). Here the text is rendered as it is seen in the edit
screen, with the square brackets.

### <span id="droid">Ospalh-special</span>

<figure>
<img src="images/furikanji-mydroid.png" alt="Text: 起きなよいい加減お
with きなよいいかげん as ruby and きなよいいかげん with 起きなよいい加
減お as ruby. The kanji of the ruby are marked in orange.">
<figcaption>
AnkiDroid can be patched to use furikanji.
</figcaption>
</figure>
Daring spirits can take a look at
[my version](https://github.com/ospalh/Anki-Android/blob/ospalh-special/src/com/ichi2/libanki/hooks/FuriganaFilters.java)
of the furigana filters in
[AnkiDroid](https://github.com/nicolas-raoul/Anki-Android).  I have
added the equivalent of this addon, providing furikanji on
AnkiDroid. Unfortunately i forgot to put this change in an extra
branch. As i have made a number of other changes to my branch of the
program, you should probably just copy over this single file into your
own version. (I was unable to get the furikanji marked with the
horizontal bars as shown in the desktop client. I mark them with color
instead.)


## Boxed and boxkana

<figure>
<img src="images/boxed.png" alt="Text: ausruhen and やすむ, the やす
is surrounded by a dashed line.">
<img src="images/boxkana.png" alt="Text: ausruhen and やすむ, the やす
is shown as ruby above a dashed box.">
<figcaption>Two ways to show the reading of a
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

These effects can be achieved by applying the formating set in the
[source file](https://github.com/ospalh/anki-addons/blob/master/Furikanji.py)
directly, together with `{{kana:Field NN}}`. The simple box should work
everywhere, the boxkana should work on AnkiDroid, and possibly in
AnkiWeb, when the web browser supports `<ruby>` tags.

## Furigana, kanji and reading templates

The `{{furigana:Field NN}}`, `{{kanji:Field NN}}` and `{{kana:Field
NN}}` templates have been modified. The standard templates use ASCII
spaces (“ ”) and “>” characters to determine the beginning of the
kanji text. The modified version treats only characters in the word
character class as kanji.

This means that commas, newlines,
[CJK](http://en.wikipedia.org/wiki/CJK_characters)
[spaces](http://www.fileformat.info/info/unicode/char/3000/index.htm)
&c. can be used as separators between kanji and other, preceding text.

The addon also adds the class `furigana` to the ruby element.

### Limitations

* Leading kana are not automatically separated. For example the
  reading for 「お釣り」 must still be written with an ASCII space or
  other separator between the 「お」 and the 「釣」: 「お 釣[つ]り」.
* This mechanism only work with Python version 2.7.
* As the other functions, this works only on the desktop client.
