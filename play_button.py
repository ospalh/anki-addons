# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2013–16 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to add AnkiDroid-style replay buttons."""

import os
import re
import shutil

from BeautifulSoup import BeautifulSoup
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QDesktopServices

from anki.cards import Card
from anki.hooks import addHook, wrap
from anki.sound import play
from aqt import mw
from aqt.browser import Browser
from aqt.browser import DataModel
from aqt.clayout import CardLayout
from aqt.reviewer import Reviewer

__version__ = "2.0.0"

sound_re = ur"\[sound:(.*?)\]"

hide_class_name = u'browserhide'


def svg_css(Card):
    """Add the svg button style to the card style"""
    return u"""<style scoped>
.replaybutton span {
  display: inline-block;
  vertical-align: middle;
  padding: 5px;
}

.replaybutton span svg {
  stroke: none;
  fill: black;
  display: inline;
  height: 1em;
  width: 1em;
  min-width: 12px;
  min-height: 12px;
}
</style>
""" + old_css(Card)


def play_button_filter(
        qa_html, qa_type, dummy_fields, dummy_model, dummy_data, dummy_col):
    u"""
    Filter the questions and answers to add play buttons.
    """

    def add_button(sound):
        u"""
        Add a button after the match.

        Add a button after the match to replay the audio. The title is
        set to "Replay" on the question side to hide information or to
        the file name on the answer.
        """
        if 'q' == qa_type:
            title = u"Replay"
        else:
            title = sound.group(1)
        return u"""{orig}<a href='javascript:py.link("ankiplay{fn}");' \
title="{ttl}" class="replaybutton browserhide"><span><svg viewBox="0 0 32 32">\
<polygon points="11,25 25,16 11,7"/>Replay</svg></span></a>\
<span style="display: none;">&#91;sound:{fn}&#93;</span>""".format(
            orig=sound.group(0), fn=sound.group(1), ttl=title)
        # The &#91; &#93; are the square brackets that we want to
        # appear as brackets and not trigger the playing of the
        # sound. The span inside the a around the svg is there to
        # bring this closer in line with AnkiDroid.
    return re.sub(sound_re, add_button, qa_html)


def review_link_handler_wrapper(reviewer, url):
    u"""Play the sound or call the original link handler."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        original_review_link_handler(reviewer, url)


def simple_link_handler(url):
    u"""Play the file."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        QDesktopServices.openUrl(QUrl(url))


def add_clayout_link_handler(clayout, dummy_t):
    u"""Make sure we play the files from the card layout window."""
    clayout.forms[-1]['pform'].frontWeb.setLinkHandler(simple_link_handler)
    clayout.forms[-1]['pform'].backWeb.setLinkHandler(simple_link_handler)


def add_preview_link_handler(browser):
    u"""Make sure we play the files from the preview window."""
    browser._previewWeb.setLinkHandler(simple_link_handler)


def reduce_format_qa(self, text):
    u"""Remove elements with a given class before displaying."""
    soup = BeautifulSoup(text)
    for hide in soup.findAll(True, {'class': re.compile(
            '\\b' + hide_class_name + '\\b')}):
        hide.extract()
    return original_format_qa(self, unicode(soup))


original_review_link_handler = Reviewer._linkHandler
Reviewer._linkHandler = review_link_handler_wrapper

original_format_qa = DataModel.formatQA
DataModel.formatQA = reduce_format_qa

old_css = Card.css
Card.css = svg_css

addHook("mungeQA", play_button_filter)
Browser._openPreview = wrap(Browser._openPreview, add_preview_link_handler)
CardLayout.addTab = wrap(CardLayout.addTab, add_clayout_link_handler)
