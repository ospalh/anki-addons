# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html



'''
Download Japanese pronunciations from Japanesepod
'''


import urllib
import urllib2
import os

from aqt import mw

from process_audio import process_audio
from blacklist import get_hash
from exists import free_media_name


download_file_extension = u'.mp3'

# Set the default language for tts.
default_language = 'en'

url_gtts = 'http://translate.google.com/translate_tts?'

user_agent_string = 'Mozilla/5.0'

opener = urllib.FancyURLopener({})
opener.version = user_agent_string

# Code

def get_word_from_google(source, language=None):
    if not source:
        raise ValueError('Nothing to download')
    base_name = free_media_name(source, download_file_extension)
    get_url = build_query_url(source, language=None)
    # This may throw an exception
    file_name, retrieve_header = opener.retrieve(
        get_url, os.path.join(mw.col.media.dir(), base_name))
    try:
        file_hash = get_hash(file_name)
    except ValueError:
        os.remove(file_name)
        # Simpler to just raise again
        raise
    # for testing
    # try:
    file_name = process_audio(file_name)
    # except:
    #    pass
    return os.path.basename(file_name), file_hash


def build_query_url(source, language=None):
        qdict = {}
        if not language:
            language = default_language
        qdict['tl'] = language.encode('utf-8')
        qdict['q'] = source.encode('utf-8')
        return url_gtts + urllib.urlencode(qdict)
