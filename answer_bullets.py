# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2014 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html
#
#

"""
Anki plugin to indicate which answer button was pressed.

This addon to Anki2 shows from one to four little dots indicating
which answer button was pressed, similar to the way AnkiDroid does.

"""

from anki.hooks import wrap
from aqt.reviewer import Reviewer

__version__ = '0.1.0'


bullets_display_time = 2000  # ms
ease_bullet_styles = {
    1: u'color: #c35617; visibility: visible;',
    2: u'color: black; visibility: visible;',
    3: u'color: #070; visibility: visible;',
    4: u'color: #070; visibility: visible;'}
no_bullet_style = u"visibility: hidden;"


def show_answer_dots(reviewer, ease):
    """Show n=ease dots.

    Show a number of dots to the left of the answer timer (or at the
    top rightof the bottom button area) indicating which answer button
    was pressed.

    This is inspired by AnkiDroid, where this is an undocumented
    feature.
    """
    try:
        ease_style = ease_bullet_styles[ease]
    except KeyError:
        ease_style = no_bullet_style
        return
    reviewer.bottom.web.eval(
        u'''\
$("#easebullets").text("{txt}");
$("#easebullets").attr("style", "{stl}");
setTimeout(function(){{$("#easebullets").attr(\
    "style", "{cstl}");}}, {to});'''.format(
        txt=u'•' * ease, stl=ease_style, cstl=no_bullet_style,
        to=bullets_display_time))


def reviewer_bottom_html(reviewer, _old=None):
    """Add the bullet span"""
    txt = _old(reviewer)
    txt = txt.replace(
        '<span id=time',
        '<span class="stattxt" id="easebullets"></span><span id=time'
    )
    return txt


Reviewer._answerCard = wrap(Reviewer._answerCard, show_answer_dots, "after")
Reviewer._bottomHTML = wrap(
    Reviewer._bottomHTML, reviewer_bottom_html, "around")
