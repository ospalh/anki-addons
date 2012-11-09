# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from Merriam-Webster.
'''

import tempfile
import urllib
import urllib2
import os
import re

from BeautifulSoup import BeautifulSoup as soup

from .process_audio import process_audio, unmunge_to_mediafile
from .blacklist import get_hash
from .uniqify import uniqify_list

download_file_extension = u'.wav'

url_mw_word = 'http://www.merriam-webster.com/dictionary/'
"""URL to get the word definition page."""
url_mw_popup = 'http://www.merriam-webster.com/audio.php?'
"""URL for the play audio pop-up"""

user_agent_string = 'Mozilla/5.0'


def get_words_from_mw(source):
    """
    Get pronunciations of a word from Merriam-Webster.

    Look up an English word at merriam-webster.com, look for
    pronunciations in the page and get audio files for those.

    There may be more than one pronunciation (eg row: \ˈrō\ and
    \ˈrau̇\), so return a list.
    """
    if not source:
        raise ValueError('Nothing to download')
    # The download has to be done in steps:
    # First, get the page for the definitions
    word_page_url = url_mw_word + urllib.quote(source.encode('utf-8'))
    # This may throw an exception
    word_request = urllib2.Request(word_page_url)
    # Not sure if this is needed
    word_request.add_header('User-agent', user_agent_string)
    word_response = urllib2.urlopen(word_request)
    if 200 != word_response.code:
        raise ValueError(str(word_response.code) + ': ' + word_response.msg)
    # Do our parsing with BeautifulSoup
    word_soup = soup(word_response)
    # The audio clips are stored as input tags with class au
    word_input_aus = word_soup.findAll(name='input', attrs={'class': 'au'})
    # The interesting bit it the onclick attribute and looks like
    # "return au('moore01v', 'Moore\'s law')" Isolate those. Make it
    # readable. We do the whole processing EAFP style. When MW changes
    # the format, the processing will raise an exception that we will
    # catch in download.py.
    file_word_list = []
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
        # There may be a meaning number, as in "1row" "3row" in the
        # title..
        match = re.search(
            "Listen to the pronunciation of ([0-9]+)" + re.escape(source),
            input_tag['title'])
        try:
            meaning_no = match.group(1)
        except AttributeError:
            meaning_no = None
        file_word_list.append((mw_audio_fn_base, mw_audio_word, meaning_no))
    #  The same file may appear more than once.
    file_word_list = uniqify_list(file_word_list)
    # Now eliminate words that are not what we asked for. For example
    # if you ask mw for rower, you get the "row" page, which has
    # pronunciations for "row", "rower" and the other "row".
    file_word_list = [fw_pair for fw_pair in file_word_list
                      if fw_pair[1] == source]
    words_tuple_list = []
    for mw_fn, mw_src, meaning_no in file_word_list:
        extras = dict(source='Merriam-Webster')
        if meaning_no:
            extras['Meaning #'] = meaning_no
        try:
            word_file, word_hash = get_word_hash_pair(mw_fn, source)
        except ValueError:
            continue
        words_tuple_list.append((word_file, word_hash, extras))
    return words_tuple_list


def get_word_hash_pair(base_name, source):
    """
    Get an audio file from MW, check the hash and return it.

    Load what would be shown as the MW play audio browser pop-up,
    isolate the "Use your default player" link from that, get the file
    that points to and get that. Than do the hash checking and
    processing.
    """
    popup_url = get_popup_url(base_name, source)
    popup_request = urllib2.Request(popup_url)
    # Not sure if this is needed
    popup_request.add_header('User-agent', user_agent_string)
    popup_response = urllib2.urlopen(popup_request)
    if 200 != popup_response.code:
        raise ValueError(str(popup_response.code) + ': ' + popup_response.msg)
    popup_soup = soup(popup_response)
    # The audio clip is the only embed tag.
    popup_embed = popup_soup.find(name='embed')
    audio_url = popup_embed['src']
    audio_request = urllib2.Request(audio_url)
    # Not sure if this is needed
    audio_request.add_header('User-agent', user_agent_string)
    audio_response = urllib2.urlopen(audio_request)
    if 200 != audio_response.code:
        raise ValueError(str(audio_response.code) + ': ' + audio_response.msg)
    temp_file = tempfile.NamedTemporaryFile(
        delete=False, suffix=download_file_extension)
    temp_file.write(audio_response.read())
    temp_file.close()
    try:
        file_hash = get_hash(temp_file.name)
    except ValueError:
        os.remove(temp_file.name)
        raise
    try:
        return process_audio(temp_file.name, source, download_file_extension,
                             silence_percent=0.2, silence_end_percent=0.5),\
               file_hash
    except:
        return unmunge_to_mediafile(temp_file.name, source,
                                    download_file_extension),\
               file_hash


def get_popup_url(base_name, source):
    """Build url for the MW play audio pop-up."""
    qdict = dict(file=base_name, word=source)
    return url_mw_popup + urllib.urlencode(qdict)
