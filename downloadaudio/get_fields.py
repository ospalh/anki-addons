# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Extract field data to download.
"""

from collections import namedtuple
import re

from aqt import mw

from .field_data import FieldData, JapaneseFieldData


# # Change these to mach the field names of your decks. Make sure to
# # not use capital letters. We compare these to lower-case only
# # versions of the field names. When these lists contain upper-case
# # letters, no field will ever be matched and nothing will be
# # downloaded.
expression_fields = [u'expression', u'word']
# Fields we get the ‘normal’ download text from.
#
# Text from these fields is used by most downloaders. When no field is
# found here, we use the first field.


reading_keys = [u'reading', u'kana', u'かな', u'仮名']
# Fields we get our Japanese text from.
#
# For Japanesepod we use these fields as source. A ‘Reading’ field is
# typically filled automatically by the Japanese Support add-on in a
# useful way (that is, with the reading in square brackets).


audio_field_keys = [u'audio', u'sound']
# Fields we put our downloaded sounds in. Don’t try crazy stuff here.

split_kanji_kana = False
# Replace ‘False’ with ‘True’ when you have no kanji in your reading field

# Change this at your own risk.
field_name_re = r'{{(?:[/^#]|[^:}]+:|)([^:}{]*%s[^:}{]*)}}'


def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes


def field_data(note, audio_field, reading=False):
    u"""Return FieldData when we have a source field

    Return FieldData when we have a matching source field for our
    audio field.  """
    def return_data(idx):
        source_name = field_names[idx]
        if reading:
            return JapaneseFieldData(
                source_name, audio_field, note[source_name])
        else:
            return FieldData(
                source_name, audio_field, note[source_name])

    a_name = audio_field.lower()
    field_names = [item[0] for item in note.items()]
    f_names = [fn.lower() for fn in field_names]
    # First, look for just audio fields
    for afk in audio_field_keys:
        if a_name == afk:
            if reading:
                sources_list = reading_keys
            else:
                sources_list = expression_fields
            for cnd in sources_list:
                for idx, lname in enumerate(f_names):
                    if cnd == lname:
                        return return_data(idx)
            # At this point: The target name is good, but we found no
            # source name.
            if not reading:
                # Don't give for most languages. Simply use the first
                # field. That should work for a lot of people
                return return_data(0)
            else:
                # But that doesn't really work for Japanese.
                raise KeyError('No source name found (case 1)')
        # This point: target name is not exactly the field name
        if afk not in a_name:
            # And not a substring either
            continue
        # Here: the field name contains an audio or sound.
        # Mangle the name as described. For the reading case we get a
        # list. So do a list for the other case as well.
        if reading:
            sources_list = [a_name.replace(afk, rk) for rk in reading_keys]
        else:
            # Here the tricky bit is to remove the right number of '_'
            # or ' ' characters, 0 or 1, but not 2. What we want is:
            # ExampleAudio -> Example
            # Example_Audio -> Example
            # Audio_Example -> Example
            # but
            # Another_Audio_Example -> Another_Example, not Another_Example
            # While a bit tricky, this is not THAT hard to do. (Not
            # lookbehind needed.)
            sources_list = [
                re.sub(r'[\s_]{0}|{0}[\s_]?'.format(re.escape(afk)),
                       '', a_name, count=1, flags=re.UNICODE)]
        for cnd in sources_list:
            for idx, lname in enumerate(f_names):
                if cnd == lname:
                    return return_data(idx)
        # We do have audio or sound as sub-string but did not find a
        # maching field.
        raise KeyError('No source field found. (case 2)')
    # No audio field at all.
    raise KeyError('No source field found. (case 3)')


def field_data_from_kanji_kana(note, fn):
    # Do the search twice
    base_fd = field_data(note, fn)
    # base_fd contains the kanji
    read_fd = field_data(note, fn, True)
    # read_fd is the right type but needs to be updated.
    read_fd.kanji = base_fd.word
    read_fd.word = base_fd.word  # Not used, Set anyway.
    read_fd.word_field_name = base_fd.word_field_name
    return read_fd


def get_side_fields(card, note):
    u"""Return a list of FieldDatas for the currently visible side

    Go through the fields of the currently visible side and return
    relevant data, as FieldData objects, for audio fields where we
    have matching text fields."""
    if 'question' == mw.reviewer.state:
        template = card.template()[u'qfmt']
    else:
        template = card.template()[u'afmt']
    audio_field_names = []
    all_field_names = [item[0] for item in note.items()]
    for afk in audio_field_keys:
        # Append all fields in the current template/side that contain
        # 'audio' or 'sound'
        audio_field_names += re.findall(
            field_name_re % afk, template, flags=re.IGNORECASE)
        # We use the (old style) % operator rather than
        # unicode.format() because we look for {}s in the re, which
        # would get more complicated with format().
    audio_field_names = uniqify_list(audio_field_names)
    # Filter out non-existing fields.
    audio_field_names = [
        fn for fn in audio_field_names if fn in all_field_names]
    field_data_list = []
    for audio_field in audio_field_names:
        try:
            field_data_list.append(field_data(note, audio_field))
        except (KeyError, ValueError):
            # No or empty reading field
            pass
        if not split_kanji_kana:
            try:
                field_data_list.append(
                    field_data(note, audio_field, reading=True))
            except (KeyError, ValueError):
                pass
        else:
            try:
                field_data_list.append(
                    field_data_from_kanji_kana(note, audio_field))
            except (KeyError, ValueError):
                pass
    return field_data_list


def get_note_fields(note):
    u"""Return a list of FieldDatas for the note

    Go through the note’s fields and return relevant data, as
    FieldData objects, for audio fields where we have matching text
    fields."""
    field_names = [item[0] for item in note.items()]
    field_data_list = []
    for afk in audio_field_keys:
        for fn in field_names:
            if afk not in fn.lower():
                continue
            if not split_kanji_kana:
                try:
                    field_data_list.append(field_data(note, fn, reading=True))
                except (KeyError, ValueError):
                    # No or empty source field.
                    pass
            else:
                try:
                    field_data_list.append(
                        field_data_from_kanji_kana(note, fn))
                except (KeyError, ValueError):
                    # No or empty source field.
                    pass
            try:
                field_data_list.append(field_data(note, fn))
            except (KeyError, ValueError):
                # No or empty source field.
                pass
    return field_data_list
