# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""Add-on for Anki 2 to colour a typed in numeric answer."""

import re

from aqt.reviewer import Reviewer
from anki.utils import stripHTML


__version__ = "1.0.1"

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

scalar_format_string = "<span class=\"typedscalar {0}\" " + \
    "style=\"font-family: '{1}'; font-size: {2} px; " + \
    "background-color: {3}\">{4}</span>"


def scalar_type_ans_answer_filter(self, buf):
    """
    Return numeric answer in red, yellow or green.

    When certain conditions are met, return the typed-in answer in
    red, yellow or green, depending how close the given answer was to
    the correct one.
    """
    # Redo bits of typeQuesAnswerFilter to get the field name typed in
    # and most of the old typeAnsAnswerFilter.
    m = re.search(self.typeAnsPat, buf)
    if not self.typeCorrect:
        return re.sub(self.typeAnsPat, "", buf)
    # tell webview to call us back with the input content
    # Copy-and-pasted. I guess it’s harmless
    self.web.eval("_getTypedText();")
    # munge correct value
    cor = self.mw.col.media.strip(stripHTML(self.typeCorrect))
    # Cascade of tests
    try:
        fld = m.group(1)
    except AttributeError:
        # No typed answer field.
        return old_type_ans_answer_filter(self, buf)
    if scalar_field in fld.lower() and not fld.startswith("cq:"):
        try:
            color_string, class_string = \
                scalar_color_class(cor, self.typedAnswer)
        except ValueError:
            # not floats
            return old_type_ans_answer_filter(self, buf)
        else:
            return re.sub(
                self.typeAnsPat,
                scalar_format_string.format(class_string, self.typeFont,
                                            self.typeSize, color_string,
                                            self.typedAnswer),
                buf)
    # Still here not really scalar.:
    return old_type_ans_answer_filter(self, buf)


def scalar_color_class(a, b):
    """
    Return a color string and a class string.

    Return a string that can be used to color a html text and a
    string that can be used as css class. The color is a red, yellow
    or green depending on how close the two numbers a and b are to
    each other, the class describes this fact.

    When a and b can't be converted to numbers, the ValueError of that
    conversion is not caught.
    """
    try:
        target_value = int(a)
        given_value = int(b)
    except ValueError:
        # New style: no try here. Catch that case higher up.
        target_value = float(a)
        given_value = float(b)
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


old_type_ans_answer_filter = Reviewer.typeAnsAnswerFilter
Reviewer.typeAnsAnswerFilter = scalar_type_ans_answer_filter
