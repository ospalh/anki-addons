# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html



'''
Download Japanese pronunciations from Japanesepod
'''

import tempfile
import urllib
import urllib2
import os

from aqt import mw

from process_audio import process_audio
from blacklist import get_hash
from exists import free_media_name


download_file_extension = u'.mp3'

url_gtts = 'http://translate.google.com/translate_tts?'

user_agent_string = 'Mozilla/5.0'

# Code

def get_word_from_google(source, language=None):
    if not source:
        raise ValueError('Nothing to download')
    # base_name = free_media_name(source, download_file_extension)
    get_url = build_query_url(source, language)
    print 'gtts url: ', get_url
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    temp_file = tempfile.NamedTemporaryFile(delete=False,
                                            suffix=download_file_extension)
    temp_file.write(response.read())
    temp_file.close()
    try:
        file_hash = get_hash(temp_file.name)
    except ValueError:
        os.remove(temp_file.name)
        # Simpler to just raise again
        raise
    extras = dict(source='GoogleTTS')
    return process_audio(temp_file.name, source, download_file_extension),\
        file_hash, extras


def build_query_url(source, language=None):
        qdict = {}
        if not language:
            language = default_language
        qdict['tl'] = language.encode('utf-8')
        qdict['q'] = source.encode('utf-8')
        return url_gtts + urllib.urlencode(qdict)
