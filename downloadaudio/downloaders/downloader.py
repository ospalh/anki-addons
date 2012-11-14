# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Class to download a files from a speaking dictionary or TTS service.
'''

import urllib
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup as soup

# Make this work without PyQt
with_pyqt = True
try:
    from PyQt4.QtGui import QImage
    from PyQt4.QtCore import QSize, Qt
except ImportError:
    with_pyqt = False


class AudioDownloader(object):
    """
    Class to download a files from a dictionary or TTS service.

    This is the base class for the downloaders of spoken
    pronunciations.

    The derived classes must implement self.download_files()
    """
    def __init__(self):
        self.language = ''
        """
        The language used.

        This is used as a public variable and set for every download.
        """
        self.downloads_list = []
        """
        Store for downloaded data.

        This is where self.download_files should
        """
        self.display_text = ''
        """Text shown as source after download"""
        self.base_name = ''
        """Base of the final file name."""
        self.file_extension = u'.wav'
        # A typical downloaders will need something like this.
        self.url = ''
        """The base URL used for (the first step of) the download."""
        self.icon_url = ''
        """URL to get the address of the site icon from."""
        self.max_icon_size = 20
        """Max size we scale the site icon down to, if larger."""
        self.user_agent = 'Mozilla/5.0'
        """
        User agent string that can be used for requests.

        At least Google TTS won't give out their translations unless
        we pretend to be some typical browser.
        """
        self.site_icon = None
        """The sites's favicon."""

    def download_files(self, word, base, ruby):
        """
        Downloader functon.

        This is the main worker function. It has to be reimplemented
        by the derived classes.

        The input is the text to use for the download, either the
        whole text (for most languages) or split into kanji and kana
        for Japanese. (The same split could be used for a Chinese
        downloader, split into hanzi and pinyin (or bopomofo, ...).)

        This function should clear the self.downloads_list, try to get
        pronunciation files from its source, put those into tempfiles,
        and add a (temp_file_name, extras) pair to
        self_downloads_lists for each downloaded file (which may of
        course be zero, e.g. when the self.language is wrong). extras
        should be a dict with interesting informations, like meaning
        numbers, name of speaker &c. It should also call
        self.set_names().
        """
        # NB. Checking file hashes and audio processing is now
        # done by the calling function.
        raise NotImplementedError("Use a class derived from this.")

    def set_names(self, text, base, ruby):
        """
        Set the display text and file base name variables.

        Set self.display_text and self.base_name with the text used
        for download, formated in a form useful for display and for a
        file name, respectively.
        This version uses just the text. It
        should be reimplemented for Japanese (Chinese, ...)
        downloaders that use the base and ruby.
        """
        self.base_name = text
        self.display_text = text

    def get_icon(self):
        """
        Get icon for the site as a QPixmap.

        Get the site icon, either the 'rel="icon"' or the favicon, for
        the web page at url or passed in as page_html. Return a PyQt4
        QPixmap.
        """
        if not with_pyqt:
            self.site_icon = None
            return
        page_request = urllib2.Request(self.icon_url)
        if self.user_agent:
            page_request.add_header('User-agent', self.user_agent)
        page_response = urllib2.urlopen(page_request)
        if 200 != page_response.code:
            self.get_favicon()
            return
        page_soup = soup(page_response)
        try:
            icon_url = page_soup.find(
                name='link', attrs={'rel': 'icon'})['href']
        except (TypeError, KeyError):
            self.get_favicon()
            return
        # The url may be absolute or relative.
        if not urlparse.urlsplit(icon_url).netloc:
            icon_url = urlparse.urljoin(
                self.url, urllib.quote(icon_url.encode('utf-8')))
        icon_request = urllib2.Request(icon_url)
        if self.user_agent:
            icon_request.add_header('User-agent', self.user_agent)
        icon_response = urllib2.urlopen(icon_request)
        if 200 != icon_response.code:
            self.site_icon = None
            return
        self.site_icon = QImage.fromData(icon_response.read())
        max_size = QSize(self.max_icon_size, self.max_icon_size)
        icon_size = self.site_icon.size()
        if icon_size.width() > max_size.width() \
                or icon_size.height() > max_size.height():
            self.site_icon = self.site_icon.scaled(
                max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def get_favicon(self):
        """
        Get favicon for the site.

        This is called when the site_url can't be loaded or when that
        page doesn't contain a link tag with rel set to icon (the new
        way of doing site icons.)
        """
        if not with_pyqt:
            self.site_icon = None
            return
        ico_url = urlparse.urljoin(self.icon_url, "/favicon.ico")
        ico_request = urllib2.Request(ico_url)
        if self.user_agent:
            ico_request.add_header('User-agent', self.user_agent)
        ico_response = urllib2.urlopen(ico_request)
        if 200 != ico_response.code:
            self.site_icon = None
            return
        self.site_icon = QImage.fromData(ico_response.read())
        max_size = QSize(self.max_icon_size, self.max_icon_size)
        ico_size = self.site_icon.size()
        if ico_size.width() > max_size.width() \
                or ico_size.height() > max_size.height():
            self.site_icon = self.site_icon.scaled(
                max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def get_data_from_url(self, url_in):
        """
        Return raw data loaded from an URL.

        Helper function. Put in an URL and it sets the agent, sends
        the requests, checks that we got error code 200 and returns
        the raw data only when everything is OK.
        """
        request = urllib2.Request(url_in)
        request.add_header('User-agent', self.user_agent)
        response = urllib2.urlopen(request)
        if 200 != response.code:
            raise ValueError(str(response.code) + ': ' + response.msg)
        return response.read()

    def get_soup_from_url(self, url_in):
        """
        Return data loaded from an URL, as BeautifulSoup(3) object.

        Wrapper helper function aronud self.get_data_from_url()
        """
        return soup(self.get_data_from_url(url_in))
