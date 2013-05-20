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


def play_button_filter(qa, dummy_card):
    u"""
    Filter the questions and answers to add play buttons.
    """

    def add_button(sound):
        u"""Add img link after the match."""
        return u"""{orig}<a href='javascript:py.link("ankiplay{fn}");' \
title="{fn}"><img src="{ip}" alt="play" style="display: inline; height: 1em; \
vertical-align: center;"></a>""".format(
            orig=sound.group(0), fn=sound.group(1), ip=arrow_img_path)
    return re.sub(sound_re, add_button, qa)


def link_handler_wrapper(reviewer, url):
    u"""Play the sound or call the original link handler."""
    if url.startswith("ankiplay"):
        play(url[8:])
    else:
        original_link_handler(reviewer, url)


original_link_handler = Reviewer._linkHandler
Reviewer._linkHandler = link_handler_wrapper

addHook("filterQuestionText", play_button_filter)
addHook("filterAnswerText", play_button_filter)
