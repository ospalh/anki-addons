#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

import re
from BeautifulSoup import BeautifulSoup
from aqt.browser import DataModel

# Define the name of the class you want to be hidden in the browser.
hide_class_name = u'browserhide'


def reduce_format_qa(self, text):
    soup = BeautifulSoup(text)
    for hide in soup.findAll(True,
                        {'class': re.compile('\\b' + hide_class_name + '\\b')}):
        hide.extract()
    return old_format_qa(self, unicode(soup))


old_format_qa = DataModel.formatQA
DataModel.formatQA = reduce_format_qa
