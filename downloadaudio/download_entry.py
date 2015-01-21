# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Copyright © 2012–2013 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


class DownloadEntry(object):
    u"""Data about a single file downloaded by a downloader"""
    def __init__(
            self, word_file_path, word_file_name, base_name, display_text,
            file_extension=u'.wav', extras={},
            show_skull_and_bones=False):
        self.word_file_path = word_file_path
        # Absolute file path of the downloaded audio file
        self.word_file_name = word_file_name
        # The file name of the downloaded audio file (the
        # last component of word_file_path
        self.base_name = base_name
        # Base of the file name in the media direcotry, without file
        # extension or number. (A number gets added later when we have
        # several files for one word.)
        self.display_text = display_text
        # Text shown as source after download
        self.file_extension = file_extension
        # The file extension (with dot)
        self.extras = extras
        # A dict with strings of interesting informations, like
        # meaning numbers or name of speaker, or an empty dict.
        # (shown in the tooltip)
        self.show_skull_and_bones = show_skull_and_bones
        # Should we show the skull and crossbones in the review
        # dialog?
        # Normal downloaders should leave this alone. The point of the
        # whole blacklist mechanism is that JapanesePod can't say
        # no. Only when there is a chance that we have a file we want
        # to blacklist (that is, when we actually downloaded something
        # from Japanesepod) should we set this to True.
