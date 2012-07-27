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
import shutil

import romaji
import kana_kanji
from exists import exists_lc
from progress import progress

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, showText, askUser
from anki.utils import ids2str, stripHTML

name_source_fields = ['SequenceMarker','Reading', 'Expression', 'Kanji' ]

## Try to separate kanji and kana from the string to use. Convert
## something like 「お 父[とう]さん」 into “お父さん_おとうさん”. This
## should be harmless for most non-Japanese data. If your data uses
## square brackets for other purposes, consider setting this to False.
split_reading = True
# split_reading = False

## When split_reading is True, use a reading, even when the katakana
## version of the reading is identical to the expression.
reading_for_katakana = False
# reading_for_katakana = True

hash_name_pat = '(?:\[sound:|src *= *")([a-z0-9]{32})'\
    '(\.[a-zA-Z0-9]{1,5})(?:]|")'


def katakanaize(hiragana):
    """
    Return katakana
    
    Transform a hiragana string to katakana through the circuitous
    route of converting it to rōmaji, then to uppercase, than to
    kana again.
    
    """
    return romaji.kana(romaji.roma(hiragana).upper())


def mangle_reading(nbn):
    """Try to separate Japanese kanji and reading out of a string """
    # Variable names and comments here assume the text is
    # Japanese. When it is not, nothing bad should happen.
    kana = kana_kanji.kana(nbn)
    kanji = kana_kanji.kanji(nbn)
    if kana and not kanji:
        # Quick save
        kanji = kana
    # Now the tricky bit: decide when to use the split values.
    if kana and kanji and kanji != kana:
        if reading_for_katakana or \
                katakanaize(kanji) != katakanaize(kana):
            return kanji + u'_' + kana
        else:
            return kanji
    # Still here: i guess don’t use the split after all.
    return nbn



def new_name_base(old_base, note):
    """
    Get the base of a new file name
    
    Look at the information on the card and use the data to create
    a base new name.
    """
    def find_field(note, old_base):
        """
        Compare the  candidate fields and the notes fields.
            
        Look through the two lists, name_source_fields and the
        note’s items, to find the field we should use. Put in
        function so we can break out of nested loops.
        
        """
        for sf in name_source_fields:
            for name, value in note.items():
                if name == sf:
                    value = stripHTML(value)
                    # Check here if we have something left. So we
                    # can keep on looking when we have a candidate
                    # field but it’s empty.
                    if value and not old_base in value:
                        # Avoid the field we got the name from
                        # (i.e. the audio, image field).
                        return name, value
        # We got here: no match.
        return None, None

    # Several tries. First, look through the list.
    name, value = find_field(note, old_base)
    if value and not old_base in value:
        return value
    # Still here, next try the sort field.
    name, value = note.items()[mw.col.models.sortIdx(note.model())]
    value = stripHTML(value)
    if value and not old_base in value:
        return value
    for name, value in note.items():
        # Last resort: go through the fields and grab the first
        # non-empty one, except the one with the file.
        value = stripHTML(value)
        if value and not old_base in value:
            return value
    # Well, shoot. Looks like the only field with anything interesting
    # is the one with the file. (Almost reasonable. One-side cards to
    # just listen to something and decide without further info if you
    # recoginze that.)
    raise ValueError(u'No data for new name found')



def free_media_name(base, end):
    """
    Return a useful media name.

    Return a name that can be used for the media file. That is one
    that based on the base name and end, but doesn't exist, nor does
    the it clash with another file different only in upper/lower case.
    """
    mdir = mw.col.media.dir()
    if not exists_lc(mdir, base + end):
        return base+end
    for i in range(1, 10000):
        # Don't be silly. Give up after 9999 tries.
        long_name = '{0} ({1}){2}'.format(base, i, end)
        if not exists_lc(mdir, long_name):
            return long_name
    raise ValueError
    
        
def new_media_name(old_base, old_end, note):
    """
    Get new file name for a hashed file name.
    
    Make sure the desired name doesn’t clash with other names.
    Return a file name that doesn’t clash with existing files,
    doing parts by hand to avoid issues with case-sensitive and
    non-case-sensitive file systems.
        
    This means we also have to add a version of the name to a
    list, so the next card won't use this name.
    """
    nbn = new_name_base(old_base, note)
    if split_reading:
        nbn = mangle_reading(nbn)
    # remove any dangerous characters
    # First replace [,] with (, )
    nbn = nbn.replace('[', '(')
    nbn = nbn.replace(']', ')')
    # Then delete a string of other characters
    nbn = re.sub(r"[][<>:/\\&?\"\|]", "", nbn)
    if not nbn:
        raise ValueError
    return free_media_name(nbn, old_end)



def test_and_dehashilate():
    if not test_names():
        showInfo('No hashes found in cards. Have a nice day.')
        return
    if not askUser('Go ahead?\nThis cannot be undone!\nUse at your own risk!\n'\
                       'Backup your collection before continuing!'):
        return
    if not askUser('Click on "No".\n'\
                       'Clicking on "Yes" will probably mess up your collection.\n'\
                       'You will have to fix it yourself!',
                   defaultno=True):
        return
    dehashilate()

def test_names():
    """Go through the collection and show possible new names
    
    Search the cards for sounds or images with file names that look
    like MD5 hashes, rename the files and change the notes.
    
    """
    test_string = u''
    nids = mw.col.db.list("select id from notes")
    for nid in progress(nids, "Dehashilating", "This is all wrong!"):
        n = mw.col.getNote(nid)
        for (name, value) in n.items():
            rs =  re.search(hash_name_pat, value)
            if None == rs:
                continue
            try:
                new_name_ = new_media_name(rs.group(1), rs.group(2), n)
            except ValueError:
                continue
            test_string += u'{0}{1} → {2}\n'.format(
                rs.group(1), rs.group(2),
                new_name_)
    if (test_string):
        showText('These new names will be used:\n' + test_string)
    return test_string


def dehashilate():
    """Go through the collection and clean up MD5-ish names

    Search the cards for sounds or images with file names that
    look like MD5 hashes, rename the files and change the notes.
    
    """
    mdir = mw.col.media.dir()
    new_names_dict = {}
    rename_exec_list = []
    bad_mv_text = u''
    mw.checkpoint(_("Dehashilate"))
    nids = mw.col.db.list("select id from notes")
    for nid in progress(nids, "Dehashilating", "This is all wrong!"):
        n = mw.col.getNote(nid)
        for (name, value) in n.items():
            for match in re.findall(hash_name_pat, value):
                rs =  re.search(hash_name_pat, value)
                if None == rs:
                    # Should be redundant with the for match ...:
                    # loop. RAS 2012-06-23
                    continue
                old_name = '{0}{1}'.format(rs.group(1), rs.group(2))
                try:
                    new_name  = new_names_dict[old_name]
                except KeyError:
                    try:
                        new_name = new_media_name(rs.group(1), rs.group(2), n)
                    except ValueError:
                        continue
                    do_rename = True
                else:
                    do_rename = False
                if do_rename:
                    src = os.path.join(mdir, old_name)
                    dst = os.path.join(mdir, new_name)
                    try:
                        os.rename(src, dst)
                    except OSError:
                        print 'src: ', src
                        print 'dst: ', dst
                    else:
                        new_names_dict[old_name] = new_name
                    n[name] = value.replace(old_name, new_name)
                    n.flush()
                    rename_exec_list.append(dict(nid=nid,flds=n.joinedFields()))
    mw.col.db.executemany("update notes set flds =:flds where id =:nid",
                          rename_exec_list)
    # This is a bit of voodo code. Without it the cards weren't
    # synced. Maybe this helps. (Cribbed from anki.find, but don't
    # keep extra list of nids.) RAS 2012-06-20
    # And it doesn't work. RAS 2012-07-13

    # """File
    # "/home/roland/Anki-tests/addons/dehashilator/dehashilator.py",
    # line 268, in dehashilate 
    # mw.col.updateFieldCache([re_dict[nids] for re_dict in
    # rename_exec_list])
    # TypeError: unhashable type: 'list'"""
     # mw.col.updateFieldCache([re_dict[nids] for re_dict in rename_exec_list])
    mw.reset()
    if bad_mv_text:
        showText('These files weren’t renamed:\n' + test_string)
    

    
