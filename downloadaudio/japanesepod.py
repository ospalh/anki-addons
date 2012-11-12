# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
# Inspiration and source of the URL: Tymon Warecki
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html


'''
Download Japanese pronunciations from Japanesepod
'''


import os
import tempfile
import urllib
import urllib2

from .blacklist import get_hash
from .process_audio import process_audio, unmunge_to_mediafile
from .siteicon import get_icon

download_file_extension = u'.mp3'

url_jdict = \
    'http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?'
icon_url = "http://www.japanesepod101.com/"
site_icon = None
"""The sites's favicon. Reloaded on first download after program start."""


def get_word_from_jpod(kanji, kana):
    """
    Download audio from kanji and kana from japanesepod.
    """
    maybe_get_icon()
    base_name = build_base_name(kanji, kana)
    get_url = build_query_url(kanji, kana)
    # This may throw an exception
    request = urllib2.Request(get_url)
    # request.add_header('User-agent', 'PyMOTW
    # (http://www.doughellmann.com/PyMOTW/)')
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
    extras = dict(source='Japanesepod')
    try:
        return process_audio(temp_file.name, base_name,
                             download_file_extension),\
            file_hash, extras, site_icon
    except:
        # Most likely case when we get here: no pysox
        return unmunge_to_mediafile(temp_file.name, base_name,
                                    download_file_extension),\
            file_hash, extras, site_icon


def build_query_url(kanji, kana):
        qdict = {}
        if kanji:
            qdict['kanji'] = kanji.encode('utf-8')
        if kana:
            qdict['kana'] = kana.encode('utf-8')
        return url_jdict + urllib.urlencode(qdict)


def build_base_name(kanji, kana):
    """Base of the file name to come."""
    base_name = kanji
    if kana:
        base_name += u'_' + kana
    return base_name


def maybe_get_icon():
    """Get the site icon when we haven't got it already."""
    global site_icon
    if site_icon:
        return
    site_icon = get_icon(icon_url)
