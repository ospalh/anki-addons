---
title: Replay buttons on card (PNG)
main_file: png_play_button.py
permalink: Play_button_png.html
tags:
 - review
 - replay
 - button
layout: addon
status: obsolete
status_color: rod
status_text_color: white
abstract: "Show a replay button for each file on a card."
first_image: play_buttons.png
first_alt: "Flash card with text and play buttons."
# ankiweb_id: 498789867
---

Simple add-on that adds play buttons to the cards for audio and video
files.

With this it is possible to replay individual files. For example just
the pronunciation of a word, or just one example sentences.

<blockquote class="nb">This add-on has been superseded by the <a href="Play_button.html">play button</a> add-on.</blockquote>

This is in Anki 2.0 style, and will not be updated.

## Installation

To install this add-on, copy the
[source file](https://github.com/ospalh/anki-addons/blob/develop/png_play_button.py)
to your `addon` folder and add the image file to your
`collection.media` folder as `_inline_replay_button.png`. (It is
called
[`replay.png`](https://github.com/ospalh/anki-addons/blob/develop/color_icons/replay.png)
on github.)

## Old style

This add-on is an older version of the [play button](Play_button.html)
add-on, and uses a PNG image as the button. The button image is the
same as the one used on older versions of AnkiDroid.

The add-on sets a maximum size for the button, because it will look
fuzzy when scaled up too much. UTSL to change the allowed maximum
size.

## Browserhide

<span  class="clear" />
<figure>
<img src="images/browserhide.png" alt="Part of the Anki review window.
Text: みんなの日本語： にんぎょう.  Below part of the Anki card
browser. One line highlighted. Text: 人形; Japanisch-De...; にんぎょう">
<figcaption>The text <q lang="ja">みんなの日本語：</q> is shown on the card,
but not in the browser.</figcaption>
</figure>
The add-on also hides text with the CSS class `browserhide` in the
card browser. With its help the name of sound and video files is shown in
the card browser instead of the file name of the replay arrow
image. The class is useful for cards where there is a text repeated
for every card, too. Put text  parts of your card template that
should not appear in the card browser into spans with the class `browserhide`.

The effect of the `browserhide` class is similar to using the
<q>Browser Appearance</q> feature hidden in the <q>More</q> button of
the template editor.

There is another add-on that implements *only* this hiding of text in
the text browser, called [Lean browser qa](Lean_browser_qa.html).
