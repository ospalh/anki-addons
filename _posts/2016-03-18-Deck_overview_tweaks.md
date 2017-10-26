---
title: Deck overview tweaks
main_file: deck_overview_tweaks.py
permalink: Deck_overview_tweaks.html
layout: addon
status: update-planned
status_color: yellow
status_text_color: black
abstract: Show the learn count on the start screen
first_image: tweaked_deck_overview.png
first_alt: "The deck overview with New, Learn and Due columns and a footer line with card count sums"
first_caption: Learn counts in the deck overview
---

<blockquote class="nb">This is an Anki 2.0 plugin. I think i will
update it to 2.1, but don’t know when i will get around to it. If you
are impatient, you can of course do the update yourself. Please let me
know which way you want your version published.</blockquote>

An add-on to show the learn count on the deck overview screen. With
this, Anki desktop is more in line with AnkiDroid.

You also get a footer line with the sums of the new, learn and due
counts, and of the total count of cards due. The last number is,
again, something AnkiDroid shows you, but the other Anki versions
don’t.

The first section of the Python file gives you the options to modify
the appearance of the deck list a bit more. For example the symbols
used for decks with subdecks shown, with subdecks hidden, or without
subdecks can be changed. I personally like some symbol, like a bullet
(<q>•</q>) for decks without subdecks, so the indentations match, but
this is not standard. To show this bullet, the
<q>`no_subdeck_bullet`</q> string can be changed to that
character. Edit the add-on file through the Tools→Add-ons… menu
item. The color and styling of the counts shown can be changed similarly.
