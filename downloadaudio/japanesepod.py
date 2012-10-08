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

from process_audio import process_audio, unmunge_to_mediafile
from blacklist import get_hash
from exists import free_media_name


download_file_extension = u'.mp3'


url_jdict='http://assets.languagepod101.com/dictionary/japanese/audiomp3.php?'
# url_jdict='http://assets.languagepod101.com/dictionary/japanese/audioogg.php?'

# Code

def get_word_from_jpod(kanji, kana):
    """
    Download audio from kanji and kana from japanesepod.
    """
    base_name = build_base_name(kanji, kana)
    get_url = build_query_url(kanji, kana)
    # This may throw an exception
    request = urllib2.Request(get_url)
    # request.add_header('User-agent', 'PyMOTW (http://www.doughellmann.com/PyMOTW/)')
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
    extras = dict(source='Japanesepod')
    try:
        return process_audio(temp_file.name, base_name,
                             download_file_extension),\
            file_hash, extras
    except:
        # Most likely case when we get here: no pysox
        return unmunge_to_mediafile(temp_file.name, base_name,
                                    download_file_extension),\
            file_hash, extras


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
