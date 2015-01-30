# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2015 Paul Hartmann <phaaurlt@gmail.com>
# Copyright © 2012–2015 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

from .blacklist import add_black_hash
from .processors import processor

class DownloadEntry(object):
    u"""Data about a single file downloaded by a downloader"""
    def __init__(self, field_data, file_path, extras, icon):
        self.file_path = file_path
        # Absolute file path of the downloaded audio file
        self.word = field_data.word
        self.word_field_name = field_data.word_field_name
        self.audio_field_name = field_data.audio_field_name
        self.file_extension = u'.mp3'
        # The file extension (with dot)
        self.extras = extras
        # A dict with strings of interesting informations, like
        # meaning numbers or name of speaker. Usually contains the
        # source.
        self.icon = icon
        # The downloader’s favicon
        self.action = Action.Add

        @property
        def display_name(self):
            return self.word

        @property
        def base_name(self):
            return self.word

        @property
        def entry_hash(self):
            return None
            # We are back to the way where the downloader checks
            # whether the file has a bad hash. This now doubles as the
            # old show_skull_and_bones. We show that button when this
            # has an interesting value. And that is set in JpodDownleadEntry

        def dispatch(self, note):
            u"""Do what should be done with the downloaded file

            Depending on self.action, do that action.

            * That is, move the file do the media folder if we want it
              on the note or just want to keep it.
            * Add it to the note if that’s what we want.
            * Delete it if we want just delete or blacklist it.
            * Blacklist the hash if that’s what we want."""
            if self.action == Action.Add or self.action == Action.Keep:
                media_fn = process.process_and_move(self)
                if self.action == Action.Add:
                    note[self.audio_field_name] += '[sound:' + media_fn + ']'
            if self.action == Action.Delete or self.action == Action.Blacklist:
                os.remove(self.file_path)
            if self.action == Action.Blacklist:
                add_black_hash(self.entry_hash)


class JpodDownloadEntry(DownloadEntry):
    u"""Data about a single file downloaded by a downloader"""
    def __init__(
            self, japanese_field_data, file_path, extras, icon, file_hash):
        DownloadEntry.__init__(
            self, japanese_field_data, file_path, extras, icon)
        self.kanji = japanese_field_data.kanji
        self.kana = japanese_field_data.kana
        self.hash_ = file_hash

        @property
        def base_name(self):
            return u"{kanji}_{kana}".format(kanji=self.kanji, kana=self.kana)

        @property
        def display_name(self):
            return u"{kanji}（{kana}）".format(kanji=self.kanji, kana=self.kana)
            # N.B.: those are “full width” (read, CJK) parentheses

        @property
        def entry_hash(self):
            return self.hash_

class Action(object):
    Add, Keep, Delete, Blacklist = range(0, 4)
