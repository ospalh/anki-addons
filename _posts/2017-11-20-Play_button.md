---
title: Replay buttons on card
main_file: play_button.py
permalink: Play_button.html
tags:
 - review
 - replay
 - button
layout: addon
status: working (basic)
status_color: green
status_text_color: white
abstract: "Show a replay button for each file on a card."
first_image: SVG_buttons_solarized.png
first_alt: "Flash card with text and play buttons."
ankiweb_id: 498789867
---

Simple add-on that adds play buttons to the cards for audio and video
files.

With this it is possible to replay individual files. For example just
the pronunciation of a word, or just an example sentences.

The button is created as inline SVG and copies the look of the replay
button of newer AnkiDroid versions. The minimum size is set to
12 pixel, otherwise the button is the same size as the text.

The old Anki 2.0 version worked in the card layout editor and the
preview as well. The new Anki 2.1 version works only during reviews so
far. I think i’ll update the other add-ons before i go back to
this. So replay there may take a while.

<span  class="clear" />

## Styling

<figure>
<img src="images/þéttbýll.png" alt="Anki review window. Large text “þéttbýll
” with a “play” button of the same size and small text “urban” with a small, red play button.">
<figcaption>The replay button can be styled via CSS.</figcaption>
</figure>

The buttons are created on the fly, and their appearance can be
changed via the card templates. It is somewhat tricky to get CSS
right. As an example that can be copied and adapted, to turn only one
replay button red, wrap the field in a span with a class like
`red_button` in the “Front Template” or “Back Template” of the card

{%raw%}
```html
<span class="red_button">{{Audio}}</span>
```
{%endraw%}

Then set `fill` to `red` for `.red_button .replaybutton span svg` in
“Styling”:

```css
.red_button .replaybutton span svg {
  fill: red;
}
```

This kind of styling should be done when using the
[night mode](Local_CSS_and_DIY_night_mode.html) add-on, or you may end
up with black replay buttons on a black background.

<figure>
<img src="images/urban_shadow.png" alt="“urban” and a red play button
with a shadow effect">
</figure>

On some platforms, CSS filters may work. For example this:

```css
.red_button .replaybutton span svg {
  fill: red;
  -webkit-filter: drop-shadow( 5px 5px 2px #f88 )
}
```
might be used to add a shadow effect.

<span  class="clear" />

## Card browser

The replay button is not shown in the card browser. Instead the sound file names are added to its  list section in the way they are entered into the cards, as `[sound:NN.mp3]` or similar.

At leas that is the idea. I am not sure about this browser hide functionality on Anki 2.1. The same caveat as above applies.
