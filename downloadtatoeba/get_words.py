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

user_agent = '''Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) \
Gecko/20100101 Firefox/15.0.1'''

def uniqify_list(seq):
    """Return a copy of the list with every element appearing only once."""
    # From http://www.peterbe.com/plog/uniqifiers-benchmark
    no_dupes = []
    [no_dupes.append(i) for i in seq if not no_dupes.count(i)]
    return no_dupes



def download_files(word, note, foreign_lang, local_langs):
    ur"""
    Download one sentence from Tatoeba.org

    ...
    """
    self.downloads_list = []
    if not word:
        return
    # Do our parsing with BeautifulSoup
    page, limit = get_page_limit(note.tags)
    url = build_url(page, limit, foreign_lang, local_langs)
    word_soup = get_soup_from_url(url)
    word_input_aus = word_soup.findAll(name='input', attrs={'class': 'au'})
    meaning_no_list = []
    for input_tag in word_input_aus:
            onclick_string = input_tag['onclick']
            onclick_string = onclick_string.lstrip('return au(').rstrip(');')
            match = re.search(
                "Listen to the pronunciation of ([0-9]+)" + re.escape(word),
                input_tag['title'])
            try:
                meaning_no = match.group(1)
            except AttributeError:
                meaning_no = None
                #  The same file may appear more than once, but with different
                #  meaning_nos.
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


def get_data_from_url(url_in):
    """
    Return raw data loaded from an URL.

    Helper function. Put in an URL and it sets the agent, sends
    the requests, checks that we got error code 200 and returns
    the raw data only when everything is OK.
    """
    try:
        # There have been reports that the request was send in a
        # 32-bit encoding (UTF-32?). Avoid that. (The whole things is
        # a bit curious, but there shouldn't really be any harm in
        # this.)
        request = urllib2.Request(url_in.encode('ascii'))
    except UnicodeDecodeError:
        request = urllib2.Request(url_in)
    try:
        # dto. But i guess this is even less necessary.
        request.add_header('User-agent', user_agent.encode('ascii'))
    except UnicodeDecodeError:
        request.add_header('User-agent', self.user_agent)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    return response.read()
