title: Quick note and deck buttons
id: quick_buttons
main_file: "Quick note and deck buttons.py"
status: working
type: addon
date: 2013-01-23
status_color: yellow
status_text_color: black
abstract: Quickly select a few models or decks.
first_image: quick_buttons.png
first_alt: The top of the add card dialog with a few extra buttons
first_caption: Select your favourite model or deck.

This add-on adds a few buttons to the right of the select note type
button and the select deck button at the top of the add card dialog.

Click on them to select your favourite model or note type.

<blockquote class="nb">You will have to modify the add-on source to
adapt this to your deck and model names.</blockquote>

## Setup

After downloading, you have to modify the `Quick note and deck
buttons.py` file. Trigger the “Tools/Add-ons/Open Add-ons
Folder...” menu item, pick out that file and open it with your
favourite source editor or trigger “Tools/Add-ons/Quick note and deck
buttons/Edit...” to use Anki’s built-in editor.

There are two bits of code that should be changed, marked with the
commets `# Set up here...` and `# ... and here ...`. A knowledge of
[Python](http://www.python.org/)
[syntax](http://docs.python.org/2/tutorial/index.html) may be helpful
to set this up, but following the examples and only changing text
inside of quotation marks should work.

### Lists of dictionaries

The parts that should be changed are called
[lists](http://docs.python.org/2/tutorial/introduction.html#lists) of
[dictionaries](http://docs.python.org/2/tutorial/datastructures.html#dictionaries). The
lists are marked with square bracktets, `[` and `]`, the dictionaries
with curly braces, `{` `}`. Each dictionary describes one button.

Each of these button dictonaries must contain at least two key-value
pairs:

* A `"label"`. The vaule after the `:` sets up the name shown in the
  button. Use quotation marks with an extra `u` before them to define
  a unicode string. I would suggest using short texts, such as single
  characters.
* A `"name"`. This is the name of the model for dicts in the
  `model_buttons` list and the name of the deck in the `deck_buttons`
  list. Make sure that these names are correct. Cut-and-paste
  the names if possible.


For more options read the comments in the
[source file](https://github.com/ospalh/anki-addons/blob/master/Quick%20note%20and%20deck%20buttons.py).

## Notes

<blockquote class="nb">At the moment, it looks ugly on
Macs.</blockquote>

This add-on is an expansion of the Quick change Note buttons add-on. The code
is based on that version, by Steve AW. Many thanks, for the code and
also for the idea in the first place.
