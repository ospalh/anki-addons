# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2 to add AnkiDroid-style replay buttons."""

import os
import re

from anki.hooks import addHook
from anki.sound import play
from aqt.reviewer import Reviewer

sound_re = "\[sound:(.*?)\]"

arrow_img_path = os.path.join(
    os.path.dirname(__file__), 'play_button_icon', 'play.png')


def play_button_filter(qa_html, qa_type, dummy_fields, dummy_model,
                       dummy_data, dummy_col):
    u"""
    Filter the questions and answers to add play buttons.
    """

    def add_button(sound):
        u"""
        Add img link after the match.

        Add an img link after the match to replay the audio. The title
        is set to "Replay" on the question side to hide information or
        to the file name on the answer.
        """
        if 'q' == qa_type:
            title = u"Replay"
        else:
            title = sound.group(1)
        return u"""{orig}<a href='javascript:py.link("ankiplay{fn}");' \
title="{ttl}"><img src="{ip}" alt="play" style="display: inline; \
max-height: 1em;" class="replaybutton"></a>""".format(
            orig=sound.group(0), fn=sound.group(1), ip=arrow_img_path,
            ttl=title)
    return re.sub(sound_re, add_button, qa_html)


def link_handler_wrapper(reviewer, url):
    u"""Play the sound or call the original link handler."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        original_link_handler(reviewer, url)


original_link_handler = Reviewer._linkHandler
Reviewer._linkHandler = link_handler_wrapper

addHook("mungeQA", play_button_filter)
