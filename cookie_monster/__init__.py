# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2014–17 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Add-on for Anki 2.1 to add AnkiDroid-style replay buttons."""

import re
import urllib.parse
from aqt.qt import *
from aqt.webview import AnkiWebPage
from aqt import mw


def setHtmlWithBaseurl(self, html):
    """Pass along the base url when setting the HTML

    Because something, something, security, you are not allowed to
    pass along cookis to a webview page, unless you set the baseurl,
    too. So do that. With exception handling if we can’t find it.
    """
    app = QApplication.instance()
    oldFocus = app.focusWidget()
    self._domDone = False
    try:
        base_url = QUrl(
            urllib.parse.unquote(
                re.search('<base href="(.*?)">', html).group(1)) +
            "__viewer__.html")
    except AttributeError as ae:
        self._page.setHtml(html)
    else:
        self._page.setHtml(html, base_url)
        # work around webengine stealing focus on setHtml()
    if oldFocus:
        oldFocus.setFocus()


AnkiWebPage.setHtml = setHtmlWithBaseurl
mw.web._setHtml = setHtmlWithBaseurl
