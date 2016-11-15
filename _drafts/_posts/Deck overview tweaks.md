title: Deck overview tweaks
id: deck_overview
main_file: deck_overview_tweaks.py
date: 2016-03-18
layout: addon
status: working
status_color: green
status_text_color: white
abstract: Show the learn count on the start screen
first_image: tweaked_deck_overview.png
first_alt: "The deck overview with New Learn and Due columns and a footer line with card count sums"
first_caption: Learn counts in the deck overview

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
