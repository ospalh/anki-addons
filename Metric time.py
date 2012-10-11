# -*- mode: python ; coding: utf-8 -*-
# © 2012 Roland Sieker <ospalh@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import math
from decimal import Decimal
from anki import utils, sched, stats
from anki.lang import _
# To override fmtTimeSpan that are already loaded:
from aqt import browser, deckbrowser, reviewer

"""Replace time values with just days or years."""

__version__ = "1.0.0"

day_format_separators = {-1: u'.', -3: u"’", -4: u"’", -6: u"’"}
year = 365.2421897


def omag(x):
    """Return the order of magnitude of a number."""
    try:
        return int(math.floor(math.log10(abs(x))))
    except ValueError:
        return 0


def days_from_s(seconds, sigfig=2, short=False, maybe_show_years=True):
    """
    Return a value formated in a specific way.

    Returns a string that represents the number of days given as an
    argument formated in a specific way that should make parsing the
    decimal part of the age easier for humans.
    """
    days = seconds / 86400.0
    if days > year and maybe_show_years:
        if short:
            return"{0:.1f}".format(days / year) + _("&#8239;a")
        else:
            return"{0:.1f} ".format(days / year) + _("years")
    # Calculate how many digits to show. Show full precision of days,
    # limited for shorter times.
    show_digits = max(sigfig - omag(days) - 1, 0)
    out_string = ''
    if 0 == show_digits:
        out_string = str(int(round(days, 0)))
    else:
        decimal_days = Decimal(str(days)) \
            .quantize(Decimal('0.' + '0' * (show_digits - 1) + '1'))
        dec_sign, dec_digits, dec_exponent = decimal_days.as_tuple()
        ndig = len(dec_digits)
        if dec_sign:
            out_string = '-'
        for pad in range(0, dec_exponent + ndig - 1, -1):
            try:
                out_string += day_format_separators[pad]
            except KeyError:
                pass
            out_string += '0'
        for ex, dg in enumerate(dec_digits):
            # Add a decorator if it is the right position
            try:
                out_string += \
                    day_format_separators[-ex + dec_exponent + ndig - 1]
            except KeyError:
                pass
            out_string += str(dg)
    if short:
        out_string += _("&#8239;d")
    else:
        out_string += _(" days")
    return out_string


def metric_time_span(time, pad=0, point=0, short=False, after=False, unit=99):
    return days_from_s(time, short=short, maybe_show_years=True)

old_fmt_time_span = utils.fmtTimeSpan
utils.fmtTimeSpan = metric_time_span

# We have to override these by hand, as they have already been
# included when this file is loaded.
browser.fmtTimeSpan = metric_time_span
deckbrowser.fmtTimeSpan = metric_time_span
reviewer.fmtTimeSpan = metric_time_span
sched.fmtTimeSpan = metric_time_span
stats.fmtTimeSpan = metric_time_span
