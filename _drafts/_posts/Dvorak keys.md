title: Dvorak keys
id: dvorak
main_file: dvorak_keys.py
status: working
layout: addon
date: 2013-05-07
status_color: green
status_text_color: white
abstract: "Use keys easy to use for user of the <a
href=\"http://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard\">Dvorak
simplified keyboard</a> to answer a question."
first_image: Dvorak_keys.png
first_alt: "Sketch of a keyboard and hands. Some keys are marked as described
in the text."
first_caption: The keys to use.
ankiweb_id: 2714331040
extra_jq_script: dvorak_tips.js

Use keys easy to use for user of the <a
href="http://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard">Dvorak
simplified keyboard</a> to answer a question.

The point is to remember the key positions, rather than the characters
the keys usually produce.

There are three sets of keys to use. The first is with the four typing
fingers of the left hand in the row above the home row, going from
<q>again</q> with the <span class="qtbase pinky">little finger</span>,
through <q>hard</q> with the ring finger, <q>good</q> for the middle finger to
<q>easy</q> for the index finger.

The second set is in the home position. Left index finger for <q>again</q>
and three fingers of the right hand: index finger for <q>hard</q>, middle
finger for <q>good</q> and ring finger for <q>easy</q>.

The third set is similar to the first set, but in the bottom row,
here, too, going from <span class="qtbase pinky">little finger</span>,
<q>again</q>, to the index finger, <q>easy</q>. (Some (German? international?)
keyboards have a small left shift key and an extra key for <q><</q> and
<q>></q>. That key is skipped.) (The idea for this set of keys came from
Peter Horwood, (<q>Madman Pierre</q>), who has released
[his own add-on](https://ankiweb.net/shared/info/3196965470) which
does this remapping.)

These keys were selected so that they don't clash with other functions
like add card or edit card.


## Configuration

The keys that are used are defined in a Python dictionary. Read the
comments in the
[source file](https://github.com/ospalh/anki-addons/blob/master/dvorak_keys.py)
for details.

I tried to find good keys to use for QWERTY keyboards, but
could not. My best idea was to use the four keys for the index fingers,
in the home positions or reaching towards each other. These are there
in a commented-out alternative version of the dictionary.
