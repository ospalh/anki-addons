# -*- mode: python ; coding: utf-8 -*-
# Copyright © 2012 Roland Sieker
# Based on deurl-files.py by  Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#

"""Rename files that have MD5ish names

Rename files with Anki <1.2-ish MD5 names with names derived from the
note content.

"""


import re
import os

from romaji import kana, roma
from progress import progress

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, askUser
from anki.utils import ids2str

name_source_fields = ['Reading', 'Expression', 'Kanji' ]

## Try to separate kanji and kana from the string to use. Convert
## something like 「お 父[とう]さん」 into “お父さん_おとうさん”. This
## should be harmless for most non-Japanese data. If your data uses
## square brackets for other purposes, consider setting this to False.
split_reading = True
# split_reading = False

## When split_reading is True, use a reading, even when the katakana
## version of the reading is identical to the expression.
reading_for_katakana = False
# no_reading_for_katakana = True

## To avoid too long syncs of data when only the names have changed,
## provide a way to rename just the files on another computer with a
## batch or shell script file.
batch_name = 'rename_hash-name_files.bat'
script_name = 'rename_hash-name_files.sh'


class Dehashilator(object):

    """Class to rename files that have MD5ish names

    Rename files with Anki <1.2-ish MD5 names with names derived from the
    note content.
    
    """

    def ___init___(self):
        self._hash_name_pat = '(?:\[sound:|src *= *")([a-z0-9]{32})'\
            '(\.[a-zA-Z0-9]{1,5})(?:]|")'
        self._done_names = {}
        self.shell_script_string = u''
        self.batch_string = u''

    def new_base_name(self, note):
        """Get a new base name from a card.
        
        Looks at the note’s fields and pick a new base name for the file.
        
        """
        name, value = note.items()[0]
        return value

    def unique_file_name(self, base_name, ending):
        """Make sure the desired name doesn’t clash with other names.

        Return a file name that doesn’t clash with existing files,
        doing parts by hand to avoid issues with case-sensitive and
        non-case-sensitive file systems.
        
        """
        lbn = base_name.lower()
        return base_name + ending

    def katakanaize(self, hiragana):
        """Return katakana

        Transform a hiragana string to katakana through the circuitous
        route of converting it to rōmaji, then to uppercase, than to
        kana again.

        """
        return kana(roma(hiragana).upper())

    def dehashilate(self):
        """Go through the collection and clean up MD5-ish names

        Search the cards for sounds or images with file names that
        look like MD5 hashes, rename the files and change the notes.
        
        """
        nids = mw.col.db.list("select id from notes")
        for nid in progress(nids, "Dehashilating", "This is all wrong!"):
            n = mw.col.getNote(nid)
            for (name, value) in n.items():
                rs =  re.search(self._hash_name_pat, value)
                if None == rs:
                    continue
                print name, rs.group(1) + rs.group(2), 
                print ' → ',  _new_base_name(n) + rs.group(2)



