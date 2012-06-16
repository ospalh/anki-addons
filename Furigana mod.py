# -*- coding: utf-8 -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# Origianl code: Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

import re, sys
from anki import hooks

too_old = sys.version_info < (2, 7)

if too_old:
    split_pat = r' ?(?P<kanji>[^ >\n]+?)\[(?P<kana>.+?)\]'
else:
    split_pat = u' ?(?P<kanji>[-+×÷%\.\w]+?)\[(?P<kana>.+?)\]'
    
furigana_pat = r'<ruby class="furigana"><rb>\g<kanji></rb><rt>\g<kana></rt></ruby>'
furikanji_pat = r'<ruby class="furikanji"><rb>\g<kana></rb><rt>\g<kanji></rt></ruby>'

def no_sound(repl):
    def func(match):
        if match.group('kana').startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            if too_old:
                return re.sub(split_pat, repl, match.group(0))
            return re.sub(split_pat, repl, match.group(0), flags=re.UNICODE)
    return func

def kanji_word_re(txt, *args):
    if too_old:
        return re.sub(split_pat, no_sound(r'<span class="kanji">\g<kanji></span>'), txt)
    return re.sub(split_pat, no_sound(r'<span class="kanji">\g<kanji></span>'), txt, flags=re.UNICODE)

def kana_word_re(txt, *args):
    if too_old:
        return re.sub(r, no_sound(r'<span class="kana">\g<kana></span>'), txt)
    return re.sub(split_pat, no_sound(r'<span class="kana">\g<kana></span>'), txt, flags=re.UNICODE)

def furigana_word_re(txt, *args):
    if too_old:
        return re.sub(r, no_sound(furigana_pat), txt)
    return re.sub(split_pat, no_sound(furigana_pat), txt, flags=re.UNICODE)


def furikanji(txt, *args):
    if too_old:
        return re.sub(split_pat, no_sound(furikanji_pat), txt)
    return re.sub(split_pat, no_sound(furikanji_pat), txt, flags=re.U)


def box_kana(txt, *args):
    return u'<ruby class="boxkana"><rb style="border:dashed; border-width: 1px">　</rb><rt>%s</rt></ruby>' % txt

def boxed(txt, *args):
    return u'<span class="boxed" style="border:dashed; border-width: 1px">%s</span>' % txt


hooks.addHook('fmod_furikanji', furikanji)
hooks.addHook('fmod_boxkana', box_kana)
hooks.addHook('fmod_boxed', boxed)
if hooks._hooks['fmod_kanji']:
    hooks._hooks['fmod_kanji'][0] = kanji_word_re
if hooks._hooks['fmod_kana']:
    hooks._hooks['fmod_kana'][0] = kana_word_re
if hooks._hooks['fmod_furigana']:
    hooks._hooks['fmod_furigana'][0] = furigana_word_re

