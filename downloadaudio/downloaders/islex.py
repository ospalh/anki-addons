# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2015 Daniel Eriksson <daniel@deriksson.se>
# Copyright © 2015 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations for Icelandic from islex.is
"""

import urllib

from .downloader import AudioDownloader
from ..download_entry import DownloadEntry


class IslexDownloader(AudioDownloader):
    """Download audio from Islex"""

    def __init__(self):
        AudioDownloader.__init__(self)
        self.url = 'http://islex.is/'
        self.icon_url = 'http://islex.is/'
        self.file_extension = u'.mp3'

    def download_files(self, field_data):
        self.downloads_list = []
        if not self.language.lower().startswith('is'):
            return
        if field_data.split:
            return
        if not field_data.word:
            return
        # These flags were used by an advanced search on Islex. They
        # work, but not all of them may be needed.
        qdict = {'finna': 1, 'dict': 'SE', 'erflokin': 1, 'nlo': 1, 'fuzz': 1,
                 'samleit': field_data.word.encode('utf-8')}
        soup = self.get_soup_from_url(self.url + 'se?' + urllib.urlencode(qdict))
        href_list = []
        if soup.findAll(attrs=dict(id='ord')):
            # When we have a table tag with id="ord" we (probably)
            # have just one word. Use that.
            word = {'url': self.url + soup.find('audio').find(
                           'source', type="audio/mp3")['src']}
            # Get the spelling and gender, these are not essential
            # so if something goes wrong, just let it pass.
            try:
                word['spelling'] = soup.find('table', id='flettuhaus').find(
                                   'span', {'class': 'fletta'}).getText()
                # This will raise exception for non-nouns
                word['gender'] = soup.find('table', id='flettuhaus').find(
                                 'span', {'class': 'ofl'}).getText()
            except:
                pass
            href_list.append(word)

        else:
            # More than one word. Or 0 words.
            links = soup.find(
                attrs={'class': 'leitres'}).find('ul').findAll('a')
            # When we have 0 words this raises some exception. Which is fine.
            for a in links:
                try:
                    word_soup = self.get_soup_from_url(self.url + a['href'])
                except (AttributeError, KeyError):  # What else could go wrong?
                    continue

                word = {'url': self.url + word_soup.find('audio').find(
                               'source', type="audio/mp3")['src']}
                # Get the spelling and gender, these are not essential
                # so if something goes wrong, just let it pass.
                try:
                    word['spelling'] = word_soup.find('table', id='flettuhaus').find(
                                       'span', {'class': 'fletta'}).getText()
                    # This will raise exception for non-nouns
                    word['gender'] = word_soup.find('table', id='flettuhaus').find(
                                     'span', {'class': 'ofl'}).getText()
                except:
                    pass
                href_list.append(word)
        if href_list:
            self.maybe_get_icon()
        for word in href_list:
            extras = {'Source': 'Islex'}
            if 'gender' in word:
                extras['gender'] = word['gender']
            entry = DownloadEntry(
                field_data, self.get_tempfile_from_url(word['url']),
                extras, self.site_icon)
            if 'spelling' in word:
                entry.word = word['spelling']
            self.downloads_list.append(entry)
