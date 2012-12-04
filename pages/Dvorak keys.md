title: Dvorak keys
id: dvorak
main_file: Dvorak%20keys.py
status: working
type: addon
status_color: green
status_text_color: white
abstract: "Use keys easy to use for user of the <a
href=\"http://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard\">Dvorak
simplified keyboard</a> to answer a question."
first_image: Dvorak_keys.png
first_alt: "Colorcoded sketch of a keyboard and hands. The colors show
which finger to use for which key. Some keys are marked as described
in the text."
first_caption: The keys to use.
ankiweb_id: 2714331040
extra_jq_script: dvorak_tips.js

Use keys easy to use for user of the <a
href="http://en.wikipedia.org/wiki/Dvorak_Simplified_Keyboard">Dvorak
simplified keyboard</a> to answer a question.

The point is to remember the key positions, rather than the characters
the keys usually produce.

There are three sets of keys to use, with the four typing fingers of the
left hand in the row above the home row, going from “again” with the
<span class="qtbase pinky">little finger</span>, through “hard”
with the ring finger, “good” for the middle finger to “easy” for the
index finger.

The second set is in the home position. Left index finger for “again”
and three fingers of the right hand: index finger for “hard”, middle
finger for “good” and ring finger for “easy”.

The third set is similar to the first set, but in the bottom row,
here, too, going from <span class="qtbase pinky">little finger</span>,
“again”, to the index finger, “easy”. (Some (German? international?)
keyborads have a small left shift key and an extra key for “<” and
“>”. That key is skipped.) (The idea for this set of keys came from
Peter Horwood, (“Madman Pierre”), who has released
[his own add-on](https://ankiweb.net/shared/info/3196965470) which
does this remapping.)

These keys were selected so that they don't clash with other functions
like add card or edit card.


## Configuration

The keys that are used are defined in a Python dictionary. Read the
comments in the
[source file](https://github.com/ospalh/anki-addons/blob/master/Dvorak%20keys.py)
for details.

I tried to find good keys to use for QWERTY keyboards, but
couldn't. My best idea was to use the four keys for the index fingers,
in the home positions or reaching towards each other. These are there
in a commented-out alternative version of the dictionary.
