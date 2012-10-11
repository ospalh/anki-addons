# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

import locale
import decimal
from anki.hooks import addHook
from anki.utils import isMac

"""
Anki-2 add-on to format numbers just the way i like them.
"""

# I personally like the Swiss use of the apostroph as thousands separator.
# locale.setlocale(locale.LC_NUMERIC, 'de_CH.UTF-8')

__version__ = '1.1.2'

millions_word = (u' <span class="number_romaji">Millionen</span>')
billions_word = (u' <span class="number_romaji">Milliarden</span>')
arab_format_string = '<span class="number_arab">{0}</span>'


def swiss_format(num):
    """
    Return the number num as a string with Swiss formating.

    Return the number num as a string with Swiss formating, but don't
    use a thousands separator for numbers < 10'000. Also wrap the
    number in a span with class number_arab.

    There seems to be a problem with locales on Macs, so just wrap in
    the span there.
    """
    do_group = (num >= 10000)
    if not isMac:
        # AFAIK loading locales on Macs didn't throw an exception, but
        # gave ugly layout. So don't try it there.
        try:
            # On the other hand, i have problems loading the swiss
            # locale on some other systems. So only try it.
            locale.setlocale(locale.LC_NUMERIC, ('de_CH', 'UTF-8'))
            num_string = locale.format('%d', num, grouping=do_group)
        except:
            num_string = str(num)
    else:
        num_string = str(num)
    return arab_format_string.format(num_string)


def ch_millionen(txt, *args):
    """
    Return the text reformated for my geography deck.

    * Return txt when it is not a number or when it is 0
    * Return txt multiplied by 1'000'000 when it is <1
    * Return txt with the words Millionen added when it is >=1 and <
      1000
    * Return txt with the words Billionen added when it is >= 1000
    When txt is reformated, it uses the Swiss thousands separator of "'".
    This gives nice formating for inhabitans numbers in my geography deck.
    """
    # Total rework. RAS 2012-09-06
    # Parts taken from my "days" script, see
    # https://github.com/ospalh/age/blob/master/days
    try:
        dec_mega = decimal.Decimal(txt)
    except decimal.InvalidOperation:
        # No number
        return txt
    if 0 == dec_mega:
        # Case "0 Einwohner" == "0 Millionen Einwohner"
        return txt

    dms, dmd, dme = dec_mega.as_tuple()
    # order of magnitude +1
    omagp = len(dmd) + dme
    # billons
    if omagp >= 4:
        return arab_format_string.format(float(dec_mega) / 1000.0)\
            + billions_word
    # Full millions
    if dme >= 0:
        # No need to do the swiss formating here. It is the point of
        # the billions exercise that we have <1000 million here. And we don't
        # really need it until 10 billions.
        return str(int(dec_mega)) + millions_word
    # Less than a million or something like 3.5 million.
    return swiss_format(int(dec_mega * 1000000))


def ch_t_sqkm(txt, *args):
    """
    Return the text reformated for my geography deck.

    * Return txt when it is not a number

    * Return txt multiplied by 1'000 with km<sup>2</sup> added when it is <1000
    * Return txt divided by 1'000 with Mm<sup>2</sup> added when it is >=1000
    When txt is reformated, it uses the Swiss thousands separator of "'".
    The text is also wrapped in some classes.
    This gives nice formating for area numbers in my geography deck.
    """
    # Total rework. RAS 2012-09-06
    # Parts taken from my "days" script, see
    # https://github.com/ospalh/age/blob/master/days
    try:
        dec_kilo = decimal.Decimal(txt)
    except decimal.InvalidOperation:
        # No number
        return txt
    dks, dkd, dke = dec_kilo.as_tuple()
    # order of magnitude +1
    omagp = len(dkd) + dke
    if omagp >= 4:
        return arab_format_string.format(float(dec_kilo) / 1000.0) + \
            u' <span class="number_romaji">Mm<sup>2</sup></span>'
    if dke < -3:
        return str(float(dec_kilo) * 1000.0) + \
            u' <span class="number_romaji">km<sup>2</sup></span>'
    return swiss_format(int(dec_kilo * 1000)) + \
        u' <span class="number_romaji">km<sup>2</sup></span>'


def jp_man(txt, *args):
    """
    Return the text reformated for my geography deck.

    * Return txt when it is not a number
    * Return txt multiplied by 1'000 when it is <10
    * Return txt divided by 10 with "万" added when it is >=10
    The text is also wrapped in some classes.
    This gives nice formating for area numbers for Japanese
    prefectures in my geography deck.
    """
    # Total rework. RAS 2012-09-06
    # Parts taken from my "days" script, see
    # https://github.com/ospalh/age/blob/master/days
    try:
        dec_kilo = decimal.Decimal(txt)
    except decimal.InvalidOperation:
        # No number
        return txt
    dks, dkd, dke = dec_kilo.as_tuple()
    # order of magnitude +1
    omagp = len(dkd) + dke
    # We cheat a bit. We know that we won’t have 一億km². No check for
    # >=6.
    if omagp >= 2:
        return arab_format_string.format(float(dec_kilo) / 10.0) + \
            u'<span class="number_kanji">万</span>'
    return arab_format_string.format(int(dec_kilo * 1000))


def ch_integer(txt, *args):
    """
    Return text formated as a swiss integer if possible.
    """
    try:
        s_int = int(txt)
    except ValueError:
        return txt
    return swiss_format(s_int)


addHook('fmod_swissmega', ch_millionen)
addHook('fmod_swisssqkm', ch_t_sqkm)
addHook('fmod_swissint', ch_integer)
addHook('fmod_jpman', jp_man)
