# -*- mode: Python ; coding: utf-8 -*-
# © 2012–3 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Add-on for Anki 2 to add css classes to the typed in answer.
"""

from BeautifulSoup import BeautifulSoup

from aqt import mw
from anki.hooks import addHook

good_class = 'typedgood'
bad_class = 'typedbad'

mw.reviewer.calculateOkBadStyle()
bad_style = mw.reviewer.styleBad
good_style = mw.reviewer.styleOk


def classified_correct(res, right, typed, card):
    """
    Remove the style and replace it with classes.

    Remove the style that colors a typed answer red or green with css classes.
    It is up to the user to define styling for these classes.
    """
    print('cc: r: {}, t: {}'.format(right, typed))
    print('res {}'.format(res))
    if not res:
        res = mw.reviewer(res, right, typed, card)
        print('res now {}'.format(res))
    if not res:
        return u''
    soup = BeautifulSoup(res)
    for tag in soup.findAll(name='span'):
        print('tag: {}'.format(tag))
        try:
            style = tag['style']
        except KeyError:
            continue
        if bad_style == style:
            del tag['style']
            tag['class'] = bad_class
        if good_style == style:
            del tag['style']
            tag['class'] = good_class
    return unicode(soup)

addHook("filterTypedAnswer", classified_correct)
