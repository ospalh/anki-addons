title: Nachschlagen
id: lookup
main_file: nachschlagen.py
layout: addon
date: 2013-05-07
status: working
status_color: green
status_text_color: white
abstract: "Menu to look up words at a few web sites. Most useful for
speakers of German learning Japanese."
first_image: nachschlagen.png
first_alt: "A menu called Nachschlagen under the Tools menu. Menu
items: Japanisch bei Wadoku, Deutsch bei Wadoku, Auswahl bei Wadoku,
Kanji bei Kanji-Lexikon, Kanjiauswahl bei Kanji-Lexikon, Ausdruck bei
Forvo, Auswahl bei Forvo"
first_caption: The new menu
ankiweb_id: 1211332804

Like the <q>Lookup</q> menu from the Japanese support add-on, this
adds a menu called <q lang="de">Nachschlagen</q> were you can look up
words at some of my favorite resources.

A few of them are German, and the whole add-on is kept in German as
well. <q lang="de">Nachschlagen</q> is German for <q>look up</q>.

## Set-up

There is a configuration section at the head of the
[source file](https://github.com/ospalh/anki-addons/blob/master/nachschlagen.py)
where a few things can be configured. Most of it is not too important
and explained in the file itself. You may encounter the error message
<q>No field found for look-up. Consider changing the field name lists
in the plugin source.</q> That means that my guesses about what you
use as field names were wrong. In this case you should add your
favorite field names to the `expression_fields` and `meaning_fields`
lists.


## For learners of any spoken language

The <q>Forvo</q> links are useful for learners of any spoken language. Look
up pronunciations at the crowd-sourced [forvo.com](http://forvo.com).

## For learners of Japanese

The kanji look-up at
[saiga-jp.com](http://www.saiga-jp.com/kanji_dictionary.html) may be
useful for learners of Japanese

## For German speakers

The two other resources are more narrowly useful for German speakers:

* [Kanjilexikon](http://lingweb.eva.mpg.de/kanji/index.html), pretty
  much what it says. A German kanji dictionary.
* [WaDoku](http://www.wadoku.de/wadoku), basically *the* Japanese–German
  online dictionary
