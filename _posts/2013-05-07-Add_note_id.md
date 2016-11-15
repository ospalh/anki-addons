---
title: Add note id
permalink: Add_note_id.html
main_file: add_note_id.py
layout: addon
status: working
status_color: green
status_text_color: white
abstract: >
  The first field of cards should be unique. To make sure this is the
  case, this add-on adds a unique number to fields called <code>Note ID</code>.
subtitle: Make all cards unique
first_image: Note%20ID.png
first_caption: "Name the first field “Note ID”"
first_alt: "Name the first field “Note ID”"
ankiweb_id: 1672832404
---
A fix to the problem of synonyms.

When adding new cards, the first field must be unique, but what about
synonyms? Of course it is possible to add an explanation to the word
to specify which is the meaning in this case. A more elegant
way is to add more fields to show which is the correct meaning in this
case, for example with an example sentence.

The solution is to add the number that Anki uses internally to
identify the note to the note itself.

The note id field is also useful when editing the data outside of Anki
(text export, edit, text import). With the add-on, Anki can reliably
match the notes on reimport, even when the first <q>interesting</q> field
changed.

To use, the first field in the card model must be named <q>Note ID</q>.
Then, when adding content, this field is automatically filled with a
number based on the note id when you move the cursor to another field.

## Menu
There is also an item in the Tools menu that goes through the whole
collection and adds note ids to all empty Note ID fields. This is
useful when adding the field to decks you already
have. ([UTSL](http://www.jargon.net/jargonfile/u/UTSL.html) to hide the
menu item.)
