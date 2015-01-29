# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2015 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""
Download pronunciations from Forvo.
"""

import urllib

try:
    import simplejson as json
except ImportError:
    import json

from ..download_entry import DownloadEntry
from .downloader import AudioDownloader


class ForvoDownloader(AudioDownloader):
    """Download audio from Forvo"""
    def __init__(self):
        AudioDownloader.__init__(self)
        # Keep these two in sync
        self.file_extension = u'.ogg'
        self.path_code = 'pathogg'
        # Keep this secret:
        self.url = 'http://apifree.forvo.com/action/word-pronunciations/' \
            'format/json/order/rate-desc/limit/3/' \
            'key/XXXXXXXXXX/word/'
        self.icon_url = 'http://www.forvo.com/'
        self.gender_dict = {'f': u'♀', 'm': u'♂'}

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from Forvo
        """
        self.downloads_list = []
        if split:
            # Here, too, just avoid double downloads.
            return
        if not word:
            return
        self.maybe_get_icon()
        get_url = self.build_query_url(word)
        # Caveat! The old code used json.load(response) with a
        # file-like object.  now we ues json.loads(get_data()) with a
        # string. Don't confuse load() with loads()!
        reply_dict = json.loads(self.get_data_from_url(get_url))
        self.get_items(reply_dict['items'], word)

    def get_items(self, items_list, word):
        for itm in items_list:
            extras = dict(Source='Forvo.com')
            try:
                user_str = itm['username']
            except KeyError:
                pass
            else:
                try:
                    user_str += u' ({0})'.format(self.gender_dict[itm['sex']])
                except KeyError:
                    pass
                extras['User'] = user_str
            try:
                extras['Language'] = itm['langname']
            except KeyError:
                pass
            try:
                extras['Rating'] = itm['rate']
            except KeyError:
                pass
            word_path, word_fname = self.get_file_name(
                word, self.file_extension)
            try:
                with open(word_path, 'wb') as word_file:
                    word_file.write(
                        self.get_data_from_url(itm[self.path_code]))
            except (ValueError, KeyError):
                continue
            dl_entry = DownloadEntry(
                word_path, word_fname, base_name=word, display_text=word,
                file_extension=self.file_extension, extras=extras)
            self.downloads_list.append(dl_entry)
        # No clean-up

    def build_query_url(self, word):
        builded_url = self.url + urllib.quote(word.encode('utf-8'))
        if self.language:
            builded_url += '/language/' + self.language
        return builded_url + '/'
