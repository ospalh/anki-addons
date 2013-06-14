# -*- mode: Python ; coding: utf-8 -*-
# Copyright © 2012–2013 Roland Sieker <ospalh@gmail.com>
# Based in part on code by Damien Elmes <anki@ichi2.net>
#
# License: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2 to colour a typed in numeric answer."""

import re

from aqt.reviewer import Reviewer
from anki.cards import Card
from anki.utils import stripHTML
from anki.hooks import wrap


__version__ = "2.1.0"

# Code word to look for in the field name to decide whether to do the
# number comparison:
scalar_field = 'scalar'
"""Code word needed to tread input as number"""

# Factor to decide what counts as ‘good enough’. It should be > 1.0
# (or at least >= 1.0). What you use here depends on how precisely you
# want to remember your numbers.


pass_factor = 2.0
"""Factor that defines what gets a yellow color."""

# And the classes that are added.
fail_class = 'typeBad'
pass_class = 'typePass'
exact_class = 'typeGood'



scalar_css = u"""
<style scoped>
.{tp} {{background-color:  #ff0; }}
</style>
""".format(tp=pass_class)

exact_format_string = u"""\
<div id=typeans class="typedscalar">
<span class="{cl} allGood">{num}</span>
</div>
"""
two_num_format_string = u"""\
<div id=typeans class="typedscalar corrected">
<span class="{cl} given">{g}</span>
<span class="arrow">→</span>
<span class="{ccl} correct">{c}</span>
</div>
"""


def scalar_card_css(self):
    u"""Add the colors for this to the css."""
    return scalar_css + old_css(self)

def correct_scalar(reviewer, given, correct, showBad=True, _old=None):
    u"""
    Return numeric answer with red, yellow or green background.

    When certain conditions are met, return the typed-in answer with
    CSS classes added that give them a red, yellow or green
    background, depending how close the given answer was to the
    correct one.
    """
    try:
        fld = re.search('\[\[type:([^\]]+)\]\]', reviewer.card.a()).group(1)
    except AttributeError:
        # No typed answer to show at all.
        return _old(reviewer, given, correct, showBad)
    if not scalar_field in fld.lower() or fld.startswith("cq:"):
        return _old(reviewer, given, correct, showBad)
    try:
        class_string = scalar_color_class(given, correct)
    except ValueError:
        return _old(reviewer, given, correct, showBad)
    else:
        if class_string == exact_class:
            return exact_format_string.format(cl=class_string, num=given)
        else:
            return two_num_format_string.format(
                cl=class_string, g=given, c=correct, ccl=exact_class)


def scalar_color_class(g, t):
    """
    Return a color string and a class string.

    Return a string that can be used to color an html text and a
    string that can be used as a css class. The color is red, yellow
    or green depending on how close the two numbers t and g are to
    each other, the class describes this fact.

    When t and g can't be converted to numbers, the ValueError of that
    conversion is not caught.
    """
    try:
        target_value = int(t)
        given_value = int(g)
    except ValueError:
        # New style: no try here. Catch that case higher up.
        target_value = float(t)
        given_value = float(g)
    # One of the two conversions worked: we have two valid numbers, two
    # ints or two floats. We don’t really care which.
    if target_value == given_value:
        return exact_class
    # Now we know that they are not the same, so either red or yellow.
    try:
        factor = 1.0 * given_value / target_value
    except ZeroDivisionError:
        return fail_class
    if factor < 1.0 / pass_factor or factor > pass_factor:
        return fail_class
    return pass_class


Reviewer.correct = wrap(Reviewer.correct, correct_scalar, "around")

old_css = Card.css
Card.css = scalar_card_css
