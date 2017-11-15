# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2.1 to zoom in or out."""

from types import MethodType

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMenu

from aqt import mw
from aqt.webview import AnkiWebView, QWebEngineView
from anki.hooks import addHook, runHook, wrap
from anki.lang import _

__version__ = "1.1.0"

# Standard zoom factors for the main views of the central area:
deck_browser_standard_zoom = 1.0
overview_standard_zoom = 1.0
reset_required_standard_zoom = overview_standard_zoom
review_standard_zoom = 1.0
# Before you change the review_standard_zoom size, maybe you should
# use larger fonts in your decks.


# How much to increase or decrease the zoom factor with each step. The
# a little odd looking number is the fourth root of two. That means
# with four clicks you double or half the size, as precisely as
# possible.
zoom_step = 2.0**0.25


def zoom_in(step=None):
    """Increase the text size."""
    if not step:
        step = zoom_step
    mw.web.setZoomFactor(mw.web.zoomFactor() * step)


def zoom_out(step=None):
    """Decrease the text size."""
    if not step:
        step = zoom_step
    mw.web.setZoomFactor(mw.web.zoomFactor() / step)


def reset_zoom(state=None, *args):
    """Reset the text size."""
    if not state:
        state = mw.state
    standard_zoom = deck_browser_standard_zoom
    if 'overview' == state:
        standard_zoom = overview_standard_zoom
    if 'requestRequired' == state:
        standard_zoom = reset_required_standard_zoom
    if 'review' == state:
        standard_zoom = review_standard_zoom
    mw.web.setZoomFactor(standard_zoom)


def add_action(submenu, label, callback, shortcut=None):
    """Add action to menu"""
    action = QAction(_(label), mw)
    action.triggered.connect(callback)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    submenu.addAction(action)


def setup_menu():
    """Set up the zoom menu."""
    try:
        mw.addon_view_menu
    except AttributeError:
        mw.addon_view_menu = QMenu(_('&View'), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(),
            mw.addon_view_menu
        )

    mw.zoom_submenu = QMenu(_('&Zoom'), mw)
    mw.addon_view_menu.addMenu(mw.zoom_submenu)

    add_action(mw.zoom_submenu, 'Zoom &In', zoom_in, 'Ctrl++')
    add_action(mw.zoom_submenu, 'Zoom &Out', zoom_out, 'Ctrl+-')
    mw.zoom_submenu.addSeparator()

    add_action(mw.zoom_submenu, '&Reset', reset_zoom, 'Ctrl+0')


def handle_wheel_event(event):
    """
    Zoom on mouse wheel events with Ctrl.

    Zoom in our out on mouse wheel events when Ctrl is pressed.  A
    standard mouse wheel click is 120/8 degree. Zoom by one step for
    that amount.
    """
    if event.modifiers() & Qt.ControlModifier:
        step = event.angleDelta().y()
        if step > 0:
            zoom_in()
        elif step < 0:
            zoom_out()
    else:
        original_mw_web_wheelEvent(event)


def run_move_to_state_hook(state, *args):
    """Run a hook whenever we have changed the state."""
    runHook("movedToState", state)


def real_zoom_factor(self):
    """Use the default zoomFactor.

    Overwrites Anki's effort to support hiDPI screens.
    """
    return QWebEngineView.zoomFactor(self)


mw.moveToState = MethodType(wrap(mw.moveToState.__func__, run_move_to_state_hook), mw)
addHook('movedToState', reset_zoom)
original_mw_web_wheelEvent = mw.web.wheelEvent
mw.web.wheelEvent = handle_wheel_event
mw.web.zoomFactor = MethodType(real_zoom_factor, mw.web)
AnkiWebView.zoomFactor = real_zoom_factor
setup_menu()
