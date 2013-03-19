title: Batteries
id: batteries
type: other_page

Usually, [Python](http://python.org), the programming language Anki
and Anki add-ons are written in comes with a number of functions
useful for programmers, the
[Python Standard Library](http://docs.python.org/2/library/). This
approach has been called “batteries included”.

Accordingly, when writing some of my add-ons i used functions from the
standard library without second thought.

As it turend out, a standard binary installation of Anki brings along
only some of the files of the standard library. This means that some
of my add-ons won’t run on typical Anki installs, even when they run
on my system.

## Affected add-ons:

This applies to the following add-on. Non of them have been published
on Anki web or are all that useful for the general public.

* [Metric time](Metric%20time.html)
* [Swiss locale](Swiss%20locale.html)
* [Kanji stroke color](Kanji%20stroke%20color.html)
* [Copy diagrams](Copy%20diagrams.html)

The other add-ons should not need this.

## Solution 1: Put back the batteries

I have identified the files that my add-ons need that are not part of
an Anki installation and gathered them together in the folder
“[`batteries`](https://github.com/ospalh/anki-addons/tree/master/batteries)”. Put
a copy of this folder into your “`Anki/add-ons`” folder to run

## Solution 2: Run from source

Most Linux systems already have Python installed. When running Anki
from source, the library files from the system-wide Python
installation will be used.

But Anki needs some other packages, that should be installed through
the local package manager, most notably PyQt. Setting up Anki to run
from source goes beyond this page. Look at the
[Anki main page](http://ankisrs.net/index.html#devel) to get started.
