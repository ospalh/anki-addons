title: Add note id
id: add_nid
main_file: Add%20note%20id.py
type: addon
date: 2012-12-21
status: working
status_color: green
status_text_color: white
abstract: "The first field of cards should be unique. To make sure
this is the case, this add-on adds a unique number to fields called
`Note ID`."
subtitle: Make all cards unique
first_image: Note%20ID.png
first_caption: "Name the first field is called Note ID"
first_alt: "Name the first field is called Note ID"
ankiweb_id: 1672832404

A fix to the problem of synonyms.

When adding new cards, the first field must be unique. But what about
synonyms? Of course it is possible to add an explanation to the word
to specify which is the meaning in this case. But a more elegant
way is to add more fields to show which is the correct meaning in this
case, for example with an example sentence.

The solution is to add the number that Anki uses internally to
identify the note to the note itself.

To use, the first field in the card model must be named "Note ID".
Then, when adding content, this field is automatically filled with the
note id when you move the cursor to another field.


## Menu
There is also an item in the Tools menu that goes through the whole
collection and adds note ids to all empty Note ID fields. This is
useful when adding the field to decks you already
have. ([UTSL](http://www.jargon.net/jargonfile/u/UTSL.html) to hide the
menu item.)
