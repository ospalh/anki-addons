# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2014–17 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2.1 to add AnkiDroid-style replay buttons."""

import re
import urllib.parse
from aqt.webview import AnkiWebPage
from aqt import mw
from PyQt5.QtCore import QUrl

def setHtmlWithBaseurl(webpage, html):
    try:
        base_url = QUrl(
            urllib.parse.unquote(
                re.search('<base href="(.*?)">', html).group(1)) +
            "__viewer__.html")
    except AttributeError as ae:
        original_setHtml(webpage, html)
    else:
        original_setHtml(webpage, html, base_url)


original_setHtml = AnkiWebPage.setHtml

AnkiWebPage.setHtml = setHtmlWithBaseurl
#mw.web._page.setHtml = setHtmlWithBaseurl
