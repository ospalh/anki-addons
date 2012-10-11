# -*- mode: python ; coding: utf-8 -*-
# A “very pythonic progress dialog”
# found at http://lateral.netmanagers.com.ar/weblog/posts/BB917.html
# © 2000-2012 Roberto Alsina
# Creative Commons Attribution-NonCommercial-ShareAlike 2.5 licence
# http://creativecommons.org/licenses/by-nc-sa/2.5/

'''
A very pythonic progress dialog.

Iterate over progress(iterator)
instead of iterator. That’s pretty much it.
'''

from aqt.qt import *


def progress(data, *args):
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
