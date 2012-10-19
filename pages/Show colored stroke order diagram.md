title: Show colored stroke order diagrams
id: csod
main_file: Show colored stroke order diagram.py
status: early development
type: addon
status_color: red
status_text_color: white
abstract: Another take on displaying the KanjiVG stroke order diagrams with color. Not much more than an idea how to go about it at the moment.
first_image: palette_gimped.png
first_alt: The idea is to pick the stroke colors from an image file.

This is a work in progress that is intended to replace my
[Kanji stroke color](Kanji stroke colour.html) add-on and possibly
coexist with [cayennes](http://cayennes.github.com)’
[add-on](https://github.com/cayennes/kanji-colorize/tree/master/anki),
this one used on desktop clients, cayennes’ on AnkiWeb and mobile
devices.

### Goals

* Use one xml file as the data base.
* Extract svgs from that xml and colorize on the fly
* Make it possible to use different colors at different times, by
  using an image as template.
* Add other effects, such as shadows, or possibly animation, on the fly. Again, with
  different parameters at different times.
* Use this as a normal template or to replace the svgs/images from
  cayennes’ add-on

## Data set

This uses the [KanjiVG](http://kanjivg.tagaini.net/) kanji stroke
order data set as the base.
