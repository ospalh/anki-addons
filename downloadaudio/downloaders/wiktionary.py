# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from Wiktionary.
'''

import urlparse
import re

from .downloader import AudioDownloader


class WiktionaryDownloader(AudioDownloader):
    """Download audio from Wiktionary"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.ogg'
        self.icon_url = 'http://de.wiktionary.org'
        self.url = 'http://{0}.wiktionary.org/wiki/{1}'
        self.site_url = 'http://dict.tu-chemnitz.de/'
        # This re should find only the 'real' files, not the file
        # description pages. Mediawiki builds 256 (0x100) sub-folders
        # in the style <hex_digit_1>/<hex_digit_1><hex_digit_2>. Look
        # for that pattern.
        self.word_ogg_re = r'/([a-f0-9])/\1[a-f0-9]/[^/]*\b{word}\b[^/]*\.ogg$'
        # This seems to work to extract the url from a <button> tag's
        # onclick attribute.
        self.button_onclick_re = '"videoUrl":"([^"]+)"'

    def download_files(self, word, base, ruby):
        """
        Get pronunciations of a word from the right wiktionary.
        """
        self.downloads_list = []
        self.set_names(word, base, ruby)
        if not word:
            return
        self.maybe_get_icon()
        self.language = self.language[:2]
        word_soup = self.get_soup_from_url(
            self.url.format(self.language, word))
        # There are (at least) two ways the audio files can be present:
        ogg_url_list = []
        # As simple links:
        a_list = word_soup.findAll('a')
        for a in a_list:
            try:
                # Caveat. I have seen an <a> without a href! (It was '<a
                # id="top"></a>', maybe they handle it with CSS.) So href_list
                # = [a['href'] for a in a_list] might not work.
                href = a['href']
            except KeyError:
                continue
            # We look for links to ogg files (and not the description
            # pages) that contain our word.
            if re.search(self.word_ogg_re.format(word=re.escape(word)), href):
                print 'good href: {}'.format(href)
                ogg_url_list.append(href)
        # Next, look for source and src. Seen those inside audio tags.
        # I'm not sure if this is any use, but i guess it does no harm.
        source_list = word_soup.findAll('source')
        print 'source list: {}'.format(source_list)
        for source in source_list:
            try:
                # Take the same precaution as above
                src = source['src']
            except KeyError:
                continue
            # We might have other source tags, for whatever. Use the
            # same re as above. Should work out fine.
            if re.search(self.word_ogg_re.format(word=re.escape(word)), src):
                print 'good src: {}'.format(src)
                ogg_url_list.append(src)

        # At least from fr.wiktionary.org i got <button>.
        button_list = word_soup.findAll('button')
        print 'button list: {}'.format(button_list)
        for button in button_list:
            try:
                # Take the same precaution as above
                video_url = re.search(
                    self.button_onclick_re, button['onclick']).group(1)
            except (KeyError, AttributeError):
                continue
            if re.search(self.word_ogg_re.format(
                    word=re.escape(word)), video_url):
                print 'good vurl: {}'.format(video_url)
                ogg_url_list.append(video_url)

        # When we have the audio tags, there probably are direct <a>
        # links to those files as well, so
        ogg_url_list = self.uniqify_list(ogg_url_list)
        for url_to_get in ogg_url_list:
            # We may have to add a scheme or a scheme and host
            # name (netloc). urlparse to the rescue!
            word_url = urlparse.urljoin(
                self.url.format(self.language, ''), url_to_get)
            try:
                word_data = self.get_data_from_url(word_url)
            except:
                continue
            word_path, word_fname = self.get_file_name()
            with open(word_path, 'wb') as word_file:
                word_file.write(word_data)
            self.downloads_list.append(
                (word_path, word_fname, dict(Source="Wiktionary")))
