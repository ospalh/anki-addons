# -*- coding: utf-8 -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re, sys

too_old = sys.version_info < (2, 7)

if too_old:
    split_pat = r' ?(?P<kanji>[^ >\n]+?)\[(?P<kana>.+?)\]'
else:
    split_pat = u' ?(?P<kanji>[-+×÷%\.\w]+?)\[(?P<kana>.+?)\]'
    
def no_sound(repl):
    """Return text outside a [sound: ] field."""
    def func(match):
        if match.group('kana').startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            if too_old:
                return re.sub(split_pat, repl, match.group(0))
            return re.sub(split_pat, repl, match.group(0), flags=re.UNICODE)
    return func

def kanji(txt, *args):
    """Return the kanji of a standard kakasi reading."""
    if too_old:
        return re.sub(split_pat, no_sound(r'\g<kanji>'), txt)
    return re.sub(split_pat, no_sound(r'\g<kanji>'), txt, flags=re.UNICODE)

def kana(txt, *args):
    """Return the kana of a standard kakasi reading."""
    if too_old:
        return re.sub(r, no_sound(r'\g<kana>'), txt)
    return re.sub(split_pat, no_sound(r'\g<kana>'), txt, flags=re.UNICODE)

