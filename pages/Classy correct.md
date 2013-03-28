title: Classy correct
id: classy_correct
main_file: classy_correct.py
date: 2013-03-25
tags: [class, css, future]
type: addon
status: future
status_color: red
status_text_color: white
abstract: Add a css classes to the corrected answer.
first_image: classy.png
first_alt: "Sceenshot with three lines of text. 1, 2: „Die Hauptstadt
von Mosambik ist Maputo.“, 3.:  „Mabuto“, the „b“ is red, the rest
green"
first_caption: "The red and green marking is more reserved and matches
the color scheme."

This add-on removes the explicit styling from the corrected answer and
replaces it with the classes `typedgood` or `typedbad`. It is up to
the user, but possible now, to set up the style for this in the card
template.


<blockquote class="nb">
This add-on relies on a change i suggested for Anki, but that has not
been implemented. You have to use my ospalh-special branch for this
add-on to do anything.
</blockquote>

The important bits of the card template used were
<blockquote><pre><code>.typedbad {color: #dc322f;}
.typedgood {color: #859900;}</code></pre></blockquote>

Other bits were
<blockquote><pre><code>.card{
  font-family: 'Demos LT';
  font-size: 24px;
  text-align: center;
  color: #657b83;
  background-color: #fdf6e3;
}
\#corrected span:hover  { text-shadow: 1px 2px 5px #657b83; }</code></pre></blockquote>


<figure>
<img src="images/stylish.png"
alt="Sceenshot with the same text as above. In line three, the „b“ is
in black with red background, the rest
black with green background." />
<figcaption>
    The old style.
</figcaption>
</figure>
The basic color scheme in the example images is called
[Solarized](http://ethanschoonover.com/solarized).

The original style is to show the the text in black with red or green
background, which may not look too good with color schemes that don’t
use black text.
