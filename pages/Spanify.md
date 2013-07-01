title: Spanify text
id: spanify
main_file: spanify.py
date: 2013-06-19
type: addon
status: hackish
status_color: yellow
status_text_color: black
abstract: Add buttons to the note editor to wrap text in spans.
first_image: s1s2s3.png
first_alt: "The Anki note editor button row has s1, s2 and
s3 buttons."
first_caption: Three new buttons.

Another add-on to add buttons to the note editor. This adds buttons to
wrap text in spans.

By default there are three buttons, “s1”, “s2” and “s3”, that wrap the
text selected in a note’s field in `<span class="sN">`/`</span>`
tags. (`N` = 1, 2, 3). It is up to the user to set up the card
styling to make use these classes.

<blockquote class="nb">
The changes made by the add-on are invisible in the card editor, and
on the cards, unless styling for the classes is added.
</blockquote>

This add-on is based on Thomas Tempé
[strikethrough button](https://ankiweb.net/shared/info/999886206)
add-on.
