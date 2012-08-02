# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# Based in part on code by Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt.reviewer import Reviewer
from anki.utils import stripHTML
import re
"""Add-on for Anki 2 to colour a typed in numeric answer."""


# Code word to look for in the field name to decide whether to do the
# number comparison:
scalar_field = 'Scalar'

# Factor to decide what counts as ‘good enough’. It should be > 1.0
# (or at least >= 1.0). What you use here depends on how precisely you
# want to remember your numbers.
pass_factor = 1.5

# How the number is coloured.
fail_color= '#f00'
pass_color= '#ff0'
exact_color= '#0f0'
# (It looks like ‘red’, ‘yellow’ and ‘green’ work but are
# different colours.)



def scalar_type_ans_answer_filter(self, buf):
    # Redo bits of typeQuesAnswerFilter to get the field name typed in and most of the old typeAnsAnswerFilter.
    m = re.search(self.typeAnsPat, buf)
    colour_string = u''
    scalar_worked = False
    if not self.typeCorrect:
        return re.sub(self.typeAnsPat, "", buf)
    # tell webview to call us back with the input content
    # Copy-and-pasted. I guess it’s harmless
    self.web.eval("_getTypedText();")
    # munge correct value
    cor = self.mw.col.media.strip(stripHTML(self.typeCorrect))
    # Cascade of tests
    if m:
        fld = m.group(1)
        if not fld.startswith("cq:") and scalar_field in fld:
            scalar_worked, colour_string = scalar_color(cor, self.typedAnswer)
    if scalar_worked:
        return re.sub(self.typeAnsPat, """
<span id=coransscalar style="font-family: '%s'; font-size: %spx; colour: black; background: %s">%s</span>""" %
                      (self.typeFont, self.typeSize, colour_string, self.typedAnswer), buf)
    else:
        return old_type_ans_answer_filter(self, buf)

def scalar_color(a, b):
    """
    Return a Boolean and a color string.

    Return True and a string that can be used to color a html text. The color
    is a red, yellow or green depending on how close the two numbers a
    and b are to each other.

    When a and b can't be converted to numbers, False and an empty
    string is returend.
    """
    try:
        target_value = int(a)
        given_value =  int(b)
    except ValueError:
        try:
            target_value = float(a)
            given_value =  float(b)
        except ValueError:
            return False, u''
    # One of the two conversions worked: we have two valid numbers, two
    # ints or two floats. We don’t really care which.
    if target_value == given_value:
        return True, exact_color
    # Now we know that they are not the same, so either red or yellow.
    try:
        factor = 1.0 * given_value/target_value
    except ZeroDivisionError:
        return True, fail_color
    if factor < 1.0/pass_factor or factor > pass_factor:
        return True, fail_color
    return True, pass_color


old_type_ans_answer_filter = Reviewer.typeAnsAnswerFilter
Reviewer.typeAnsAnswerFilter = scalar_type_ans_answer_filter
