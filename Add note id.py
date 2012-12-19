# -*- mode: Python ; coding: utf-8 -*-
#
# Copyricht © 2012 Roland Sieker, <ospalh@gmail.com>
#
# Portions of this file were originally written by
# Damien Elmes <anki@ichi2.net>
#
# License: Most parts: GNU GPL, version 3 or later;
# http://www.gnu.org/copyleft/gpl.html
#
# Licence progress: see below
#
# See the notes in the progress function

"""
Anki2 add-on to make notes unique

Add the note id to a field named Note ID in
"""

from PyQt4.QtCore import QCoreApplication, SIGNAL
from PyQt4.QtGui import QAction, QProgressDialog

from anki.hooks import addHook
from anki.lang import _
from aqt import mw
from aqt.utils import askUser
from aqt.addcards import AddCards

__version__ = '1.2.1'

# Field names to use. Use only lower-case here. The field name can
# have upper-case letters. (Use "Note ID" as the field name.)
id_fields = ['note id', 'nid']

## Select one or the other line.

## You can remove the '# ' from the 'show_menu_item =
## False' line (and add one to the show_menu_item = True' line) to
## hide the 'Add note ids' menu after you have filled the fields in
## your old cards. NB.: remember to remove the space at the start of
## the line, too.
show_menu_item = True
# show_menu_item = False


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
    it = iter(data)
    widget = QProgressDialog(*args + (0, it.__length_hint__()))
    c = 0
    for v in it:
        QCoreApplication.instance().processEvents()
        if widget.wasCanceled():
            raise StopIteration
        c += 1
        widget.setValue(c)
        yield(v)


def is_idfield(f):
    """Does string f name an id field?"""
    fl = f.lower()
    for idf in id_fields:
        if fl == idf:
            return True
    return False


def add_nids_to_all():
    """
    Add note id to all empty fields with the right names.

    Iterate over all notes and add the nid
    """
    if not askUser(_(u"Add note id to all 'Note ID' fields?")):
        return
    # Maybe there is a way to just select the notes which have a nid
    # field. But this should work and efficency isn't too much of an
    # issue.
    nids = mw.col.db.list("select id from notes")
    # Iterate over the cards
    for nid in progress(nids, _(u"Adding note ids."), _(u"Stop that!")):
        n = mw.col.getNote(nid)
        # Go over the fields ...
        for name in mw.col.models.fieldNames(n.model()):
            # ... and if it's a nid fields
            if is_idfield(name) and not n[name]:
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


def can_close_add_cards(self):
    if self.forceClose or self.editor.fieldsAreBlank():
        return True
    # Work-alike for of Editor.fieldsAreBlank(), but skip the
    # note id field.
    n = self.editor.note
    # Go over the fields ...
    for name in mw.col.models.fieldNames(n.model()):
        if not is_idfield(name) and n[name]:
            return askUser(_("Close and lose current input?"))
    return True


if show_menu_item:
    add_nid = QAction(mw)
    mw.form.menuTools.addAction(add_nid)
    add_nid.setText(_(u"Add note ids"))
    mw.connect(add_nid, SIGNAL("triggered()"), add_nids_to_all)

addHook('editFocusLost', onFocusLost)
AddCards.canClose = can_close_add_cards
