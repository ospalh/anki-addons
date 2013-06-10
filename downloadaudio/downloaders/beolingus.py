# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from BeoLingus.
'''

import urllib
import urlparse
import re

# url_bl_word = 'dict.tu-chemnitz.de/dings.cgi?service=de-en&query=unwahr'

download_file_extension = u'.wav'


from .downloader import AudioDownloader, uniqify_list


class BeolingusDownloader(AudioDownloader):
    """Download audio from Beolingus"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.mp3'
        self.icon_url = 'http://dict.tu-chemnitz.de/'
        self.url = 'http://dict.tu-chemnitz.de/dings.cgi?'
        self.site_url = 'http://dict.tu-chemnitz.de/'
        # Seen this encoding in their page. Oh, my.
        self.site_encoding = 'ISO-8859-1'
        self.speak_code = 'dings.cgi?speak='
        # I have seen "text=sink%20{verb}" and the like. The simple text
        # match wasn't good enough.
        # self.text_code = 'text='
        self.text_re = u'text={0}(?:%20{{([a-zA-Z ]+)}})?$'
        self.services_dict = {'de': 'de-en', 'en': 'en-de', 'es': 'es-de'}
        """
        Mapping of languages to "services".

        We can get pronunciations for the three keys in this dictionary.
        """
        self.service = None

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from BeoLingus

        Get pronunciations for words in one of three languages.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads
            return
        self.set_names(word, base, ruby)
        # EAFP. When we call this with a wrong language we fly right
        # out of this with a KeyError.
        self.service = self.services_dict[self.language[:2].lower()]
        if not word:
            return
        word_soup = self.get_soup_from_url(self.build_word_url(word))
        href_list = [a['href'] for a in word_soup.findAll('a')]
        href_list = uniqify_list(href_list)
        href_list = [href for href in href_list
                     if (self.speak_code + self.language) in href]
        # Unroll this step, so the adding of the extra element becomes
        # more readable.
        speak_list = []
        for href in href_list:
            re_found = re.search(self.text_re.format(re.escape(word)), href)
            if re_found:
                # NB: the group(1) may be None.
                speak_list.append((href, re_found.group(1)))
        if speak_list:
            # Only get the icon when we (seem to) have a pronunciation
            self.maybe_get_icon()
        for url_to_get, part_of_speech in speak_list:
            # We may have some extra info: the bit in the {}s.
            extras = dict(Source="Beolingus")
            if part_of_speech:
                # As said above, the bit in the curly braces may not be there.
                extras['Part of speech'] = part_of_speech
            try:
                word_path, word_fname = self.get_word_file(url_to_get, word)
            except ValueError:
                continue
            self.downloads_list.append((word_path, word_fname, extras))

    def get_word_file(self, popup_url, word):
        """
        Get an audio file from Beolingus

        Load what would be shown as the Beolingus play audio browser
        pop-up, isolate the "Listen with your default mp3 player" link
        from that, get the file that points to and get that.
        """
        word = urllib.quote(word.encode('utf-8'))
        popup_url = re.sub(';text=.*$', ';text=' + word, popup_url)
        popup_url = urlparse.urljoin(self.site_url, popup_url)
        popup_soup = self.get_soup_from_url(popup_url)
        # The audio link should be the only link.
        href_list = [a['href'] for a in popup_soup.findAll('a')]
        href_list = [href for href in href_list if "speak" in href]
        href_list = [href for href in href_list
                     if href.endswith(self.file_extension)]
        # If we don't have exactly one url, something's wrong. Assume
        # we have at least one.
        word_url = href_list[0]
        word_url = urlparse.urljoin(self.site_url, word_url)
        word_data = self.get_data_from_url(word_url)
        word_path, word_fname = self.get_file_name()
        with open(word_path, 'wb') as word_file:
            word_file.write(word_data)
        return word_path, word_fname

    def build_word_url(self, source):
        u"""Put source into a dict useful as part of a url."""
        qdict = dict(service=self.service, query=source.encode('utf-8'))
        return self.url + urllib.urlencode(qdict)
