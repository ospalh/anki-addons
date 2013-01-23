title: Deck name in title
id: title
main_file: Deck%20name%20in%20title.py
status: working
type: addon
date: 2012-07-31
status_color: green
status_text_color: white
abstract: "Show the name of the deck you are currently learning in the
window title."
first_image: deck_title.png
first_alt: "A winwodw title: “Lernen::1 日本語::1 和独::VHS – Anki”"
first_caption: The window title shows a deck name.
ankiweb_id: 3895972296

Show the name of the deck you are currently learning in the window
title.

When there is more than one profile, it also shows the current profile name.

### Setup

The behavior of the add-on can be changed in two points by editing
the
[source file](https://github.com/ospalh/anki-addons/blob/master/Deck%20name%20in%20title.py):

* title_separator: What to print between the deck name and program
  name. Normally a spaced n-dash.
* show_subdeck: Whether to show the subdeck you have descended into
  during learning or only the deck you clicked on in the deck
  browser.
