# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

import re, sys
from anki.hooks import addHook

tooOld = sys.version_info < (2, 7)

if tooOld:
    r = r' ?([^ ]+?)\[(.+?)\]'
else:
    r = r' ?([\w]+?)\[(.+?)\]'
    
ruby = r'<ruby><rb>\1</rb><rt>\2</rt></ruby>'

def noSound(repl):
    def func(match):
        if match.group(2).startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            if tooOld:
                return re.sub(r, repl, match.group(0))
            return re.sub(r, repl, match.group(0), flags=re.UNICODE)
    return func

def kanji(txt, *args):
    if tooOld:
        return re.sub(r, noSound(r'\1'), txt)
    return re.sub(r, noSound(r'\1'), txt, flags=re.UNICODE)

def kana(txt, *args):
    if tooOld:
        return re.sub(r, noSound(r'\2'), txt)
    return re.sub(r, noSound(r'\2'), txt, flags=re.UNICODE)

def furigana(txt, *args):
    if tooOld:
        return re.sub(r, noSound(ruby), txt)
    return re.sub(r, noSound(ruby), txt, flags=re.UNICODE)

def install():
    addHook('fmod_kanji', kanji)
    addHook('fmod_kana', kana)
    addHook('fmod_furigana', furigana)
