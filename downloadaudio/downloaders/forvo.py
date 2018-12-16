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
        self.field_data = None

    def download_files(self, field_data):
        """
        Get pronunciations of a word from Forvo
        """
        self.downloads_list = []
        self.field_data = field_data
        if field_data.split:
            return
        if not field_data.word:
            return
        self.maybe_get_icon()
        # Caveat! The old code used json.load(response) with a
        # file-like object.  now we ues json.loads(get_data()) with a
        # string. Don't confuse load() with loads()!
        reply_dict = json.loads(self.get_data_from_url(self.query_url()))
        self.get_items(reply_dict['items'])

    def get_items(self, items_list):
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
            try:
                file_path = self.get_tempfile_from_url(itm[self.path_code])
                # I guess the try is not really necessary. Anyway.
            except (ValueError, KeyError):
                continue
            entry = DownloadEntry(
                self.field_data, file_path, extras, self.site_icon)
            entry.file_extension = self.file_extension
            self.downloads_list.append(entry)
        # No clean-up

    def query_url(self):
        builded_url = self.url + urllib.quote(
            self.field_data.word.encode('utf-8'))
        if self.language:
            builded_url += '/language/' + self.language
        return builded_url + '/'
