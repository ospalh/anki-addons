title: Kanji stroke color
id: kanjistrokecolor
main_file: Kanji stroke colour.py
type: addon
status: hackish, desktop only
status_color: yellow
status_text_color: black
abstract: A quick hack add-on to show (colored) stroke order diagrams.
first_image: stroke color.png
first_alt: Colored stroke order diagram for 休

This is a quick hack to show colored stroke order diagrams. You need
to put stroke order diagram svgs in
`Anki/addons/kanji-colorize-indexed`. Then they are shown when you use
the template `{{kanjiColor:NN}}`.

### Alternative

This add-on serves a similar purpose as
[cayennes](http://cayennes.github.com)’s 
 [add-on](https://github.com/cayennes/kanji-colorize/tree/master/anki)
 part of the kanji-colorize project.

#### Pros
* Does not need another field in the model
* Keeps the collection.media folder clean.
* Somewhat simple to exchange the whole set with another color
  scheme. Just bend one link to another directory.
* With the alt text and the kanjistrokeorder font, it's not that bad
  on AnkiWeb/AnkiDroid

#### Cons

* The core function, color, is not working on AnkiWeb/AnkiDroid
* The set-up of Cayennes's add-on may be easier on the add-on side.

### Diagrams

The diagrams can be produced with either Cayenne's
[kanji-colorize](https://github.com/cayennes/kanji-colorize/) script
or with [my fork](https://github.com/ospalh/kanji-colorize) of it.

Both use the [KanjiVG](http://kanjivg.tagaini.net/) data set as the base.
