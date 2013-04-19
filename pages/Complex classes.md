title: Complex use of classes
id: crazy_classes
type: subpage
ankiweb_id: 2327947748
parent: Furikanji
extra_jq_script: class_tips.js

These are examples of more creative use of the classes added by the
Furikanji add-on.

## Markers for furikanji

I use markers that show the beginning and end of a specific block of
readings:

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
[AnkiDroid patch](Furikanji.html#droid).


## Separator for kana

Some people like to use the interpunct <span class="qtbase
nakaguro"><q
lang='ja'>[・](http://www.fileformat.info/info/unicode/char/30fb/index.htm)</q></span>
to separate the kana for different kanji. For example, for the word <q
lang='ja'>中黒</q> the text <q lang='ja'>`なか・ぐろ`</q> is used in a
reading field.

An alternative is to use the
[Japanese Support](https://ankiweb.net/shared/info/3918629684) addon
to automatically generate readings. They are usually by word, and have
to be rearranged slightly by hand. In the example, you would type the
kanji<q lang='ja'>中黒</q> into the “Expression” field. With a tab or mouse click,
the “Reading” field would be filled with <q lang='ja'>中黒[なかぐろ]</q>. For this
trick to work, this string would have to changed to <q lang='ja'>中[なか]黒[ぐろ]</q>
by hand, by adding an extra pair of square brackets and dragging
the<q lang='ja'>なか</q> into them.

The adding of the interpunct can be done using two CSS pseudo-classes,
“`:after`” and “`:last-child`”:
<blockquote class=lsting><pre><code>&lt;div class="interpuncts">{kana:Reading}}&lt;/div></code></pre></blockquote>

<blockquote class=lsting><pre><code>.interpuncts .kana:after{content:"・";}
.interpuncts .kana:last-child:after{content: none;}</code></pre></blockquote>

The advantage of this method over using a pure kana is that with this
method furigana can be used as well, with “`{{furigana:Reading}}`”.

## Furigana on hover

This method works without this add-on as well.

To show furigana only when the mouse hovers above it use:
<blockquote class=lsting><pre><code>&lt;div class="kanjihover">{{furigana:Reading}}&lt;/div></code></pre></blockquote>

<blockquote class=lsting><pre><code>.kanjihover rt{visibility: hidden;}
.kanjihover ruby:hover rt {visibility: visible;}</blockquote></pre></code>

or to activate this for all furigana everywhere, drop the extra class:

<blockquote class=lsting><pre><code>{{furigana:Reading}}</code></pre></blockquote>

<blockquote class=lsting><pre><code>rt{visibility: hidden;}
ruby:hover rt {visibility: visible;}</blockquote></pre></code>
