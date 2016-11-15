title: Compare to kana
id: comparekana
main_file: compare_to_kana.py
layout: addon
date: 2015-10-16
status: working
status_color: green
status_text_color: white
abstract: "When typing in Japanese readings, remove the kanji bit from
the correct text, so that the red and green coloring of the answer
works correctly."
first_image: compare_to_kana.png
first_alt: "Three lines of Text: 1: Einwohner, Bürger: 住民 じゅうみん
　読み 2: じゅ-みん (kana in green, the dash in red) 3: じゅうみん (the
じゅ and みん in green, う in blue)"
first_caption: The typed-in answer was compared to the kana only.
ankiweb_id: 4091556602

A typical model for learning Japanese has a field called <q>Reading</q>. In
that field, the reading (kana) is stored *along with the kanji*. For
example, in a note defining the Japanese word for citizens, the
reading field would look like <q lang="ja">住民[じゃうみん]</q>. Like this, the
standard templates `{{furigana:Reading}}` and `{{kana:Reading}}` work.

<span class="clear" />
<figure>
<img src="images/compare_full_reading.png" alt="Same flash card as
above, but line 3 now reads 住民[じゃうみん], with everything but the
じゅ and みん in blue. Line 2 also shows more red hyphens.">
<figcaption>
The original comparison shows more text as incorrect than it should.
</figcaption></figure>

This set-up causes problems when you use the type-answer feature to
learn the reading of Japanese words. You type just the kana, but they
are then compared to the whole stored answer, including the kanji and
square brackets. When you type the answer correctly, a large part will
be marked in red. This add-on filters the text used as reference for
the typed text the same way the `{kana:NN}` template dose and compares
the typed text only with the kana part of the stored text.

## Setup

The kanji are removed when the model name contains the word <q>Japanese</q>
and the field name contains <q>Reading</q>. Use `{{type:Reading}}` or
`{{type:NN Reading}}` in your cards.

### CSS

The example images where taken with a somewhat complex note
type. Without further set-up, the background rather than the text of
the correct and wrong parts of the text is colored. To override this,
the following CSS was used:
<blockquote class=lsting><pre><code><span>.card {color: #657b83; background-color: #fdf6e3;}
\#typeans span {background-color: #fdf6e3;}
.typeBad {color: #dc322f;}
.typeMissed, .typePass {  color: #268bd2;}
.typeGood{color: #859900;} </code></pre></blockquote>

The basic color scheme is called
[Solarized](http://ethanschoonover.com/solarized).
