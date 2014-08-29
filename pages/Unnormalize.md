title: Unnormalize
id: unnormalize
main_file: unnormalize.py
date: 2013-06-07
type: addon
status: may add errors, broken
status_color: red
status_text_color: white
abstract: "Fix file name problems caused by Unicode normalization."
first_image: tuebingen_tuebingen.png
first_alt: 'Screen text: In media folder but not used by any cards:
Tübingen_Neckarfront.jpg Used on cards but missing from media folder:
Tübingen_Neckarfront.jpg.'
first_caption: "So, the file is there and it is missing‽"

This can be used to fix a problem caused by adding files “sideways” on
Macs.

<blockquote class="nb">
This add-on does not work with newer versions of Anki. On the other
hand it should not be needed any more.
</blockquote>

## The problem

When files are added not with the file add dialog through the paper
clip icon, but through other ways,

* by copying them to the media folder by hand and adding the text to
  display them to the fields,
* through other tools like older versions (up to version 2.3.4, 24
  January 2013) of my [Download audio](Download%20audio.html) add-on,
* or possibly by drag-and-dropping them from the Finder,

there may be a problem caused by a quirk of the Macs’ file system. In
file names on Macs, many
non-[ASCII](http://en.wikipedia.org/wiki/ASCII) characters are
[decomposed](http://en.wikipedia.org/wiki/Precomposed_character#Comparing_precomposed_and_decomposed_characters).
For example, the character
“[ü](http://www.fileformat.info/info/unicode/char/00fc/index.htm)” is
stored as
“[u](http://www.fileformat.info/info/unicode/char/0075/index.htm)”
plus the
[dots](http://www.fileformat.info/info/unicode/char/0308/index.htm) as
an extra character.

Most of the time this is completely harmless. But when the text in the
field contains an un-decomposed character, for example “`<img
src="Tübingen_Neckarfront.jpg" />`” and that text together with the
file with the decomposed name, “`Tübingen_Neckarfront.jpg`”, are
synced to a Linux or Windows machine, those two strings do not point
to the same file. The result is that the file isn’t show during
review. At the moment (January 2013, Anki 2.0.6), the
“Tools/Maintenance/Unused media...”  file will not detect this
problem, it only becomes apparent during reviews or when browsing the
cards.


## The solution

The add-on goes through the collection and renames media file to those
used in the collection when the on-disk name is the Mac OS X version
of that in the collection.

<blockquote class="nb">This add-on in a hack. It worked well for me,
but might introduce errors in the collection. Caveat
emptor.</blockquote>

This can work only when run on non-Macs. When there is no non-Mac
desktop client available, the only solution to this problem that i see
is to go through the collection and fix the file names by hand. Or
possibly re-download audio clips with a new version of Download audio,
if that is what caused the problems.

## See also

This issue has been discussed as
[one](https://anki.lighthouseapp.com/projects/100923/tickets/500-anki-confused-about-some-file-names#ticket-500)
or possibly
[two](https://anki.lighthouseapp.com/projects/100923/tickets/559-problems-with-files-containing-umlauts-related-to-500)
issues at the Anki issue tracker.
