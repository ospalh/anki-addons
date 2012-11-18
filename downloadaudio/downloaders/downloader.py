# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Class to download a files from a speaking dictionary or TTS service.
'''

import tempfile
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
        self.display_text = u''
        """Text shown as source after download"""
        self.base_name = u''
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
        self.use_temp_files = False
        """
        Whether to use files created by tempfiles or not.

        Where to write the downloaded files, in /tmp/ or into the Anki
        media directory directly. (This is
        """
        self.download_directory = None
        """
        Where to write the downloaded files.

        If this is None or empty
        (i.e. "if not self.download_directory:...")
        (and self.use_temp_files == False)
        we use the current directory.
        """

        self.site_icon = None
        """The sites's favicon."""

    def download_files(self, word, base, ruby, split):
        """
        Downloader functon.

        This is the main worker function. It has to be reimplemented
        by the derived classes.

        The input is the text to use for the download, either the
        whole text (for most languages) or split into kanji and kana,
        base and ruby.

        This function should clear the self.downloads_list, call
        self.set_names(), and try to get pronunciation files from its
        source, put those into tempfiles, and add a (temp_file_path,
        base_name, extras) pair to self_downloads_lists for each
        downloaded file (which may of course be zero, e.g. when the
        self.language is wrong). extras should be a dict with
        interesting informations, like meaning numbers, name of
        speaker &c.
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

    def maybe_get_icon(self):
        """
        Get icon for the site as a QImage if we haven't already.

        Get the site icon, either the 'rel="icon"' or the favicon, for
        the web page at url or passed in as page_html and store it as
        a QImage. This function can be called repeatedly and loads the
        icon only once.
        """
        if self.site_icon:
            return
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
        if self.site_icon:
            return
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

    def get_file_name(self):
        """
        Get a free file name.

        Determine where we should write the data and build a free name
        based on that. This looks at self.use_temp_files and
        self.download_diretory. Read their docstrings.
        """
        if self.use_temp_files:
            tfile = tempfile.NamedTemporaryFile(
                delete=False, suffix=self.file_extension)
            tfile.close()
            # Hack, free_media_name returns full path and file name,
            # so return two files here as well. But there is no real
            # need to split off the file name from the direcotry bit.
            return tfile.name, tfile.name
        else:
            # IAR, specifically PEP8. When we don't use temp files, we
            # should clean up the request string a bit, and that is
            # best done with Anki functions. So, when
            # self.use_temp_files is False, we need anki, bits of
            # which are imported by ..exists.
            from ..exists import free_media_name
            return free_media_name(
                self.base_name, self.file_extension)

    def uniqify_list(self, seq):
        """Return a copy of the list with every element appearing only once."""
        # From http://www.peterbe.com/plog/uniqifiers-benchmark
        no_dupes = []
        [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
        return no_dupes
