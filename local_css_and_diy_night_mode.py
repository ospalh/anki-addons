# -*- mode: python ; coding: utf-8 -*-
#
# © copyright 2012 Roland Sieker <ospalh@gmail.com>
# Contains snippets of code from anki proper,
# written by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
# Insipired by CSS Modify Style-Sheet input by DAThomas

"""
Load local CSS and add it to the cards.

This is an add-on for Anki 2 SRS.
Load the file 'user_style.css' from the user’s profile folder
(e.g. "~/Anki/User 1/user_style.css") and add it to the cards, before
the style from the template.
"""

from PyQt5.QtWidgets import QAction, QActionGroup, QMenu
from PyQt5.QtCore import SIGNAL

import os
import re
from anki.cards import Card
from anki.consts import MODEL_STD
from anki import hooks
from aqt import mw


__version__ = '1.4.0'

user_css_name = 'user_style.css'
"""File name of the user's CSS"""
css_encoding = 'utf-8'
"""Encoding of the user's CSS file"""
local_class = 'loc'
"""Class added to all cards"""

user_css = u''

extra_classes_list = [
    {'class': 'night', 'display': u'Night mode'},
    ]
extra_class = None


def fix_body_class():
    u"""
    Add classes to body.

    Add classes to the html body, so the local CSS mechanism works
    together with CSS definitions for web review. Use
    ".loc.card"—without space—for the card and ".loc .classNN"—with a
    space—for sub-elements in you user_style.css.
    """
    # Gather all the A-Za-z0-9_ characters from the template and model
    # names and add those as class.
    model = mw.reviewer.card.model()
    if model['type'] == MODEL_STD:
        template_nr = mw.reviewer.card.ord
    else:
        template_nr = 0
    template_class = re.sub(r'[\W_]+', u'',
                            model['tmpls'][template_nr]['name']).lower()
    model_class = re.sub(r'[\W_]+', u'', model['name']).lower()
    body_class = r'{0} card card{1} template_{2} model_{3}'.format(
        local_class, mw.reviewer.card.ord + 1,
        template_class, model_class)
    try:
        body_class += ' ' + extra_class
    except TypeError:
        pass
    mw.web.eval(u"document.body.className = '{0}';".format(body_class))


def get_user_css():
    """
    Load the user's CSS data from disk.
    """
    global user_css
    css_path = os.path.join(mw.pm.profileFolder(), user_css_name)
    try:
        with open(css_path, 'r') as f:
            user_css = unicode(f.read(), css_encoding)
    except IOError:
        pass


def localized_card_css(self):
    """Set the css for a card"""
    return_css = u''
    if user_css:
        return_css = '<style scoped>%s</style>' % user_css
    return return_css + old_css(self)


def set_extra_class(new_extra_class):
    u"""Set the varible so the extra class is used on the next card."""
    global extra_class
    extra_class = new_extra_class


def setup_menu():
    u"""
    Add a submenu to a view menu.

    Add a submenu that lists the available extra classes to the view
    menu, creating that menu when neccessary
    """
    if extra_classes_list:
        try:
            mw.addon_view_menu
        except AttributeError:
            mw.addon_view_menu = QMenu(_(u"&View"), mw)
            mw.form.menubar.insertMenu(
                mw.form.menuTools.menuAction(), mw.addon_view_menu)
        mw.extra_class_submenu = QMenu(u"Mode (e&xtra class)", mw)
        mw.addon_view_menu.addMenu(mw.extra_class_submenu)
        action_group = QActionGroup(mw, exclusive=True)
        no_class_action = action_group.addAction(
            QAction('(none/standard)', mw, checkable=True))
        no_class_action.setChecked(True)
        mw.extra_class_submenu.addAction(no_class_action)
        mw.connect(no_class_action, SIGNAL("triggered()"),
                   lambda: set_extra_class(None))
        for ecd in extra_classes_list:
            nn_class_action = action_group.addAction(
                QAction(ecd['display'], mw, checkable=True))
            mw.extra_class_submenu.addAction(nn_class_action)
            mw.connect(nn_class_action, SIGNAL("triggered()"),
                       lambda ec=ecd['class']: set_extra_class(ec))


old_css = Card.css
Card.css = localized_card_css


hooks.addHook("showQuestion", fix_body_class)
hooks.addHook("profileLoaded", get_user_css)

setup_menu()
