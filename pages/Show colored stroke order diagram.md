title: Show colored stroke order diagrams
id: csod
main_file: Show%20colored%20stroke%20order%20diagram.py
status: abandoned
type: addon
status_color: red
status_text_color: white
abstract: "Another take on displaying the KanjiVG stroke order
diagrams with color. Not much more than an idea how to go about it at
the moment."
first_image: palette_gimped.png
first_alt: The idea is to pick the stroke colors from an image file.

This was an idea about an add-on that might have replaced my
[Kanji stroke color](Kanji%20stroke%20color.html) add-on

## Goals

### One xml file

The idea was to put all kanji stroke data svg into a single XML file
and to extract svgs from that and colorize them the fly.

There wasn't really much reason for this. So i won't do it.

### Different colors at different times.

I wanted to make it possible to use different colors at different times, by
using an image as template.

The newest version of
[Kanji stroke color](Kanji%20stroke%20color.html) offers the
possibility to change the colors. Not through an image template but
through the css file [`_kanji_style.css`](https://github.com/ospalh/anki-addons/blob/master/stroke-order-kanji/_kanji_style.css).

### Other effects

Add other effects, such as shadows, or possibly animation, on the
fly. Again, with different parameters at different times.

Dto. Put effects into
[`_kanji_script.js`](https://github.com/ospalh/anki-addons/blob/master/stroke-order-kanji/_kanji_script.js). Look
at
[`_kanji_script_shadow.js`](https://github.com/ospalh/kanji-colorize/blob/etree/kanjicolorizer/extra/_kanji_script_shadow.js)
for an idea how to indicate the groups with colored
shadows. Unfortunately this appears to not work correctly on Macs.

## Data set

This uses – or would have used – the
[KanjiVG](http://kanjivg.tagaini.net/) kanji stroke order data set as
the base.
