# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2 to zoom in or out."""

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QAction, QKeySequence, QMenu

from aqt import mw
from anki.hooks import addHook, runHook, wrap
from anki.lang import _

__version__ = "1.0.0"

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
    u"""Increase the text size."""
    if not step:
        step = zoom_step
    mw.web.setTextSizeMultiplier(mw.web.textSizeMultiplier() * step)


def zoom_out(step=None):
    u"""Decrease the text size."""
    if not step:
        step = zoom_step
    mw.web.setTextSizeMultiplier(mw.web.textSizeMultiplier() / zoom_step)


def reset_zoom(state=None, *args):
    u"""Reset the text size."""
    if not state:
        state = mw.state
    standard_zoom = deck_browser_standard_zoom
    if 'overview' == state:
        standard_zoom = overview_standard_zoom
    if 'requestRequired' == state:
        standard_zoom = reset_required_standard_zoom
    if 'review' == state:
        standard_zoom = review_standard_zoom
    mw.web.setTextSizeMultiplier(standard_zoom)


def setup_menu():
    u"""Set up the zoom menu."""
    try:
        mw.addon_view_menu
    except AttributeError:
        mw.addon_view_menu = QMenu(_(u"&View"), mw)
        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(), mw.addon_view_menu)
    mw.zoom_submenu = QMenu(_(u"&Zoom"), mw)
    mw.addon_view_menu.addMenu(mw.zoom_submenu)
    zoom_in_action = QAction(_('Zoom &In'), mw)
    zoom_in_action.setShortcut(QKeySequence("Ctrl++"))
    mw.zoom_submenu.addAction(zoom_in_action)
    mw.connect(zoom_in_action, SIGNAL("triggered()"), zoom_in)
    zoom_out_action = QAction(_('Zoom &Out'), mw)
    zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
    mw.zoom_submenu.addAction(zoom_out_action)
    mw.connect(zoom_out_action, SIGNAL("triggered()"), zoom_out)
    mw.zoom_submenu.addSeparator()
    reset_zoom_action = QAction(_('&Reset'), mw)
    reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
    mw.zoom_submenu.addAction(reset_zoom_action)
    mw.connect(reset_zoom_action, SIGNAL("triggered()"), reset_zoom)


def handle_wheel_event(event):
    u"""
    Zoom on mouse wheel events with Ctrl.

    Zoom in our out on mouse wheel events when Ctrl is pressed.  A
    standard mouse wheel click is 120/8 degree. Zoom by one step for
    that amount.
    """
    if event.modifiers() & Qt.ControlModifier:
        step = event.delta() / 120 * zoom_step
        if step > 0:
            zoom_in(step)
        else:
            zoom_out(-step)
    else:
        original_mw_web_wheelEvent(event)


def run_move_to_state_hook(state, *args):
    u"""Run a hook whenever we have changed the state."""
    runHook("movedToState", state)


mw.moveToState = wrap(mw.moveToState, run_move_to_state_hook)
addHook("movedToState", reset_zoom)
original_mw_web_wheelEvent = mw.web.wheelEvent
mw.web.wheelEvent = handle_wheel_event

setup_menu()
