title: Scalar
main_file: scalar.py
layout: addon
date: 2013-05-07
status: working
status_color: green
status_text_color: white
abstract: "Compare a typed in number with the correct answer as a
number, not as a string of digits. Color it yellow when it is close to
the right number."
first_image: scalar.png
first_caption: 70 is close to 65.
first_alt: "Two lines of Text: 1: Frankreich hat 65 Millionen
Einwohner. 2: 70 → 65. The 70 is blue, the 65 green."
ankiweb_id: 333346658

When learning some types of numbers, like the number of inhabitants of
a country, getting it almost right is good enough. This add-on colors
the answer in yellow when it was close to the original answer.

The answer is also re-arranged into a single line, and typically shown
with the standard font, not a monospace one.


## Example

<figure>
<img src="images/compare_by_char.png" alt="Similar to the image
above. The 70 and 65 are in two lines. The 70 is gray on red, the 65
gray on gray.">
<figcaption>
Without this add-on: even though the typed in answer is close to the
correct one, it is marked in red.
</figcaption>
</figure>
In the image, the correct answer is <q>65</q>, when you know it is close to
70, you type that. The original behavior is to compare character by
character, and mark the typed answer red: a 7 is no 6 and a 0 is no
5. With this add-on, the whole answer would be yellow, as it is close
to the correct answer.

On the other hand, if you had typed <q>650</q> as the answer, with the
original behavior, you would get the <q>65</q> marked green and <q>0</q> marked
red, showing more green, even though the answer is farther from the
correct one.  With this add-on the 650 would be completely red.

## Setup

### Fields

To use, the name of the answer field (the `{{type:NN}}` bit) must
contain the word <q>scalar</q>. For example use <q>Area scalar</q> or
<q>Inhabitants scalar</q> for a geography deck or <q>Atomic mass
scalar</q> for a chemistry deck.

For fields without
<q>scalar</q> in the name the behavior stays the same, doing the
character-by-character comparison.

### CSS

Like Anki itself, this add-on is doing the coloring with CSS
classes. It reuses two of the standard classes, `typeGood` and
`typeBad`, and uses the class `typePass` for the yellow close-enough
bits. To modify the display, styling for these classes should be added
to the card styling. The `div` containing the numbers also has the
class `typedscalar`, so that these numbers can be styled differently
from typed-in text.

Take a look at the [source code]
(https://github.com/ospalh/anki-addons/blob/master/scalar.py) for more
details.

The example images where taken with a somewhat complex note
type, using this type of CSS setup. In this case:
<blockquote class="lsting"><pre><code><span>.card {color: #657b83; background-color: #fdf6e3;}
\#typeans span {background-color: #fdf6e3;}
.typeBad {color: #dc322f;}
.typeMissed, .typePass {  color: #268bd2;}
.typeGood{color: #859900;} </code></pre></blockquote>

This also changes the <q>pass</q>/<q>close enough</q> color from the yellow
mentioned in the text to blue.

The basic color scheme is called
[Solarized](http://ethanschoonover.com/solarized).



### Close enough factor

To change what counts as <q>close enough</q> change the `pass_factor` in
the .py source file.

## Anki version

Please make sure that you are running a version of Anki ≥ 2.0.9, as
the comparison mechanism was changed for that release.
