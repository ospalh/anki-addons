# -*- coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
# 
# Portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# See the notes in the progress function


from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
from aqt.utils import askUser

__version__ = '1.1.0'



# Field names to use. Use only lower-case here.
id_fields = ['note id', 'nid']



def progress(data, *args):
    """
    A very pythonic progress dialog.

    Iterate over progress(iterator)
    instead of iterator. That’s pretty much it.

    """
    # found at http://lateral.netmanagers.com.ar/weblog/posts/BB917.html
    # © 2000-2012 Roberto Alsina 
    # Creative Commons Attribution-NonCommercial-ShareAlike 2.5 licence
    # http://creativecommons.org/licenses/by-nc-sa/2.5/
    it=iter(data)
    widget = QProgressDialog(*args+(0,it.__length_hint__()))
    c=0
    for v in it:
        QCoreApplication.instance().processEvents()
        if widget.wasCanceled():
            raise StopIteration
        c+=1
        widget.setValue(c)
        yield(v)

def add_nids_to_all():
    """
    Add note id to all empty fields with the right names.

    Iterate over all notes and add the nid 
    """
    if not askUser("Add note id to all 'Note ID' fields?"):
        return
    # Maybe there is a way to just select the notes which have a nid
    # field. But this should work and efficency isn't too much of an
    # issue.
    nids = mw.col.db.list("select id from notes")
    # Iterate over the cards
    for nid in progress(nids, "Adding note ids.", "Stop that!"):
        n = mw.col.getNote(nid)
        # Go over the fields ...
        for name in mw.col.models.fieldNames(n.model()):
            # ... and the target field names ..
            for f in id_fields:
                # ... and compare the two
                if f == name.lower():
                    # Check if target is empty
                    if not n[name]:
                        n[name] = str(nid)
                        n.flush()
    mw.reset()

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


add_nid = QAction(mw)
add_nid.setText("Add note ids")
mw.form.menuTools.addAction(add_nid)
mw.connect(add_nid, SIGNAL("triggered()"), add_nids_to_all)

addHook('editFocusLost', onFocusLost)
