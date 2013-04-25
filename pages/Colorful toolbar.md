title: Colorful toolbar
id: colorbar
main_file: Colorful%20toolbar.py
type: addon
date: 2013-01-15
status: working
status_color: green
status_text_color: white
abstract: "Replace the top menu bar with the “Decks Study Add Browse”
text buttons and the two rather drab sync and statistics buttons with
a colorful icon toolbar like the one in Anki 1."
subtitle: Get back the Anki1 look
first_image: Colorful%20toolbar.png
first_alt: "Anki 2 review window with two icon bars. The review area
reads Die Hauptstadt von Niue ist"
ankiweb_id: 388296573

Replace the top menu bar with the “Decks Study Add Browse” text
buttons and the two rather drab sync and statistics buttons with a
colorful icon toolbar like the one in Anki 1.

The edit button and the more button in the bottom bar are also
replaced by an icon tool bar.

This also adds a few more menu items and adds icons to the menus (not on Macs).
The tool bars can be shown and hidden via the "View" menu, the “Decks
Study Add Browse” functions can also be reached through the "Go" menu.

## Last card

The add-on has one feature that is normally hidden: a last card
button.

When the button between the “mark” and “bury” buttons has been clicked
and the arrow is green instead of gray, clicking on one of the answer
buttons (“Again”, “Good” &c.), takes you to the deck options screen
instead of showing another card.

To show this button, edit the add-on
[source](https://github.com/ospalh/anki-addons/blob/master/Colorful%20toolbar.py)
by activating the “Tools/Add-ons/Colorful toolbars/Edit...” menu item.

Remove the `#` and the space at the beginning of the  `#
show_toggle_last = True`-line  and add a `#` (and a space) to the
`show_toggle_last = False` line. Click “Save” and restart Anki.


## Variants

<figure style="width:562px;" class="clear">

<img src="images/toolbar%20netbook.png"
alt="Anki 2 with the tool bar at the left and right.  The review area
reads Die Hauptstadt von Niue ist">
<img src="images/toolbar%20ospalh.png"
alt="Anki 2 with a study icon and an undo icon.  The
review area reads Die Hauptstadt von Niue ist">
<figcaption>
    Two variants of the arrangement and selection of icons.
    </figcaption>
</figure>
Apart from the standard version, there is a
[netbook version](https://ankiweb.net/shared/info/1330596667)
on the AnkiWeb
[download page](https://ankiweb.net/shared/addons/), that places
the two icon bars to the left and right, to preserve vertical screen
space. On GitHub, there is also a branch and package named
[`ospalh-special`](https://github.com/downloads/ospalh/anki-addons/colorful_toolbar_ospalh-special.zip)
with a slightly different icon selection more to my personal taste.


[UTSL](http://www.jargon.net/jargonfile/u/UTSL.html) for further
changes to the icons shown.

## Replacing icons

The icons used are stored in the folder
`Anki/addons/color-icons`. They can be simply replaced by icons more to the
personal taste of the user.

## What *is* the capital of Niue?

<figure><img src="images/Niue%20Alofi.png" alt="Anki
2. The review area reads Die Hauptstadt von Niue ist Alofi"> </figure>
[Alofi](http://en.wikipedia.org/wiki/Alofi).
