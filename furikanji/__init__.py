# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–18 Roland Sieker <ospalh@gmail.com>
# Provenance:
# Via libanki/anki/template/furigana.py by Damien Elmes <anki@ichi2.net>
# Based off Kieran Clancy's initial implementation.
#
# License:
# GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


"""
Addon for Anki 2.1 for Furikanji and other purposes

This provides a way to show kanji above the kana.
The addon uses the Unicode word character class to decide what to
display as base text and what as ruby.

Also add a few other templates.
"""

import re
from anki import hooks


__version__ = "3.0.0"


# Get rid off the Python 2.6 vs. 2.7 check. This is Python 3 and knows
# Unicode.
# Then new split pattern
split_pat = r' ?(?P<kanji>\w+?)\[(?P<kana>.+?)\]'
# The pattern to produce the furigana. What is called ruby in the old
# code, but using named groups and adding a class.
furigana_pat = r'<ruby class="furigana"><rb>\g<kanji></rb>' + \
               r'<rt>\g<kana></rt></ruby>'
# Pattern to produce the furikanji.  This is pretty much the reason
# for this add-on.
furikanji_pat = \
    r'<ruby class="furikanji"><rb>\g<kana></rb><rt>\g<kanji></rt></ruby>'


def no_sound(repl):
    """Do re replacement only when the text is not a media file."""
    def func(match):
        """Do re replacement only when the text is not a media file."""
        if match.group('kana').startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            return re.sub(split_pat, repl, match.group(0), flags=re.UNICODE)

    return func


def kanji_word_re(txt, *dummy_args):
    """Strip kana and wrap base text in class kanji."""
    return re.sub(
        split_pat, no_sound(r'<span class="kanji">\g<kanji></span>'),
        txt, flags=re.UNICODE)


def kana_word_re(txt, *dummy_args):
    """Strip base text and wrap kana in class kana."""
    return re.sub(
        split_pat, no_sound(r'<span class="kana">\g<kana></span>'), txt,
        flags=re.UNICODE)


def furigana_word_re(txt, *dummy_args):
    """
    Format text for ruby display.

    Put text with square brackets in <ruby> tags, using text before
    the brackets as the base, the text in the brackets as <rt>, that
    is, the ruby. Add class furigana to the ruby tag.
    """
    return re.sub(split_pat, no_sound(furigana_pat), txt, flags=re.UNICODE)


def furikanji(txt, *dummy_args):
    """
    Format text for ruby display, kanji above kana.

    Put text with square brackets in <ruby> tags, using text before
    the brackets as <rt>, the ruby, and the text in the brackets as
    the base. Add class furikanji to the ruby tag. This is reversed
    from the standard way and typically shows small kanji above their
    reading.
    """
    return re.sub(split_pat, no_sound(furikanji_pat), txt, flags=re.UNICODE)


hooks.addHook('fmod_furikanji', furikanji)
if hooks._hooks['fmod_kanji']:
    hooks._hooks['fmod_kanji'][0] = kanji_word_re
if hooks._hooks['fmod_kana']:
    hooks._hooks['fmod_kana'][0] = kana_word_re
if hooks._hooks['fmod_furigana']:
    hooks._hooks['fmod_furigana'][0] = furigana_word_re
