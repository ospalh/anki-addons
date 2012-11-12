# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download pronunciations from GoogleTTS
'''

import os
import tempfile
import urllib
import urllib2


from .blacklist import get_hash
from .language import default_audio_language_code
from .process_audio import process_audio, unmunge_to_mediafile
from .siteicon import get_icon

download_file_extension = u'.mp3'

url_gtts = 'http://translate.google.com/translate_tts?'
icon_url = 'http://translate.google.com/'

user_agent_string = 'Mozilla/5.0'

site_icon = None
"""The sites's favicon. Reloaded on first download after program start."""


def get_word_from_google(source, language=None):
    if not source:
        raise ValueError('Nothing to download')
    maybe_get_icon()
    # base_name = free_media_name(source, download_file_extension)
    get_url = build_query_url(source, language)
    # This may throw an exception
    request = urllib2.Request(get_url)
    request.add_header('User-agent', user_agent_string)
    response = urllib2.urlopen(request)
    if 200 != response.code:
        raise ValueError(str(response.code) + ': ' + response.msg)
    with tempfile.NamedTemporaryFile(delete=False,
                                     suffix=download_file_extension) \
                                     as temp_file:
        temp_file.write(response.read())
    try:
        file_hash = get_hash(temp_file.name)
    except ValueError:
        os.remove(temp_file.name)
        # Simpler to just raise again
        raise
    extras = dict(source='GoogleTTS')
    try:
        return process_audio(temp_file.name, source, download_file_extension),\
            file_hash, extras, site_icon
    except:
        return unmunge_to_mediafile(temp_file.name, source,
                                    download_file_extension),\
            file_hash, extras, site_icon


def build_query_url(source, language=None):
        qdict = {}
        if not language:
            language = default_audio_language_code
        qdict['tl'] = language.encode('utf-8')
        qdict['q'] = source.encode('utf-8')
        return url_gtts + urllib.urlencode(qdict)


def maybe_get_icon():
    """Get the site icon when we haven't got it already."""
    global site_icon
    if site_icon:
        return
    site_icon = get_icon(icon_url, user_agent_string)
