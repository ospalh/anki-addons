# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

from anki.hooks import addHook
import locale

# I personally like the Swiss use of the apostroph as thousands separator.
# locale.setlocale(locale.LC_NUMERIC, 'de_CH.UTF-8')

millions_word = (u' <span class="number_romaji">Millionen</span>')
billions_word = (u' <span class="number_romaji">Milliarden</span>')


def ch_millionen(txt, *args):
    s_int = 0
    digit_shift = 0
    # check if we have whole millions
    try:
        s_int = int(txt)
        if float(txt) ==  0.0:
            # special special case. Normal exceptions: stuff like 0.5...
            # but make sure we go to the exception for true 0.
            raise ValueError
    except ValueError:
        # check if we have a whole number
        try:
            s_int = int (1000000 * float(txt))
        except ValueError:
            # Can’t get to an integer at all. forget special formarting.
            return txt
        digit_shift = 6
        if s_int < 10000:
            # Don’t group below 10000
            return str(s_int)
    if digit_shift == 0 and s_int >= 1000:
        digit_shift = -2
        s_float = s_int / 1000.0
        if s_int % 1000 == 0:
            s_int =  s_int / 1000
            digit_shift = -3
    s_num_str = u''
    locale.setlocale(locale.LC_NUMERIC, 'de_CH.UTF-8')
    if digit_shift == -2:
        s_num_str = locale.format('%.1f', s_float, grouping=True)
    else:
        s_num_str = locale.format('%d', s_int, grouping=True)
    s_num_str = '<span class="number_arab">{0}</span>'.format(s_num_str)
    if digit_shift == 0:
        s_num_str += millions_word
    if digit_shift <= -2:
        s_num_str += billions_word
    return s_num_str

def ch_t_sqkm(txt, *args):
    digit_shift = 3
    s_float = 0.0
    try:
        s_float = 1000 * float(txt)
    except ValueError:
        # Not a number.
        return txt
    s_int = int (s_float)
    if  s_int < 10000:
        # Don’t group. That’s some rule to write numbers like 7500 w/o
        # grouping.
        if s_int == s_float:
            return str(s_int) + u' <span class="number_romaji">km²</span>'
        return str(s_float) + u' <span class="number_romaji">km²</span>'
    if s_int >= 1000000:
        digit_shift = -5
        s_float = s_int / 1000000.0
        if s_int % 1000000 == 0:
            s_int =  s_int / 1000000
            digit_shift = -6
    s_num_str = u''
    locale.setlocale(locale.LC_NUMERIC, 'de_CH.UTF-8')
    if digit_shift == -5:
        s_num_str = locale.format('%.1f', s_float, grouping=True)
    else:
        s_num_str = locale.format('%d', s_int, grouping=True)
    s_num_str = '<span class="number_arab">{0}</span>'.format(s_num_str)
    if digit_shift <= -5:
        # Squaremegametres. What else?!
        s_num_str += u' <span class="number_romaji">Mm²</span>'
    else:
        s_num_str += u' <span class="number_romaji">km²''</span>'
    return s_num_str



def jp_man(txt, *args):
    # We cheat a bit. We know that we won’t have 一億km².
    i_float = 0.0
    try:
        i_float = float(txt)
    except ValueError:
        # Not a number.
        return txt
    i_int = int(i_float)
    m_float = i_float / 10.0
    m_int = int(m_float)
    if i_float < 10.0 or m_int != m_float:
        i_float *= 1000
        i_int = int(i_float)
        if i_int == i_float:
            i_str = locale.format('%d', i_int, grouping=True)
            return '<span class="number_arab">{0}</span>'.format(i_str)
        f_str = locale.format('%f', i_float, grouping=True)
        return '<span class="number_arab">{0}</span>'.format(f_str)
    return str(m_float) + u'<span class="number_kanji">万</span>'


# 
def ch_integer(txt, *args):
    s_int = 0
    try:
        s_int = int(txt)
    except ValueError:
        return txt
    locale.setlocale(locale.LC_NUMERIC, 'de_CH.UTF-8')
    s_int_str = locale.format('%d', s_int, grouping=True)
    s_int_str = '<span class="number_arab">{0}</span>'.format(s_int_str)
    return s_int_str




addHook('fmod_swissmega', ch_millionen)
addHook('fmod_swisssqkm', ch_t_sqkm)
addHook('fmod_swissint', ch_integer)
addHook('fmod_jpman', jp_man)
