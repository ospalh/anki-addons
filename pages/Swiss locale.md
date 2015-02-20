title: Swiss locale
id: swisslocale
main_file: swiss_locale.py
type: addon
date: 2013-05-07
status: one-off, broken
status_color: red
status_text_color: white
abstract: An add-on to make my German geography deck work.
first_image: nordzypern.png
first_alt: The input of 0.26 is formatted as 260'000.

This add-on provides a few hacks to make my personal German geography
deck work.

<blockquote class="nb">
This add-on needs extra Python packages. See the
<q><a href="Batteries.html">Batteries</a></q> page for details.
</blockquote>

The main problem this tries to fix is the vast span of inhabitants of
the countries and territories of the world (more than seven orders of
magnitude if you include the Pitcairn Islands, five if you count only
independent states and exclude religious headquarters). Basically there is no
nice way to display 67 and 1,347,350,000 and have both numbers look
good without a little bit of hacking. That is even more the case when
you use the input answer feature.

My solution is to store the number of inhabitants as millions. But for
countries with less then one million inhabitants, the display would
look like <q lang="de_CH">0.26 Millionen Einwohner</q> or <q
lang="de_CH">0.00007 Millionen Einwohner</q>. That looks ugly. So, i
use this add-on and in the card template i use
`{{swissmega:MegaInhabitants_Scalar}}`. Like that, the output is <q
lang="de_CH">260'000 Einwohner</q> and <q lang="de_CH">70
Einwohner</q>, while larger countries will still get something like <q
lang="de_CH">83 Millionen Einwohner</q>.

Basically the same is done with the area, which is stored in thousands
of square kilometers. One twist is that i am a big fan of the
[SI](http://en.wikipedia.org/wiki/International_System_of_Units) in
all its glory. I like to use SI prefixes even when they are not
common. So, an area of a million square kilometers, that is just one
megameter times one megameter, 1 Mm<sup>2</sup>.

The <q>Swiss</q> part comes from the fact that i just personally like the
Swiss way of writing large numbers with an apostrophe as thousands
separator and have included this in the add-on. The Swiss formatting
will only work on Linux systems.

While this add-on only works with the desktop client, the deck for
which this is written compensates for that, so that the deck is
usable on AnkiWeb and mobile devices.
