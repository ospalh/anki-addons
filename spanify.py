# -*- mode: python ; coding: utf-8 -*-
# original copyright 2013 Thomas TEMPE <thomas.tempe@alysse.org>
# as Strikethrough button in editor window
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/licenses/agpl.html

u"""
Anki2 add-on to put text in spans with classes.

This is an Anki2 add-on that adds three buttons to the card
editor. Clicking on the buttons wraps the selected text in <span>s
with class style1, style2 or style3. The user can then set up eir card
templates to modify the appearence of these texts.
"""

from anki.hooks import addHook
from aqt.editor import Editor

__version__ = "2.1.0"


def add_span(editor, s_class):
    u"""Call js function to wrap text in the span."""
    editor.web.eval(
        ur"""wrap('<span class=\"{cls}\">', '</span>');""".format(
            cls=s_class))


def setup_buttons(editor):
    u"""Add the buttons to the editor."""
    editor._addButton(
        "boxed_button", lambda ed=editor, sc=u"boxed": add_span(ed, sc),
        text=u"☐", tip="boxed")

Editor.add_span = add_span
addHook("setupEditorButtons", setup_buttons)
