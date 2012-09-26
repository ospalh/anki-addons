#!/usr/bin/env python
# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012 Roland Sieker, <ospalh@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt.qt import *
from aqt import mw


"""
Change the download audio parameters on user input.
"""

def update_pairs(general_pairs, japanese_pairs, language_code):
    """Return updated download information"""
    return general_pairs, japanese_pairs, language_code


class ReviewFields(QDialog):
    """
    A Dialog to let the user keep or discard files.
    """
    def __init__(self, general_pairs, japanese_pairs, language_code):
        self.general_pairs = general_pairs,
        self.japanese_pairs = japanese_pairs
        self.language_code = language_code
        super(ReviewFields, self).__init__() # Cut-and-pasted
        self.initUI()



    def initUI(self):
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(explanation, 0, 0, 1, 7)
        text_head_label = QLabel(u'<b>Source text</b>', self)
        text_head_label.setToolTip(self.text_help)
        layout.addWidget(text_head_label, 1,0)
        play_head_label = QLabel(u'play', self)
        play_head_label.setToolTip(self.play_help)
        layout.addWidget(play_head_label, 1,1)
        play_old_head_label = QLabel(u'play old', self)
        play_old_head_label.setToolTip(self.play_old_help)
        layout.addWidget(play_old_head_label, 1,2)
        add_head_label = QLabel(u'add', self)
        add_head_label.setToolTip(self.add_help_text_long)
        layout.addWidget(add_head_label, 1,3)
        keep_head_label = QLabel(u'keep', self)
        keep_head_label.setToolTip(self.keep_help_text_long)
        layout.addWidget(keep_head_label, 1,4)
        delete_head_label = QLabel(u'delete', self)
        delete_head_label.setToolTip(self.delete_help_text_long)
        layout.addWidget(delete_head_label, 1,5)
        blacklist_head_label = QLabel(u'blacklist', self)
        blacklist_head_label.setToolTip(self.blacklist_help_text_long)
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
        layout.addWidget(dialog_buttons, len(self.buttons_groups) + 3, 0, 1, 7)


    def create_rows(self, layout):
        play_button_group = QButtonGroup(self)
        old_play_button_group = QButtonGroup(self)
        for num, (source, dest, text, dl_fname, dl_hash, extras)\
                in enumerate(self.list, 3):
            tt_label = QLabel(text, self)
            tt_label.setToolTip(
                self.build_text_help_label(text, source, extras))
            layout.addWidget(tt_label, num, 0)
            # Play button.
            t_play_button = QPushButton(self)
            play_button_group.addButton(t_play_button, num - 3)
            t_play_button.setToolTip(self.play_help)
            t_play_button.setIcon(QIcon(os.path.join(icons_dir, 'play.png')))
            layout.addWidget(t_play_button, num, 1)
            if self.note[dest]:
                t_play_old_button = QPushButton(self)
                old_play_button_group.addButton(t_play_old_button, num - 3)
                t_play_old_button.setIcon(
                    QIcon(os.path.join(icons_dir, 'play.png')))
                t_play_old_button.setToolTip(self.note[dest])
                layout.addWidget(t_play_old_button, num, 2)
            else:
                dummy_label = QLabel('',self)
                dummy_label.setToolTip(self.play_old_empty_line_help)
                layout.addWidget(dummy_label, num, 2)
            # The group where we later look what to do:
            t_button_group = QButtonGroup(self)
            t_button_group.setExclusive(True)
            # Now the four buttons
            t_add_button = QPushButton(self)
            t_add_button.setCheckable(True)
            t_add_button.setChecked(True)
            t_add_button.setFlat(True)
            t_add_button.setToolTip(self.add_help_text_short)
            t_add_button.setIcon(QIcon(os.path.join(icons_dir, 'add.png')))
            layout.addWidget(t_add_button, num, 3)
            t_button_group.addButton(t_add_button, action['add'])
            t_keep_button = QPushButton(self)
            t_keep_button.setCheckable(True)
            t_keep_button.setFlat(True)
            t_keep_button.setToolTip(self.keep_help_text_short)
            t_keep_button.setIcon(QIcon(os.path.join(icons_dir, 'keep.png')))
            layout.addWidget(t_keep_button, num, 4)
            t_button_group.addButton(t_keep_button,  action['keep'])
            t_delete_button = QPushButton(self)
            t_delete_button.setCheckable(True)
            t_delete_button.setFlat(True)
            t_delete_button.setToolTip(self.delete_help_text_short)
            t_delete_button.setIcon(QIcon(os.path.join(icons_dir,
                                                       'delete.png')))
            layout.addWidget(t_delete_button, num, 5)
            t_button_group.addButton(t_delete_button,  action['delete'])
            t_blacklist_button = QPushButton(self)
            t_blacklist_button.setCheckable(True)
            t_blacklist_button.setFlat(True)
            t_blacklist_button.setToolTip(self.blacklist_help_text_short)
            t_blacklist_button.setIcon(QIcon(os.path.join(icons_dir,
                                                          'blacklist.png')))
            layout.addWidget(t_blacklist_button, num, 6)
            t_button_group.addButton(t_blacklist_button,  action['blacklist'])
            self.buttons_groups.append(t_button_group)
        play_button_group.buttonClicked.connect(
            lambda button: play(self.list[play_button_group.id(button)][3]))
        old_play_button_group.buttonClicked.connect(
            lambda button: playFromText(self.note[
                    self.list[old_play_button_group.id(button)][1]]))


    def build_text_help_label(self, text, source, extras):
        ret_text = u'Source text: <b>{0}</b><br>from field: {1}'\
            .format(text, source)
        for key, value in extras.items():
            ret_text += u'<br>{0}: {1}'.format(key, value)
        return ret_text
