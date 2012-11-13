# -*- mode: python; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, ospalh@gmail.com
#
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html
#


'''
Maintain a blacklist of undesired files.
'''

import hashlib
import os

# As in the main Anki code.
try:
    import simplejson as json
except ImportError:
    import json


from aqt import mw

blacklist_hashes = None
bl_file_path = os.path.join(
    mw.pm.addonFolder(), 'downloadaudio', 'blacklist.json')


def get_hash(file_name):
    """
    Return hash of the file.

    Return hash of the file file_name.  The more important function is
    that this throws a ValueError when the hash of the file is already
    in the list.
    """
    if not blacklist_hashes:
        load_hashes()
    retrieved_hash = hashlib.sha256(file(file_name, 'rb').read())
    if retrieved_hash.hexdigest() in blacklist_hashes:
        raise ValueError('Retrieved file is in blacklist. ' +
                         '(No pronunciation found.)')
    return retrieved_hash


def add_black_hash(black_hash):
    """Add a new hash to the list of blacklisted hashes."""
    global blacklist_hashes
    if not blacklist_hashes:
        load_hashes()
    blacklist_hashes.append(black_hash.hexdigest())
    save_hashes()


def load_hashes():
    """Load the blacklist from disk."""
    global blacklist_hashes
    blacklist_hashes = json.load(open(bl_file_path, 'r'))


def save_hashes():
    """Save the blacklist back to disk."""
    blacklist_file = open(bl_file_path, 'w')
    json.dump(blacklist_hashes, blacklist_file, indent=1)
    blacklist_file.close()
