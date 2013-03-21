# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2 to colour a typed in numeric answer."""

import re

from aqt.reviewer import Reviewer
from anki.utils import stripHTML
from anki.hooks import addHook


__version__ = "2.0.0"

# Code word to look for in the field name to decide whether to do the
# number comparison:
scalar_field = 'scalar'
"""Code word needed to tread input as number"""

# Factor to decide what counts as ‘good enough’. It should be > 1.0
# (or at least >= 1.0). What you use here depends on how precisely you
# want to remember your numbers.
pass_factor = 1.5
"""Factor that defines what gets a yellow color."""

# How the number is coloured.
fail_color = '#f00'
pass_color = '#ff0'
exact_color = '#0f0'
# (It looks like ‘red’, ‘yellow’ and ‘green’ work but are
# different colours.)

# And the classes that are added.
fail_class = 'scalarfail'
pass_class = 'scalarpass'
exact_class = 'scalarexact'

# Just for me: don't set background color (directly)
scalar_format_string = """<span class="typedscalar {cl}" \
style="background-color: {bg};">{num}</span>"""


def correct_scalar(res, right, typed, card):
    """
    Return numeric answer in red, yellow or green.

    When certain conditions are met, return the typed-in answer in
    red, yellow or green, depending how close the given answer was to
    the correct one.
    """
    try:
        fld = re.search('\[\[type:([^\]]+)\]\]', card.a()).group(1)
    except AttributeError:
        # No typed answer to show at all.
        return res
    if not scalar_field in fld.lower() or fld.startswith("cq:"):
        return res
    try:
        color_string, class_string = scalar_color_class(right, typed)
    except ValueError:
        # not floats
        return res
    else:
        return scalar_format_string.format(
            cl=class_string, bg=color_string, num=typed)


def scalar_color_class(t, g):
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
        return exact_color, exact_class
    # Now we know that they are not the same, so either red or yellow.
    try:
        factor = 1.0 * given_value / target_value
    except ZeroDivisionError:
        return fail_color, fail_class
    if factor < 1.0 / pass_factor or factor > pass_factor:
        return fail_color, fail_class
    return pass_color, pass_class


addHook("filterTypedAnswer", correct_scalar)
