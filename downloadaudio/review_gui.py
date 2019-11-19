# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–15 Roland Sieker <ospalh@gmail.com>
#

# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html


"""Present files and let the user decide what to do with them.

Show a list of downoladed files and present the user with a few
choices what to do wit each:
* Save: Put on the card and store the file. This is the ideal case.
* Keep file: Keep the file on disk but don't put it on the card.
* Delete: Just discard the file.
* Blacklist: Discard the file and also add the hash to a list of files
  that wil lbe automatically discarded in the future.

"""

import os

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QButtonGroup, QDialog, QDialogButtonBox, QFrame, \
    QGridLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QVBoxLayout

from aqt import mw
from anki.lang import _
from anki.sound import play, playFromText

from .download_entry import Action

icons_dir = os.path.join(mw.pm.addonFolder(), 'downloadaudio', 'icons')


def review_entries(note, retrieved_data, hide_text):
    """
    Show a dialog box where the user decides what to do.

    Show a dialog box where the user can listen to the downloaded
    audio and to already present audio and then decide whether to add,
    keep, delete, or blacklist the downloaded file.
    """
    if not note or not retrieved_data:
        raise ValueError('Nothing downloaded')
    review_files = ReviewFiles(note, retrieved_data, hide_text)
    if not review_files.exec_():
        raise RuntimeError('User cancel')
    # Go through the list and set the Action.
    for idx, entry in enumerate(retrieved_data):
        entry.action = review_files.buttons_groups[idx].checkedId()
    return retrieved_data


class ReviewFiles(QDialog):
    """
    A Dialog to let the user keep or discard files.
    """

    def __init__(self, note, entries_list, hide_text):
        super(ReviewFiles, self).__init__()
        self.note = note
        self.entries_list = entries_list
        self.num_columns = 8
        self.play_column = 2
        self.play_old_column = 3
        self.add_column = 4
        self.keep_column = 5
        self.delete_column = 6
        self.blacklist_column = 7
        self.show_skull_and_bones = any(
            entry.entry_hash for entry in self.entries_list)
        if not self.show_skull_and_bones:
            self.num_columns -= 1
        self.hide_text = hide_text
        if self.hide_text:
            self.num_columns -= 1
            self.play_column -= 1
            self.play_old_column -= 1
            self.add_column -= 1
            self.keep_column -= 1
            self.delete_column -= 1
            self.blacklist_column -= 1
        self.buttons_groups = []
        self.text_help = _("""<h4>Text used to retrieve audio.</h4>
<p>Mouse over the icons or texts below to see further information.</p>""")
        self.text_hide_help = _("""<h4>Audio source</h4>
<p>Mouse over the icons below to see further information.</p>
<p>The text that was used to retrieve the audio has been hidden to
reduce information leaks.</p> """)
        self.play_help = "<h4>Play the retrieved file.</h4>"
        self.play_old_help = _("""<h4>Play the current content of the
 audio field.</h4>
<p>No button means the field is empty. Hovering over the button shows
the current field content as text.</p>""")
        self.play_old_hide_help = _("""<h4>Play the current content of the
 audio field.</h4>
<p>No button means the field is empty.</p>""")
        self.play_old_empty_line_help = _("The target field is empty.")
        self.play_old_help_short = _("Play current field content.")
        self.add_help_text_long = _("""<h4>Add the sound to the card.</h4>
<p>This is the normal thing to select for a good download.
(You may want to select only one file in this column.)</p>""")
        self.add_help_text_short = _("Add this sound to the card")
        self.keep_help_text_long = _("""<h4>Keep the file.</h4>
<p>Keep this file in the media collection folder, but don’t add it to
the card. (This means the file will show up as an unused medium and
may be deleted during the unused media check.</p>""")
        self.keep_help_text_short = _("Keep this file")
        self.delete_help_text_long = _("""<h4>Delete the file.</h4>
<p>This is the normal thing to do with a file you don’t like.</p>""")
        self.delete_help_text_short = _("Delete this file")
        self.blacklist_help_text_long = _("""<h4>Blacklist the file.</h4>
Add an idetifier for this file to a blacklist. When this file is
downloaded again, it will be silently dropped. This behaviour is
useful for Japanesepod downloads. When your downloaded file tells you
that they are sorry, will add this soon &c., click on this.""")
        self.blacklist_help_text_short = _("Blacklist this file")
        self.blacklist_empty_line_help = _(
            "Blacklisting is only used for JapanesPod files.")
        self.initUI()

    def initUI(self):
        """Build the dialog box."""
        self.setWindowTitle(_('Anki – Download audio'))
        self.setWindowIcon(QIcon(":/icons/anki.png"))
        outer_layout = QVBoxLayout()
        self.setLayout(outer_layout)
        explanation = QLabel(self)
        if len(self.entries_list) > 1:
            explanation.setText(
                _('Please select an action for each downloaded file:'))
        else:
            explanation.setText(_('Please select what to do with the file:'))
        outer_layout.addWidget(explanation)
        scroll_area = QScrollArea()
        scroll_area.setFrameStyle(QFrame.Plain)
        inner_widget = QFrame(self)
        inner_widget.setSizePolicy(
            QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        layout = QGridLayout()
        inner_widget.setLayout(layout)
        scroll_area.setWidget(inner_widget)
        scroll_area.setWidgetResizable(True)
        outer_layout.addWidget(scroll_area)
        if not self.hide_text:
            text_head_label = QLabel(_('<b>Source text</b>'), inner_widget)
            layout.addWidget(text_head_label, 0, 0, 1, 2)
            text_head_label.setToolTip(self.text_help)
        else:
            text_head_label = QLabel(_('<b>Source</b>'), inner_widget)
            layout.addWidget(text_head_label, 0, 0)
            text_head_label.setToolTip(self.text_hide_help)
        play_head_label = QLabel(_('play'), inner_widget)
        play_head_label.setToolTip(self.play_help)
        layout.addWidget(play_head_label, 0, self.play_column)
        play_old_head_label = QLabel(_('play old'), self)
        if not self.hide_text:
            play_old_head_label.setToolTip(self.play_old_help)
        else:
            play_old_head_label.setToolTip(self.play_old_hide_help)
        layout.addWidget(play_old_head_label, 0, self.play_old_column)
        add_head_label = QLabel(_('add'), self)
        add_head_label.setToolTip(self.add_help_text_long)
        layout.addWidget(add_head_label, 0, self.add_column)
        keep_head_label = QLabel(_('keep'), self)
        keep_head_label.setToolTip(self.keep_help_text_long)
        layout.addWidget(keep_head_label, 0, self.keep_column)
        delete_head_label = QLabel(_('delete'), self)
        delete_head_label.setToolTip(self.delete_help_text_long)
        layout.addWidget(delete_head_label, 0, self.delete_column)
        if self.show_skull_and_bones:
            blacklist_head_label = QLabel(_('blacklist'), self)
            blacklist_head_label.setToolTip(self.blacklist_help_text_long)
            layout.addWidget(blacklist_head_label, 0, self.blacklist_column)
        rule_label = QLabel('<hr>')
        layout.addWidget(rule_label, 1, 0, 1, self.num_columns)
        self.create_rows(layout, inner_widget)
        dialog_buttons = QDialogButtonBox(self)
        dialog_buttons.addButton(QDialogButtonBox.Cancel)
        dialog_buttons.addButton(QDialogButtonBox.Ok)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        outer_layout.addWidget(dialog_buttons)

    def create_rows(self, layout, sarea):
        """Build the rows of the dialog box"""
        play_button_group = QButtonGroup(sarea)
        old_play_button_group = QButtonGroup(sarea)
        for num, entry in enumerate(self.entries_list, 2):
            tt_text = self.build_text_help_label(entry)
            ico_label = QLabel('', sarea)
            ico_label.setToolTip(tt_text)
            if entry.icon:
                ico_label.setPixmap(QPixmap.fromImage(entry.icon))
            layout.addWidget(ico_label, num, 0)
            tt_label = QLabel(entry.display_word, sarea)
            tt_label.setToolTip(tt_text)
            layout.addWidget(tt_label, num, 1)
            if self.hide_text:
                tt_label.hide()
            # Play button.
            t_play_button = QPushButton(sarea)
            play_button_group.addButton(t_play_button, num-2)
            t_play_button.setToolTip(self.play_help)
            t_play_button.setIcon(QIcon(os.path.join(icons_dir, 'play.png')))
            layout.addWidget(t_play_button, num, self.play_column)
            if self.note[entry.audio_field_name]:
                t_play_old_button = QPushButton(sarea)
                old_play_button_group.addButton(t_play_old_button, num-2)
                t_play_old_button.setIcon(
                    QIcon(os.path.join(icons_dir, 'play.png')))
                if not self.hide_text:
                    t_play_old_button.setToolTip(
                        self.note[entry.audio_field_name])
                else:
                    t_play_old_button.setToolTip(self.play_old_help_short)
                layout.addWidget(t_play_old_button, num, self.play_old_column)
            else:
                dummy_label = QLabel('', sarea)
                dummy_label.setToolTip(self.play_old_empty_line_help)
                layout.addWidget(dummy_label, num, self.play_old_column)
            # The group where we later look what to do:
            t_button_group = QButtonGroup(sarea)
            t_button_group.setExclusive(True)
            # Now the four buttons
            t_add_button = QPushButton(sarea)
            t_add_button.setCheckable(True)
            t_add_button.setFlat(True)
            t_add_button.setToolTip(self.add_help_text_short)
            t_add_button.setIcon(QIcon(os.path.join(icons_dir, 'add.png')))
            layout.addWidget(t_add_button, num, self.add_column)
            t_button_group.addButton(t_add_button, Action.Add)
            t_keep_button = QPushButton(sarea)
            t_keep_button.setCheckable(True)
            t_keep_button.setFlat(True)
            t_keep_button.setToolTip(self.keep_help_text_short)
            t_keep_button.setIcon(QIcon(os.path.join(icons_dir, 'keep.png')))
            layout.addWidget(t_keep_button, num, self.keep_column)
            t_button_group.addButton(t_keep_button, Action.Keep)
            t_delete_button = QPushButton(sarea)
            t_delete_button.setCheckable(True)
            t_delete_button.setFlat(True)
            t_delete_button.setToolTip(self.delete_help_text_short)
            t_delete_button.setIcon(
                QIcon(os.path.join(icons_dir, 'delete.png')))
            layout.addWidget(t_delete_button, num, self.delete_column)
            t_button_group.addButton(t_delete_button,  Action.Delete)
            t_blacklist_button = QPushButton(sarea)
            t_blacklist_button.setCheckable(True)
            t_blacklist_button.setFlat(True)
            t_blacklist_button.setToolTip(self.blacklist_help_text_short)
            t_blacklist_button.setIcon(
                QIcon(os.path.join(icons_dir, 'blacklist.png')))
            if entry.entry_hash:
                layout.addWidget(
                    t_blacklist_button, num, self.blacklist_column)
            else:
                t_blacklist_button.hide()
                dummy_label_bl = QLabel('', sarea)
                dummy_label_bl.setToolTip(self.blacklist_empty_line_help)
                layout.addWidget(dummy_label_bl, num, self.blacklist_column)
            t_button_group.button(entry.action).setChecked(True)
            # New: check a button based on how good the downloader is.
            t_button_group.addButton(t_blacklist_button, Action.Blacklist)
            self.buttons_groups.append(t_button_group)
        play_button_group.buttonClicked.connect(
            lambda button: play(
                self.entries_list[play_button_group.id(button)].file_path))
        # N.B.: anki.sound.play() plays files from anywhere, not just
        # from the colection.media folder. We should be good,
        # here. (This behaviour may be a security risk, idk.)
        old_play_button_group.buttonClicked.connect(
            lambda button: playFromText(
                self.note[
                    self.entries_list[
                        old_play_button_group.id(button)].audio_field_name]))

    def build_text_help_label(self, entry):
        """Build the bubble help text label."""
        ret_text = 'Text field: {0}'.format(entry.word_field_name)
        ret_text += '<br>Audio field: {0}'.format(entry.audio_field_name)
        for key, value in list(entry.extras.items()):
            ret_text += '<br>{0}: {1}'.format(key, value)
        return ret_text
