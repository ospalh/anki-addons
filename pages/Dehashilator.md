title: Dehashilator
id: dehashilator
main_file: Dehashilate.py
status: breaks collections
type: addon
status_color: red
status_text_color: white
abstract: Rename media files with names that look like MD5 hashes.
first_image: hashes.png
first_alt: Old and new file names.
download_file: dehashilator.zip

Rename media files with names that look like MD5 hashes.
<blockquote class=nb>This add-on is likely to break your
collection. You *will* have to fix a few file names by hand.</blockquote>

Up to version 1.1, Anki changed the names of media files added to
their [MD5](http://en.wikipedia.org/wiki/MD5)
[hashes](http://en.wikipedia.org/wiki/Cryptographic hash function).
That meant that you had directories full of file names like
`66a6565b69edcb65e7a083a4df1f0900.png` or
`2304355e4eb95f078b2565352f2b5413.mp3`, that bore no relation to the
facts (now notes) they were used on.
For decks that were created on these versions, those file names are
still present in Anki 2 collections.

While this is no real problem, it prevents you to identify a specific
file without starting Anki, for example to edit a picture. It also
bugged me personally.

## Installation

To install, copy not only the
[`dehashilate.py`](https://github.com/ospalh/anki-addons/blob/master/dehashilate.py)
source file, but also the
[`dehashilator`](https://github.com/ospalh/anki-addons/blob/master/dehashilator)
directory to the `Anki/addons` folder.

## Usage

Activate the `Tools/Dehashilate media` menu item.

The dehashilation happens in two steps. First, the collection is
scanned for hash-like file names, new names are calculated and
shown. If you don’t like the suggested names, the only solution is to
change the
[source](https://github.com/ospalh/anki-addons/blob/master/dehashilator/dehashilator.py),
especially the `name_source_fields` list.

When you like the names and click “Yes” twice, the file will be
renamed and field content changed. You should run the
`Maintenance/Unused Media ...` menu item to find problems created by
the dehashilation. You may also run the dehashilator again.  At one
time it had problems with several hash-like media in a single field.

## Notes

This was written as a one-of fix-my-collection-once add-on. As such,
with my personal collection fixed, i am not really interrested in
making this perfect. It will probably stay in its current, somewhat
buggy, state. Others are welcome to do their own work or to send pull
requests, but simple “it broke my collection” issue reports will be
ignored.

The name was inspired by the
[dihoxulator](http://www.girlgeniusonline.com/comic.php?date=20021213). So
was the [stop button
text](http://www.girlgeniusonline.com/comic.php?date=20021218).
