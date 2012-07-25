title: Add note id
id: add_nid
main_file: Add note id.py
date: 2012-06-18
tags: [field, add, unique, nid]
type: addon
status: working
status_color: green
status_text_color: white
abstract: The first field of cards should be unique. To make sure this is the case, this add-on adds a unique number to fields called `Note ID`.
first_image: Note ID.png
first_alt: The first field is called Note ID

A fix to the problem of synonyms.

When adding new cards, the first field must be unique. But what about
synonyms? Of course it is possible to add an explanation to the word
to specify which is the meaning in this case. But a more elegant
way is to add more fields to show which is the correct meaning in this
case, for example with an example sentence.

The solution is to add the number that Anki uses internally to
identify the note to the note itself.

To use, the first field in the card model must be named "Note ID"

Add the nid (note id) to a field named "Note ID" when adding or
editing notes, when that field loses focus. When the “Note ID”
field is the first field, this automatically satisfies the rule
that the first field has to be unique.  That means the “real”
fields with interesting content don’t have to be
unique. (Personally, for synonyms i like to have the same content
in the “Expression” or “Meaning” fields, and then put further
information in note or disambiguation fields.)
