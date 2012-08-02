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
ScalarField = 'Scalar'

# Factor to decide what counts as ‘good enough’. It should be > 1.0
# (or at least >= 1.0). What you use here depends on how precisely you
# want to remember your numbers.
passFactor = 2.0

# How the number is coloured.
failColour= '#f00'
passColour= '#ff0'
exactColour= '#0f0'
# (It looks like ‘red’, ‘yellow’ and ‘green’ work but are
# different colours.)



def scalarTypeAnsAnswerFilter(self, buf):
    # Redo bits of typeQuesAnswerFilter to get the field name typed in and most of the old typeAnsAnswerFilter.
    m = re.search(self.typeAnsPat, buf)
    colourString = u''
    scalarWorked = False
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
        if not fld.startswith("cq:") and ScalarField in fld:
            scalarWorked, colourString = scalarColour(cor, self.typedAnswer)
    if scalarWorked:
        return re.sub(self.typeAnsPat, """
<span id=coransscalar style="font-family: '%s'; font-size: %spx; colour: black; background: %s">%s</span>""" %
                      (self.typeFont, self.typeSize, colourString, self.typedAnswer), buf)
    else:
        return oldTypeAnsAnswerFilter(self, buf)

def scalarColour(a, b):
    """Return the colour the answer should be, red, yellow or green,
 depending on how close we are to the target."""
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
        return True, exactColour
    # Now we know that they are not the same, so either red or yellow.
    try:
        factor = 1.0 * given_value/target_value
    except ZeroDivisionError:
        return True, failColour
    if factor < 1.0/passFactor or factor > passFactor:
        return True, failColour
    return True, passColour


oldTypeAnsAnswerFilter = Reviewer.typeAnsAnswerFilter
Reviewer.typeAnsAnswerFilter = scalarTypeAnsAnswerFilter
