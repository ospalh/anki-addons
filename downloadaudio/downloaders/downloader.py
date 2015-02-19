# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
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


def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes


class AudioDownloader(object):
    """
    Class to download a files from a dictionary or TTS service.

    This is the base class for the downloaders of spoken
    pronunciations.

    The derived classes must implement self.download_files()
    """
    def __init__(self):
        self.language = ''
        # The language used.
        # This is used as a public variable and set for every download.
        self.downloads_list = []
        # Store for downloaded data.
        # This is where self.download_files should store the results
        # (type DownloadEntry).
        self.url = ''
        # The base URL used for (the first step of) the download.
        self.icon_url = ''
        # URL to get the address of the site icon from.
        self.max_icon_size = 20
        # Max size we scale the site icon down to, if larger.
        self.user_agent = 'Mozilla/5.0'
        # User agent string that can be used for requests.
        # At least Google TTS won’t give out their translations unless
        # we pretend to be some typical browser.
        self.use_temp_files = False
        # Whether to use files created by tempfiles or not.
        # Where to write the downloaded files, in /tmp/ or into the Anki
        # media directory directly.
        # This is set to True by the “real” audio processor that does
        # normalization but doesn’t work for standard installs. On
        # typical installs this is kept False.)
        self.download_directory = None
        # Where to write the downloaded files.
        # If this is None or empty (i.e. “if not
        # self.download_directory”)  (and self.use_temp_files ==
        # False) we use the current directory.
        self.site_icon = None
        # The sites’s favicon.
        self.file_extension = u'.mp3'
        # Most sites have mp3 files.

    def download_files(self, field_data):
        """Downloader functon

        This is the main worker function. It has to be reimplemented
        by the derived classes.

        The input is the text to use for the download, the whole text
        (for most languages) and the text split into base (kanji) and
        ruby (reading, kana). split is set to true when we got the
        text from a reading field and should use base and ruby rather
        than word.

        This function should clear the self.downloads_list and try to
        get pronunciation files from its source, put those into tempfiles,
        and add a DownloadEntry object to self_downloads_lists for each of
        the zero or more downloaded files. (Zero when the
        self.language is wrong, there is no file &c.)

        """
        raise NotImplementedError("Use a class derived from this.")

    def maybe_get_icon(self):
        u"""
        Get icon for the site as a QImage if we haven’t already.

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
        u"""
        Get favicon for the site.

        This is called when the site_url can’t be loaded or when that
        page doesn’t contain a link tag with rel set to icon (the new
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
        try:
            # There have been reports that the request was send in a
            # 32-bit encoding (UTF-32?). Avoid that. (The whole things
            # is a bit curious, but there shouldn’t really be any harm
            # in this.)
            request = urllib2.Request(url_in.encode('ascii'))
        except UnicodeDecodeError:
            request = urllib2.Request(url_in)
        try:
            # dto. But i guess this is even less necessary.
            request.add_header('User-agent', self.user_agent.encode('ascii'))
        except UnicodeDecodeError:
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

    def get_tempfile_from_url(self, url_in):
        """
        Download raw data from url and put into a tempfile

        Wrapper helper function aronud self.get_data_from_url().
        """
        data = self.get_data_from_url(url_in)
        # We put the data into RAM first so that we don’t have to
        # clean up the temp file when the get does not work. (Bad
        # get_data raises all kinds of exceptions that fly through
        # here.)
        tfile = tempfile.NamedTemporaryFile(
            delete=False, prefix=u'anki_audio_', suffix=self.file_extension)
        tfile.write(data)
        tfile.close()
        return tfile.name
