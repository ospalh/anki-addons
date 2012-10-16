title: Scalar
id: scalar
main_file: Scalar.py
type: addon
status: working
status_color: green
status_text_color: white
abstract: Compare a typed in number with the correct answer as a number, not as a string of digits. Color it yellow when it is close to the right number.
first_image: scalar.png
first_alt: The numbers are compared as numbers, not as single digits.
ankiweb_id: 333346658

When learning some types of numbers, like the number of inhabitants of
a country, often close is good enough. This add-on makes Anki show
that, it colours the answer in yellow when it was close to the
original answer.

#### Example
In the image correct answer is “48”, when you know it’s close to 50,
you type that. The original behaviour was to compare character by character,
and show the typed answer in red, a 5 is no 4 and a 0 is no 8. With this add-on, the whole answer
would be yellow, as it is  close to the correct answer.

On the
other hand, if you had typed  “400” as the answer, with the original
behaviour, you would get the “4” in green and “00” in red, showing more
green, even though the answer is farther from the correct one than the
“50”.

With this add-on the 400 would be completely red.

## Setup

### Inside Anki
To use, the
name of the answer field (the `{{type:NN}}` bit) must contain the word
“Scalar”. (E.g. “Area_Scalar” or “Inhabitants_Scalar” for a geography
deck or “Atomic_Mass_Scalar” for a chemistry deck.)

For fields without
“Scalar” in the name the behaviour stays the same, doing the
character-by-character comparison.

### Configuration

 To change the factor what counts as “close enough” change the
`pass_factor` in the .py source file. There are also a few other
things that can somewhat easily be changed. The comments in thy source
file should be a help.

## “Correct answer was:”

<figure style="width:410px;"><img
src="images/compare_by_char.png" alt="Very close answer and
lots of red.">
<figcaption>Even though the reading was typed correctly there is a lot
of red and extra text.</figcaption></figure>

When this add-on is working, the “Correct answer
was:” text is not shown at all. This is partly due to the way the
add-on operates, but i see this as a bonus, not a problem. At this
time, people who really want this text could possibly add it to their
own copy of the add-on. (In other words,
[UTSL](http://www.jargon.net/jargonfile/u/UTSL.html).)
