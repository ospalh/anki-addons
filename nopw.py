# -*- mode: python ; coding: utf-8 -*-
# © Roland Sieker <ospalh@gmail.com>
# Based on code by Damien Elmes <anki@ichi2.net>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import cPickle
from aqt.profiles import ProfileManager

def shortLoad(self, name, passwd=None):
    prof = cPickle.loads(
        self.db.scalar("select data from profiles where name = ?",
                       name.encode("utf8")))
    if name != "_global":
        self.name = name
        self.profile = prof
    return True


ProfileManager.load = shortLoad
