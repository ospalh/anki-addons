# -*- mode: python ; coding: utf-8 -*-
# From http://www.peterbe.com/plog/uniqifiers-benchmark

u"""Return a copy of the list with every element appearing only once."""


def uniqify_list(seq):
    u"""Return a copy of the list with every element appearing only once."""
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes
