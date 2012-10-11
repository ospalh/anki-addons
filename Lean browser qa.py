#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from lxml import html
from aqt.browser import DataModel

__version__ = "1.0.1"

# Define the name of the class you want to be hidden in the browser.
hide_class_selector = '.browserhide'


def reduce_format_qa(self, text):
    doc = html.fromstring(text)
    for el in doc.cssselect(hide_class_selector):
        el.drop_tree()
    return old_format_qa(self,
                         unicode(html.tostring(doc, encoding='utf-8'),'utf-8'))


old_format_qa = DataModel.formatQA
DataModel.formatQA = reduce_format_qa
