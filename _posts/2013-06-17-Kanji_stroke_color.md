---
title: Kanji stroke color
main_file: kanji_stroke_color.py
layout: addon
permalink: Kanki_stroke_color.html
status: broken, abandoned
status_color: red
status_text_color: white
abstract: A quick hack add-on to show (colored) stroke order diagrams.
first_image: stroke%20color.png
first_alt: "The word Zustand: and a colored stroke order diagram for 況"
first_caption: Write 況 in this order.
---
Show colored stroke order diagrams on the desktop client, including
variants.

## Alternatives

This add-on serves a similar purpose as
[Cayennes](http://cayennes.github.io)’
[Kanji colorizer](https://ankiweb.net/shared/info/1964372878). (View
the code on [GitHub](https://github.com/cayennes/kanji-colorize/).)

### Pros for this add-on
* Can show stroke variants
* Does not need another field in the model
* Keeps the collection.media folder clean.

### Cons

* With this add-on, the core function, color, is not working on
  AnkiWeb/AnkiDroid/AnkiMobile.
* Installing the add-on is somewhat tricky.

<blockquote class="nb">
This add-on needs extra Python packages. See the
<q><a href="Batteries.html">Batteries</a></q> page for details.
</blockquote>



### Other alternative

I have personally given up use of this add-on. While i still like my
way of coloring the diagrams, with the actual colors defined via CSS,
i did not like the changes to AnkiDroid needed.

I have now copied the SVGs to the media folder and added the kanji –
with variants in an extra field – to my collection with the even more
hackish/broken [Add kanji embeds](Add_kanji_embeds.html) add-on.

## Usage

<blockquote class="nb">
The user has to generate the kanji diagrams emself and put them into the add-on directory, into a <q><code>stroke-order-kanji</code></q> folder
</blockquote>


Use the template <q>`kanjiColor`</q> to see the diagrams. In the
template editor in the (front or back) template, where it says
<q>`{%raw%}{{Kanji}}{%endraw%}`</q>, change it to
<q>`{%raw%}{{kanjiColor:Kanji}}{%endraw%}`</q>. When you use another
field name for you kanji, use that instead.

## Variants

There are three more templates, that show variant stroke order
diagrams:

### kanjiColorJinmei and kanjiColorKaisho

Using either <q>`{%raw%}{{kanjiColorJinmei:Kanji}}{%endraw%}`</q> or
<q>`{%raw%}{{kanjiColorKaisho:Kanji}}{%endraw%}`</q>, the Jinmei or Kaisho variant drawings
are shown, using the normal version when there is no variant.

### kanjiColorRest

<figure>
<img src="images/three_旺.png" alt="A larger colored  stroke order diagram of
旺. Below two smaller diagrams of that character. In the bottom
diagrams the third stroke is shorter. The bottom left diagram shows
the vertical stroke on the right drawn last.">
<figcaption>For <q lang="ja">旺</q>, there are two variant forms.</figcaption>
</figure>

Using <q>`{%raw%}{{kanjiColorRest:Kanji}}{%endraw%}`</q> displays all variants of a given
kanji, and nothing when there is no variant. The variants are also
drawn smaller.


## Changing properties

### Size

The size of the displayed diagrams can be changed in the add-on’s
[source file](https://github.com/ospalh/anki-addons/blob/master/kanji_stroke_color.py).
Use the <q>Tools/Add-ons/Kanji stroke color/Edit...</q> menu item to
open it. Set the size in the line <q>`kanji_size = 200`</q>. The size
of the variants shown with the <q>kanjiColorRest</q> can be set in the
<q>`rest_size = 120`</q> line.

### Colors

In the `addons` folder, there is a sub-folder named
`stroke-order-kanji`, that contains the file `_kanji_style.css`, along
with the kanji SVG files. Change the colors in this file. Use a text
editor like Wordpad, a local CSS file editor or a web service like
[CSSColorEditor](http://css-color-replace.orca-multimedia.de/).

The kanji diagrams use different CSS classes. The strokes and stroke
numbers have classes `stroke_numN` (`stroke_num1`, `stroke_num2`,
...). The strokes have the class `stroke_path`, the numbers,
`stroke_number`.

Some stroke groups also have classes. Open an SVG
file in a text (XML) editor for details. These classes are used for
the shadow effect below.

### Other effects

The SVG files load and run the script file `_kanji_script.js` from the
`stroke-order-kanji` folder. This files does nothing in the standard
installation. There is also a file `_kanji_script_shadow.js`, that
adds a shadow effect to the strokes, when renamed, where the shadow
color indicates the group. This file can be used as an inspiration or
as the basis for other effects. Animations seem possible.

<blockquote class="nb">The shadow effect may not work correctly on all
operating systems.</blockquote>

When you try the shadow effect file and the results look ugly, copy
back the original
[`_kanji_script.js`](https://raw.github.com/ospalh/kanji-colorize/etree/kanjicolorizer/extra/_kanji_script.js)
file.
