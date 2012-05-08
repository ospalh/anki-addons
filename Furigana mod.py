# -*- coding: utf-8 -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

import re, sys
from anki.hooks import addHook

tooOld = sys.version_info < (2, 7)

if tooOld:
    splitPat = r' ?(?P<kanji>[^ \n]+?)\[(?P<kana>.+?)\]'
else:
    splitPat = r' ?(?P<kanji>[\w]+?)\[(?P<kana>.+?)\]'
    
furiganaPat = r'<ruby class="furigana"><rb>\g<kanji></rb><rt>\g<kana></rt></ruby>'
furikanjiPat = r'<ruby class="furikanji"><rb>\g<kana></rb><rt>\g<kanji></rt></ruby>'

def noSound(repl):
    def func(match):
        if match.group('kana').startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            if tooOld:
                return re.sub(splitPat, repl, match.group(0))
            return re.sub(splitPat, repl, match.group(0), flags=re.UNICODE)
    return func

def kanji(txt, *args):
    if tooOld:
        return re.sub(splitPat, noSound(r'<span class="kanji">\g<kanji></span>'), txt)
    return re.sub(splitPat, noSound(r'<span class="kanji">\g<kanji></span>'), txt, flags=re.UNICODE)

def kana(txt, *args):
    if tooOld:
        return re.sub(r, noSound(r'<span class="kana">\g<kana></span>'), txt)
    return re.sub(splitPat, noSound(r'<span class="kana">\g<kana></span>'), txt, flags=re.UNICODE)

def furigana(txt, *args):
    if tooOld:
        return re.sub(r, noSound(furiganaPat), txt)
    return re.sub(splitPat, noSound(furiganaPat), txt, flags=re.UNICODE)


def furikanji(txt, *args):
    if tooOld:
        return re.sub(splitPat, noSound(furikanjiPat), txt)
    return re.sub(splitPat, noSound(furikanjiPat), txt, flags=re.U)


def noInstall():
    pass

addHook('fmod_furikanji', furikanji)
addHook('fmod_kanjiw', kanji)
addHook('fmod_kanaw', kana)
addHook('fmod_furiganaw', furigana)

