# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

from anki.hooks import addHook
import re, sys

tooOld = sys.version_info < (2, 7)

if tooOld:
    r = r' ?([^ ]+?)\[(.+?)\]'
else:
    r = r' ?([\w]+?)\[(.+?)\]'
    

furiKanjiPat = r'<ruby><rb>\2</rb><rt>\1</rt></ruby>'
if tooOld:
    rm = r' ?([^ ]+?)\[(.+?)\]'
else:
    rm = r' ?([\w]+?)\[(.+?)\]'

def noSound(repl):
    def func(match):
        if match.group(2).startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            if tooOld:
                return re.sub(rm, repl, match.group(0))
            return re.sub(rm, repl, match.group(0), flags=re.U)
    return func

def furikanji(txt, *args):
    if tooOld:
        return re.sub(rm, noSound(furiKanjiPat), txt)
    return re.sub(rm, noSound(furiKanjiPat), txt, flags=re.U)

addHook('fmod_furikanji', furikanji)
