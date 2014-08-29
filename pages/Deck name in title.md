title: Deck name in title
id: title
main_file: deck_name_in_title.py
status: working
type: addon
date: 2013-05-07
status_color: green
status_text_color: white
abstract: "Show the name of the deck you are currently learning in the
window title."
first_image: deck_title.png
first_alt: "A window title: “Lernen::1 日本語::1 和独::VHS – Anki”"
ankiweb_id: 3895972296
extra_jq_script: dit_tips.js

Show the name of the deck you are currently <span class="qtbase
andprofile">learning</span> in the window title.

Taking a hint from some other applications, the <span class="qtbase
orprofile">deck</span> name name is shown *before* the application name.

### Setup

The behavior of the add-on can be changed in a few points by editing
the
[source file](https://github.com/ospalh/anki-addons/blob/master/deck_name_in_title.py):

* title_separator: What to print between the deck name and program
  name. Normally a spaced n-dash.
* show_subdeck: Whether to show the subdeck you have descended into
  during learning or only the deck you clicked on in the deck
  browser.
* subdeck_format: How the point between the selected deck and the one
  descended into is marked. Standard is an en-dash between the two
  colons.
