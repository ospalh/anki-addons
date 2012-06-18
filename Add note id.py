# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# Portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#


from anki.hooks import addHook
from aqt import mw

__version__ = '1.0.0'

# Field names to use. Use only lower-case here.
id_fields = ['note id', 'nid', 'id', 'nr', 'no']

def onFocusLost(flag, n, fidx):
    field_name = None
    for c, name in enumerate(mw.col.models.fieldNames(n.model())):
        for f in id_fields:
            if f == name.lower():
                field_name = name
                field_index = c
                # I would like to break out of the nested for loops
                # here. In C++ you are allowed to use a goto for that.
                # ^_^ Nothing bad will happen when we go on, though.
    if not field_name:
        return flag
    # Field already filled
    if n[field_name]:
        return flag
    # event not coming from id field?
    if field_index != fidx:
        return flag
    # Got to here: We have an empty id field, so put in a number.
    n[field_name] = str(n.id)
    return True

addHook('editFocusLost', onFocusLost)
