# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download text from tatoeba.org.
"""

import urllib
import re

from .downloader import AudioDownloader

def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes


class TatoebaDownloader(object):
    """Download text from Tatoeba"""
    def __init__(self):
        self.language = ''
        """
        The language used.

        This is used as a public variable and set for every download.
        """
        self.downloads_list = []
        """
        Store for downloaded data.

        This is where self.download_files should store the
        results. See that method's docstring.
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
        self.site_icon = None
        """The sites's favicon."""
        self.url = 'http://www.merriam-webster.com/dictionary/'
        # Here the word page url works to get the favicon.
        self.icon_url = self.url
        self.popup_url = 'http://www.merriam-webster.com/audio.php?'

    def download_files(self, word, base, ruby, split):
        ur"""
        Get pronunciations of a word from Meriam-Webster

        Look up a English word at merriam-webster.com, look for
        pronunciations in the page and get audio files for those.

        There may be more than one pronunciation (eg row: \ˈrō\ and
        \ˈrau̇\), so return a list.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        if not self.language.lower().startswith('en'):
            return
        if not word:
            return
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(word.encode('utf-8')))
        # The audio clips are stored as input tags with class au
        word_input_aus = word_soup.findAll(name='input', attrs={'class': 'au'})
        # The interesting bit it the onclick attribute and looks like
        # "return au('moore01v', 'Moore\'s law')" Isolate those. Make
        # it readable. We do the whole processing EAFP style. When MW
        # changes the format, the processing will raise an exception
        # that we will catch in download.py.
        file_list = []
        meaning_no_list = []
        for input_tag in word_input_aus:
            onclick_string = input_tag['onclick']
            # Now cut off the bits on the left and right that should be
            # there. If not, this will fail. (Most likely the split.)
            # (The idea for this downloader came from the "English helper"
            # (for Chinese people) Anki 1 plugin. That plugin used res for
            # this processing, but those fail with words that contain an
            # apostrophe.)
            onclick_string = onclick_string.lstrip('return au(').rstrip(');')
            mw_audio_fn_base, mw_audio_word = onclick_string.split(', ')
            mw_audio_fn_base = mw_audio_fn_base.lstrip("'").rstrip("'")
            mw_audio_word = mw_audio_word.lstrip("'").rstrip("'")
            mw_audio_word = mw_audio_word.replace("\\", "")
            # There may be a meaning number, as in "1row" "3row" in the
            # title..
            match = re.search(
                "Listen to the pronunciation of ([0-9]+)" + re.escape(word),
                input_tag['title'])
            try:
                meaning_no = match.group(1)
            except AttributeError:
                meaning_no = None
                #  The same file may appear more than once, but with different
                #  meaning_nos.
            try:
                other_index = file_list.index(mw_audio_fn_base)
            except ValueError:
                # This is the normal case: First time we see this file.
                # But only add this if it is actually what we have been
                # looking for. For example if you ask mw for rower, you
                # get the "row" page, which has pronunciations for "row",
                # "rower" and the other "row".
                if mw_audio_word == word:
                    file_list.append(mw_audio_fn_base)
                    meaning_no_list.append(meaning_no)
            else:
                # We already have this word, at index other_index in the
                # two lists. That meaning_no is None or a string. The
                # same for this meaning_no.
                meaning_no_list[other_index] = join_strings(
                    meaning_no_list[other_index], meaning_no)
        if file_list:
            # Only get the icon when we (seem to) have a pronunciation
            self.maybe_get_icon()
        for idx, mw_fn in enumerate(file_list):
            meaning_no = meaning_no_list[idx]
            extras = dict(Source="Merriam-Webster")
            if meaning_no:
                extras['Meaning #'] = meaning_no
            try:
                word_path, word_file = self.get_word_file(mw_fn, word)
            except ValueError:
                continue
            self.downloads_list.append((word_path, word_file, extras))

    def get_word_file(self, base_name, word):
        """
        Get an audio file from MW.

        Load what would be shown as the MW play audio browser pop-up,
        isolate the "Use your default player" link from that, get the
        file that points to and get that.
        """
        popup_soup = self.get_soup_from_url(
            self.get_popup_url(base_name, word))
        # The audio clip is the only embed tag.
        popup_embed = popup_soup.find(name='embed')
        word_data = self.get_data_from_url(popup_embed['src'])
        word_path, word_fname = self.get_file_name()
        with open(word_path, 'wb') as word_file:
            word_file.write(word_data)
        return word_path, word_fname

    def get_popup_url(self, base_name, source):
        """Build url for the MW play audio pop-up."""
        qdict = dict(file=base_name, word=source)
        return self.popup_url + urllib.urlencode(qdict)


    def set_names(self, text, dummy_base, dummy_ruby):
        """
        Set the display text and file base name variables.

        Set self.display_text and self.base_name with the text used
        for download, formated in a form useful for display and for a
        file name, respectively.
        This version uses just the text. It should be reimplemented
        for Japanese (Chinese, ...)  downloaders that use the base and
        ruby.
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
        try:
            # There have been reports that the request was send in a
            # 32-bit encoding (UTF-32?). Avoid that. (The whole things
            # is a bit curious, but there shouldn't really be any harm
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
