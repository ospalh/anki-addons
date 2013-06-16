# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from Wiktionary.
'''

import urllib
import urlparse
import re

from .downloader import AudioDownloader, uniqify_list

# Make this work without PyQt
with_pyqt = True
try:
    from PyQt4.QtGui import QImage
    from PyQt4.QtCore import QSize, Qt
except ImportError:
    with_pyqt = False


class WiktionaryDownloader(AudioDownloader):
    """Download audio from Wiktionary"""
    def __init__(self):
        AudioDownloader.__init__(self)
        self.file_extension = u'.ogg'
        self.icon_url = 'http://de.wiktionary.org/'
        self.full_icon_url = 'http://bits.wikimedia.org/favicon/piece.ico'
        self.url = 'http://{0}.wiktionary.org/wiki/{1}'
        # This re should find only the 'real' files, not the file
        # description pages. Mediawiki builds 256 (0x100) sub-folders
        # in the style <hex_digit_1>/<hex_digit_1><hex_digit_2>. Look
        # for that pattern.
        self.word_ogg_re = \
            ur'/([a-f0-9])/\1[a-f0-9]/[^/]*\b{word}\b[^/]*\.ogg$'
        # This seems to work to extract the url from a <button> tag's
        # onclick attribute.
        self.button_onclick_re = '"videoUrl":"([^"]+)"'

    def download_files(self, word, base, ruby, split):
        """
        Get pronunciations of a word from the right wiktionary.
        """
        self.downloads_list = []
        if split:
            # Avoid double downloads.
            return
        self.set_names(word, base, ruby)
        if not word:
            return
        u_word = urllib.quote(word.encode('utf-8'))
        self.maybe_get_icon()
        self.language = self.language[:2]
        word_soup = self.get_soup_from_url(
            self.url.format(self.language, u_word))
        # There are a number of ways the audio files can be present:
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
            if re.search(self.word_ogg_re.format(word=re.escape(u_word)), href,
                         flags=re.IGNORECASE):
                ogg_url_list.append(href)
        # Next, look for source and src. Seen those inside audio tags.
        # I'm not sure if this is any use, but i guess it does no harm.
        source_list = word_soup.findAll('source')
        for source in source_list:
            try:
                # Take the same precaution as above
                src = source['src']
            except KeyError:
                continue
            # We might have other source tags, for whatever. Use the
            # same re as above. Should work out fine.
            if re.search(self.word_ogg_re.format(word=re.escape(u_word)), src,
                         flags=re.IGNORECASE):
                ogg_url_list.append(src)
        # At least from fr.wiktionary.org i got a <button>.
        button_list = word_soup.findAll('button')
        for button in button_list:
            try:
                video_url = re.search(
                    self.button_onclick_re, button['onclick']).group(1)
            except (KeyError, AttributeError):
                continue
            if re.search(self.word_ogg_re.format(word=re.escape(u_word)),
                         video_url, flags=re.IGNORECASE):
                ogg_url_list.append(video_url)
        ogg_url_list = uniqify_list(ogg_url_list)
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

    def maybe_get_icon(self):
        if self.site_icon:
            return
        if not with_pyqt:
            self.site_icon = None
            return
        try:
            icon_data = self.get_data_from_url(self.full_icon_url)
        except:
            AudioDownloader.maybe_get_icon(self)
        else:
            self.site_icon = QImage.fromData(icon_data)
            max_size = QSize(self.max_icon_size, self.max_icon_size)
            ico_size = self.site_icon.size()
            if ico_size.width() > max_size.width() \
                    or ico_size.height() > max_size.height():
                self.site_icon = self.site_icon.scaled(
                    max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
