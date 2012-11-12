#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""Get a site icon as a QIcon."""

import urllib
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup as soup
from PyQt4.QtGui import QImage, QPixmap
from PyQt4.QtCore import Qt

icon_size = 20


def get_icon(url, agent=None):
    """
    Get a site icon for an URL or for an already loaded page.

    Get the site icon, either the 'rel="icon"' or the favicon, for the
    web page at url or passed in as page_html. Return a PyQt4 QPixmap.
    """
    page_request = urllib2.Request(url)
    if agent:
        page_request.add_header('User-agent', agent)
    page_response = urllib2.urlopen(page_request)
    if 200 != page_response.code:
        return get_favicon(url, agent)
    page_soup = soup(page_response)
    try:
        icon_url = page_soup.find(name='link', attrs={'rel': 'icon'})['href']
    except (TypeError, KeyError):
        return get_favicon(url, agent)
    # The url may be absolute or relative.
    if not urlparse.urlsplit(icon_url).netloc:
        icon_url = urlparse.urljoin(
            url, urllib.quote(icon_url.encode('utf-8')))
    print icon_url
    icon_request = urllib2.Request(icon_url)
    if agent:
        icon_request.add_header('User-agent', agent)
    icon_response = urllib2.urlopen(icon_request)
    if 200 != icon_response.code:
        raise ValueError(str(icon_response.code) + ': ' + icon_response.msg)
    icon_image = QImage.fromData(icon_response.read())
    return QPixmap.fromImage(icon_image.scaledToHeight(
            icon_size, Qt.SmoothTransformation))


def get_favicon(url, agent=None):
    ico_url = urlparse.urljoin(url, "/favicon.ico")
    ico_request = urllib2.Request(ico_url)
    if agent:
        ico_request.add_header('User-agent', agent)
    ico_response = urllib2.urlopen(ico_request)
    if 200 != ico_response.code:
        raise ValueError(str(ico_response.code) + ': ' + ico_response.msg)
    ico_image = QImage.fromData(ico_response.read())
    return QPixmap.fromImage(ico_image.scaledToHeight(
            icon_size, Qt.SmoothTransformation))
