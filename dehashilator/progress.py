# -*- mode: python ; coding: utf-8 -*-
# A “very pythonic progress dialog”
# © 2000-2012 Roberto Alsina 
# Creative Commons Attribution-NonCommercial-ShareAlike 2.5 licence
# http://creativecommons.org/licenses/by-nc-sa/2.5/

def progress(data, *args):
    it=iter(data)
    widget = QtGui.QProgressDialog(*args+(0,it.__length_hint__()))
    c=0
    for v in it:
        QtCore.QCoreApplication.instance().processEvents()
        if widget.wasCanceled():
            raise StopIteration
        c+=1
        widget.setValue(c)
        yield(v)

