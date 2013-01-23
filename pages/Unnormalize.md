title: Unnormalize
id: unnormalize
main_file: Unormalize.py
date: 2013-01-22
type: addon
status: "working"
status_color: green
status_text_color: white
abstract: "Fix file name problems caused by Unicode normalization."
first_image: tuebingen_tuebingen.png
first_alt: 'Screen text: In media folder but not used by any cards:
Tübingen_Neckarfront.jpg Used on cards but missing from media folder: Tübingen_Neckarfront.jpg.'
first_caption: "So, the file is there and it is missing‽"

This can be used to fix a problem caused by adding files “sideways” on
Macs.

## The problem

When files are added not with the file add dialog through the paper
clip icon, but through other ways,

* by copying them to the media folder by hand and adding the text to
  display them to the fields,
* through other tools like my
  [Download audio](Download%20audio.html) add-on,
* or possibly by drag-and-dropping them from the Finder,

there may be a problem caused by a quirk of the Macs’ file system. In
file names on Macs, many
non-[ASCII](http://en.wikipedia.org/wiki/ASCII) characters are
[depomposed](http://en.wikipedia.org/wiki/Precomposed_character#Comparing_precomposed_and_decomposed_characters).
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
file with the decomposed name, “`Tübingen_Neckarfront.jpg`”, are synced
to a Linux or Windows machine, those two strings do not point to the
same file. The result is that the file isn’t show during review. At
the moment (January 2013), the “Tools/Maintenance/Unused media...”
file will not detect this problem, it only becomes apparent during
reviews or when browsing the cards.


## The solution

When you suddenly don’t see or hear certain media on non-Apple
machines and you also work with Apple hardware, this add-on may be the
fix. Another indicator for this problem is that the “problem” file
name include some form of
[diacritic](http://en.wikipedia.org/wiki/Diacritic), such as umlauts,
accented characters or voiced kana.

<blockquote class="nb">After applying the fix, the unused media check
may <em>incorrectly</em> complain that the files whose names have been
fixed are unused, and that the files with the incorrect, decomposed
names are missing. <om>Do not delete the files with the “Delete
unused” button.</em></blockquote>

## See also

This issue has been discussed as
[one](https://anki.lighthouseapp.com/projects/100923/tickets/500-anki-confused-about-some-file-names#ticket-500)
or possibly
[two](https://anki.lighthouseapp.com/projects/100923/tickets/559-problems-with-files-containing-umlauts-related-to-500)
issues at the Anki issue tracker.
