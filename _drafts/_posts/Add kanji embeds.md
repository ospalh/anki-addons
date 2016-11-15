title: Add kanji embeds
id: embed_kanji
main_file: add_kanji_embeds.py
date: 2013-06-07
tags: [svg, embed, abandoned]
layout: addon
status: hackish, one-off
status_color: red
status_text_color: white
abstract: "A quick hack to fill my collection with the code to display
SVG stroke order diagrams"
first_image: embed_暑.png
first_alt: 'A colored stroke order diagram of 暑 and the text <embed
width="200" height="200" title="Standard" src="暑.svg"></embed>'
first_caption: "Use <emded> tags to display SVGs."

This is a chimera of parts of my
[Kanji stroke color](Kanji%20stroke%20color.html) and Cayennens’
original
[Kanji Colorizer](https://ankiweb.net/shared/info/1964372878). When
triggered, the add-on goes through the collection and fills the right
fields with embed tags for my version of the SVGs of the colored
stroke order diagrams.

The SVGs themselves are not copied. The paths in the collection are
also wrong. I used it once to make my Kanji deck usable with an
unpatched AnkiDroid and am done with this now. It will stay in this
pretty much useless state.

The add-on may also need extra Python packages. See the
<q><a href="Batteries.html">Batteries</a></q> page for details on
this.
