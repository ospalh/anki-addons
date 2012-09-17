#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


"""
Present files and let the user decide what to do with them.

Show a list of downoladed files and present the user with a few
choices what to do wit each:
* Save: Put on the card and store the file. This is the ideal case.
# Possible addition: * Keep file: Keep the file on disk but don't put
 it on the card.
* Delete: Just discard the file.

* Blacklist: Discard the file and also add the hash to a list of files
             that wil lbe automatically discarded in the future.
"""

import os
from aqt import mw
from anki.sound import play
from blacklist import add_black_hash



from aqt.qt import *

icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')

# to make the code a bit more readable
action = {'add' : 0, 'keep': 1, 'delete': 2, 'blacklist': 3}

def store_or_blacklist(note, retrieved_data):
    if not note or not retrieved_data:
        return
    review_files = ReviewFiles(note, retrieved_data)
    if not review_files.exec_():
        remove_all_files(retrieved_data)
        return
    # Go through the list once and just do what needs to be done.
    # Keep track if we have to do some clean up.
    items_added = False
    for idx, (source, dest, text, dl_fname, dl_hash) \
            in enumerate(retrieved_data):
        action_id = review_files.buttons_groups[idx].checkedId()
        print 'id for row ', idx, 'is ', action_id
        if action_id == action['add']:
            print 'add for list row ', idx
            # Add dest field and file name pair to list
            items_added = True
            note[dest] += '[sound:' + dl_fname + ']'
        if action_id == action['delete']:
            print 'remove for list row ', idx
            os.remove(os.path.join(mw.mediaDir(), dl_fname))
        if action_id == action['blacklist']:
            print 'blacklist for list row ', idx
            add_black_hash(dl_hash)
    if items_added:
        note.flush()


def remove_all_files(files_etc):
    pass

class ReviewFiles(QDialog):
    """
    A Dialog to let the user keep or discard files.
    """
    def __init__(self, note, files_list):
        self.note = note
        self.list = files_list
        # self.buttonBox = None
        self.buttons_groups = []
        super(ReviewFiles, self).__init__() # Voodoo code. Look it up!
        self.initUI()



    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        explanation = QLabel(self)
        if len(self.list) > 1:
            explanation.setText(
                u'Please select an action for each downloaded file:')
        else:
            explanation.setText(u'Please select what to do with the file:')
        layout.addWidget(explanation, 0, 0, 1, 7)
        text_head_label = QLabel(u'<b>Source text</b>', self)
        layout.addWidget(text_head_label, 1,0)
        source_head_label = QLabel(u'(from field)', self)
        layout.addWidget(source_head_label, 1,1)
        play_head_label = QLabel(u'review', self)
        layout.addWidget(play_head_label, 1,2)
        add_head_label = QLabel(u'add', self)
        layout.addWidget(add_head_label, 1,3)
        keep_head_label = QLabel(u'keep', self)
        layout.addWidget(keep_head_label, 1,4)
        delete_head_label = QLabel(u'delete', self)
        layout.addWidget(delete_head_label, 1,5)
        blacklist_head_label = QLabel(u'blacklist', self)
        layout.addWidget(blacklist_head_label, 1,6)
        rule_label = QLabel('<hr>')
        layout.addWidget(rule_label, 2, 0, 1, 7)
        self.create_rows(layout)
        dialog_buttons = QDialogButtonBox(self)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        self.connect(dialog_buttons, SIGNAL("accepted()"),
                     self, SLOT("accept()"))
        self.connect(dialog_buttons, SIGNAL("rejected()"),
                     self, SLOT("reject()"))
        layout.addWidget(dialog_buttons, 5+ 3, 0, 1, 7)


    def create_rows(self, layout):
        for num, (source, dest, text, dl_fname, dl_hash)\
                in enumerate(self.list, 3):
            tt_label = QLabel(text, self)
            layout.addWidget(tt_label, num, 0)
            tf_label = QLabel(source, self)
            layout.addWidget(tf_label, num, 1)
            # Play button.
            t_play_button = QPushButton(self)
            t_play_button.setIcon(QIcon(os.path.join(icons_dir, 'play.png')))
            layout.addWidget(t_play_button, num, 2)
            t_play_button.clicked.connect(lambda: play(dl_fname))
            t_button_group = QButtonGroup(self)
            t_button_group.setExclusive(True)
            # Now the four buttons
            t_add_button = QPushButton(self)
            t_add_button.setCheckable(True)
            t_add_button.setChecked(True)
            t_add_button.setFlat(True)
            t_add_button.setIcon(QIcon(os.path.join(icons_dir, 'add.png')))
            layout.addWidget(t_add_button, num, 3)
            t_button_group.addButton(t_add_button, action['add'])
            t_keep_button = QPushButton(self)
            t_keep_button.setCheckable(True)
            t_keep_button.setFlat(True)
            t_keep_button.setIcon(QIcon(os.path.join(icons_dir, 'keep.png')))
            layout.addWidget(t_keep_button, num, 4)
            t_button_group.addButton(t_keep_button,  action['keep'])
            t_delete_button = QPushButton(self)
            t_delete_button.setCheckable(True)
            t_delete_button.setFlat(True)
            t_delete_button.setIcon(QIcon(os.path.join(icons_dir,
                                                       'delete.png')))
            layout.addWidget(t_delete_button, num, 5)
            t_button_group.addButton(t_delete_button,  action['delete'])
            t_blacklist_button = QPushButton(self)
            t_blacklist_button.setCheckable(True)
            t_blacklist_button.setFlat(True)
            t_blacklist_button.setIcon(QIcon(os.path.join(icons_dir,
                                                          'blacklist.png')))
            layout.addWidget(t_blacklist_button, num, 6)
            t_button_group.addButton(t_blacklist_button,  action['blacklist'])
            self.buttons_groups.append(t_button_group)
