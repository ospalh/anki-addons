title: Colorful toolbars
id: colorbar
main_file: colorful_toolbars.py
type: addon
date: 2013-06-10
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
extra_jq_script: ct_tips.js

This add-on replaces the top menu bar with the “Decks Study Add
Browse” text buttons and the two rather drab sync and statistics
buttons with a colorful icon toolbar like the one in Anki 1.

The edit button and the more button in the bottom bar are also
replaced by an icon tool bar.

This also adds a few more menu items and adds icons to the menus (not on Macs).
The tool bars can be shown and hidden via the "View" menu, the “Decks
Study Add Browse” functions can also be reached through the "Go" menu.

## Menu-only items

Two items are added only to the menus, not to the icon bars:

In the “View” menu, there is a “Mute” switch. It works similar to the
“Automatically play audio” setting in the deck options (“General”
tab). Audio on the card is not played when the card is shown, but only
when <span class="qtbase or_replay_button">the replay button or the
“R” key</span> are pressed. This options works for all decks, and can
be switched on and off quickly.

The “Go” menu contains a “Last card” switch. When this is active,
rating an answer (clicking “Again”, “Good” &c.) goes back to the deck
overview screen.


## Variants

<figure style="width:562px;" class="clear">
  <img src="images/toolbar%20netbook.png" alt="Now the icon tool bars
  are at the left and right sides.">
  <img src="images/toolbar%20ospalh.png" alt="A few different icons
  appear in the top and bottom tool bars.">
  <figcaption>
    Two variants of the arrangement and selection of icons.
  </figcaption>
</figure>
The appearence can be changed by editing the add-on
 [source file](https://github.com/ospalh/anki-addons/blob/master/colorful_toolbars.py)
 by activating the “Tools/Add-ons/Colorful toolbars/Edit...” menu
item.

The file contains a switch to chage the add-on to “netbook”-mode. When
the `netbook_version = True` line is active the the two icon bars are
on the left and right, to preserve vertical screen space. To get to my
personal variant with different buttons in the bottom bar, take a look
at the git branch
[`develop-ospalh-special`](https://github.com/ospalh/anki-addons/blob/develop-ospalh-special/colorful_toolbars.py). Remember
to also get the
[icons directory](https://github.com/ospalh/anki-addons/tree/develop-ospalh-special/color_icons)
when you get the add-on from github.

There are also switches to show the “Mute” and “Last card” switches in
the bottom icon bar.

[UTSL](http://www.jargon.net/jargonfile/u/UTSL.html) for further
changes to the icons shown.

## Replacing icons

The icons used are stored in the folder
`Anki/addons/color_icons`. They can be simply replaced by icons more to the
personal taste of the user.

## What *is* the capital of Niue?

<figure><img src="images/Niue%20Alofi.png" alt="Anki
2. The review area reads Die Hauptstadt von Niue ist Alofi"> </figure>
[Alofi](http://en.wikipedia.org/wiki/Alofi).
