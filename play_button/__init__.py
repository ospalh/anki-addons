# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2013–17 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to add AnkiDroid-style replay buttons."""

import html.parser
import os
import re
import shutil
import urllib.parse

from bs4 import BeautifulSoup
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices


from anki.cards import Card
from anki.hooks import addHook, wrap
from anki.sound import play
from aqt import mw
from aqt.browser import Browser
from aqt.browser import DataModel
from aqt.clayout import CardLayout
from aqt.reviewer import Reviewer

__version__ = "3.1.0"

sound_re = r"\[sound:(.*?)\]"

hide_class_name = u'browserhide'


def svg_css(Card):
    """Add the svg button style to the card style"""
    return """<style scoped>
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
    """
    Filter the questions and answers to add play buttons.
    """

    def add_button(sound):
        """Add a button after the match.

        Add a button after the match to replay the audio. The title is
        set to "Replay" on the question side to hide information or to
        the file name on the answer.

        The filename is first unescaped and then percentage
        encoded. For example, an image of a German rock album may go
        from “&Ouml;.jpg” to “Ö.jpg” to “%C3%96.jpg”.

        """
        fn = sound.group(1)
        # Cut out some escaping of HTML enteties that is done
        # automatically by BS4
        unescaped_fn = html.parser.HTMLParser().unescape(fn)
        clean_fn = urllib.parse.quote(unescaped_fn)
        if 'q' == qa_type:
            title = "Replay"
        else:
            title = fn
        return """{orig}<a href='javascript:pycmd("ankiplay{link_fn}");' \
title="{ttl}" class="replaybutton browserhide"><span><svg viewBox="0 0 32 32">\
<polygon points="11,25 25,16 11,7"/>Replay</svg></span></a>\
<span style="display: none;">&#91;sound:{fn}&#93;</span>""".format(
            orig=sound.group(0), link_fn=clean_fn, ttl=title, fn=fn)
        # The &#91; &#93; are the square brackets that we want to
        # appear as brackets and not trigger the playing of the
        # sound. The span inside the a around the svg is there to
        # bring this closer in line with AnkiDroid.
    return re.sub(sound_re, add_button, qa_html)


def review_link_handler_wrapper(reviewer, url):
    """Play the sound or call the original link handler."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        original_review_link_handler(reviewer, url)


def simple_link_handler(url):
    """Play the file."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        QDesktopServices.openUrl(QUrl(url))


def add_clayout_link_handler(clayout, dummy_t):
    """Make sure we play the files from the card layout window."""
    clayout.forms[-1]['pform'].frontWeb.setLinkHandler(simple_link_handler)
    clayout.forms[-1]['pform'].backWeb.setLinkHandler(simple_link_handler)


def add_preview_link_handler(browser):
    """Make sure we play the files from the preview window."""
    browser._previewWeb.setLinkHandler(simple_link_handler)


def reduce_format_qa(self, text):
    """Remove elements with a given class before displaying."""
    soup = BeautifulSoup(text, 'html.parser')
    for hide in soup.findAll(True, {'class': re.compile(
            '\\b' + hide_class_name + '\\b')}):
        hide.extract()
    return original_format_qa(self, unicode(soup))


original_review_link_handler = Reviewer._linkHandler
Reviewer._linkHandler = review_link_handler_wrapper

# TODO: hide stuff from the browser again
#original_format_qa = DataModel.formatQA
#DataModel.formatQA = reduce_format_qa

old_css = Card.css
Card.css = svg_css

addHook("mungeQA", play_button_filter)
# Browser._openPreview = wrap(Browser._openPreview, add_preview_link_handler)

# TODO: fix this
#CardLayout.addTab = wrap(CardLayout.addTab, add_clayout_link_handler)
