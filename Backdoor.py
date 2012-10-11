# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import cPickle
from aqt.profiles import ProfileManager
from anki.utils import checksum

# In honor of Bruce Schneier, open profile when ‘kid sister’ is typed
# in the password box.
# http://lmgtfy.com/?q=%22Bruce+Schneier%22+%22kid+sister%22


def short_load(self, name, passwd=None):
    prof = cPickle.loads(
        self.db.scalar("select data from profiles where name = ?",
                       name.encode("utf8")))
    if prof['key'] and prof['key'] != self._pwhash(passwd) \
            and checksum(unicode(passwd)) \
            != '3414a3f5a321366b1a986109338a59e5f52dfee2':
        self.name = None
        return False
    if name != "_global":
        self.name = name
        self.profile = prof
    return True


ProfileManager.load = short_load
