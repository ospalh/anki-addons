# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: AGNU GPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#


'''
Maintain a blacklist of undesired files.
'''

import hashlib

blacklist_hashes = None

def is_blacklisted(file_name):
    retrieved_hash = hashlib.sha256(file(file_name, 'r').read())
    if retrieved_hash.hexdigest() in blacklist_hashes:
        raise ValueError('Retrieved file is in blacklist. ' +\
                             '(No pronunciation found.)')

def init():
    pass
