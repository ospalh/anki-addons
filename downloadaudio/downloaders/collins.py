# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2014–15 Roland Sieker <ospalh@gmail.com>
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Collins dictionary

Abstract base class, derived for several languages.
"""

import urllib

from .downloader import AudioDownloader, uniqify_list
from ..download_entry import Action, DownloadEntry
import aqt.utils


class CollinsDownloader(AudioDownloader):
    """Download audio from Collins"""
    def __init__(self):
        AudioDownloader.__init__(self)
        # self.url = 'http://www.collinsdictionary.com/dictionary/NN-english/'
        # The url is set in the derived French or Spanish classes.
        self.url = None
        self.base_url = u'http://www.collinsdictionary.com'
        self.lang = None  # e.g. u'fr'
        self.lang_code = None  # e.g. u'/fr_/'
        # self.icon_url = self.url
        # self.extras = dict(Source="Collins German")
        # Here the word page url works to get the favicon.
        self.action = Action.Add

    def download_files(self, field_data):
        u"""
        Get pronunciations of a word from a Collins dictionary.

        Look up a word at collins.com. There are a few derived classes
        for English, French, Spanish, German and Italian.
        """
        self.downloads_list = []
        if field_data.split:
            # Avoid double downloads
            return
        if not self.language.lower().startswith(self.lang):
            return
        if not field_data.word:
            return
        lword = field_data.word.lower()
        # Do our parsing with BeautifulSoup
        word_soup = self.get_soup_from_url(
            self.url + urllib.quote(lword.encode('utf-8')))
        html_tag_with_audio_url = word_soup.find(
            name='a', attrs={'class': 'hwd_sound sound audio_play_button'})
        if not html_tag_with_audio_url:
            return
        audio_url = self.base_url + html_tag_with_audio_url['data-src-mp3']
        self.maybe_get_icon()
        word_path = self.get_tempfile_from_url(audio_url)
        entry = DownloadEntry(
            field_data, word_path, self.extras, self.site_icon)
        entry.action = self.action
        self.downloads_list.append(entry)
