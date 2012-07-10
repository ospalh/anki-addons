# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Images:
# most icons from Anki1
# Exception: study.png,
# Found at http://www.vectorarts.net/vector-icons/free-study-book-icons/ ,
# "Free for Personal and Commercial Use"


import os
from aqt import mw, clayout
from aqt.qt import *
from anki.hooks import wrap, addHook

"""
Add a standard tool bar to Anki2.

This Anki2 addon adds a standard tool bar (a QtToolBar) to the Anki
main window. By default a few buttons (QActions) are added, more can
be added by the user.
"""

__version__ = "1.0.4"

## Position of the new toolbar: either starting out above the old tool
## bar and movable, or below the old tool bar. In that case it can't
## be dragged to another position.
qt_toolbar_movable = True
# qt_toolbar_movable = False

icons_dir = os.path.join(mw.pm.addonFolder(), 'color-icons')


def go_deck_browse():
    """Open the deck browser."""
    mw.moveToState("deckBrowser")

def go_study():
    """Start studying cards."""
    mw.col.reset()
    mw.col.startTimebox()
    mw.moveToState("review")

def go_edit_current():
    """Edit the current card when there is one."""
    try:
        mw.onEditCurrent()
    except AttributeError:
        pass


def go_edit_layout():
    """Edit the current card's note's layout if there is one."""
    try:
        ccard = mw.reviewer.card
        clayout.CardLayout(mw, ccard.note(), ord=ccard.ord)
    except AttributeError:
        return

def toggle_text_tool_bar():
    if show_text_tool_bar_action.isChecked():
        mw.toolbar.web.show()
    else:
        mw.toolbar.web.hide()

def toggle_qt_tool_bar():
    if show_qt_tool_bar_action.isChecked():
        mw.qt_tool_bar.show()
    else:
        mw.qt_tool_bar.hide()

def toggle_more_tool_bar():
    # No real need to check if we are in review. Only then should we
    # be able to activate the action.
    if show_more_tool_bar_action.isChecked():
        mw.reviewer.more_tool_bar.show()
    else:
        mw.reviewer.more_tool_bar.hide()
        


# Make all the actions top level, so we can use them for the menu and
# the tool bar.

# Most of these icons are part of the standard version, but as they
# are not currently used by the standard version, they may disappear
# when dae gets around to doing some clean up. So bring them along,
# anyway.
sync_action = QAction(mw)
sync_action.setText("S&ync")
sync_action.setIcon(QIcon(os.path.join(icons_dir, 'sync.png')))
mw.connect(sync_action, SIGNAL("triggered()"), mw.onSync)
decks_action = QAction(mw)
decks_action.setText("&Deck browser")
decks_action.setIcon(QIcon(os.path.join(icons_dir, 'deck_browser.png')))
mw.connect(decks_action, SIGNAL("triggered()"), go_deck_browse)
overview_action = QAction(mw)
overview_action.setText("Deck overview")
overview_action.setIcon(QIcon(os.path.join(icons_dir, 'study_options.png')))
mw.connect(overview_action, SIGNAL("triggered()"), mw.onOverview)
study_action = QAction(mw)
study_action.setText("Study")
study_action.setIcon(QIcon(os.path.join(icons_dir, 'study.png')))
mw.connect(study_action, SIGNAL("triggered()"), go_study)
add_notes_action = QAction(mw)
add_notes_action.setText("Add notes")
add_notes_action.setIcon(QIcon(os.path.join(icons_dir, 'add.png')))
mw.connect(add_notes_action, SIGNAL("triggered()"), mw.onAddCard)
browse_cards_action = QAction(mw)
browse_cards_action.setText("Browse cards")
browse_cards_action.setIcon(QIcon(os.path.join(icons_dir, 'browse.png')))
mw.connect(browse_cards_action, SIGNAL("triggered()"), mw.onBrowse)
statistics_action = QAction(mw)
statistics_action.setText("Show statistics")
statistics_action.setIcon(QIcon(os.path.join(icons_dir, 'statistics.png')))
mw.connect(statistics_action, SIGNAL("triggered()"), mw.onStats)
edit_current_action = QAction(mw)
edit_current_action.setText("Edit current")
edit_current_action.setIcon(QIcon(os.path.join(icons_dir, 'edit_current.png')))
mw.connect(edit_current_action, SIGNAL("triggered()"), go_edit_current)
edit_layout_action = QAction(mw)
edit_layout_action.setText("Edit layout")
edit_layout_action.setIcon(QIcon(os.path.join(icons_dir, 'edit_layout.png')))
mw.connect(edit_layout_action, SIGNAL("triggered()"), go_edit_layout)


## Template to add actions:
# NN_action = QAction(mw)
# NN_action.setText("Show NN")
# NN_action.setIcon(QIcon(os.path.join(icons_dir, 'NN.png')))
# mw.connect(NN_action, SIGNAL("triggered()"), mw.onNN)


## Actions to show and hide the different tool bars.

show_text_tool_bar_action = QAction(mw)
show_text_tool_bar_action.setText("Show text tool bar")
show_text_tool_bar_action.setCheckable(True)
#show_text_tool_bar_action.setIcon(QIcon(os.path.join(icons_dir, 'browse.png')))
mw.connect(show_text_tool_bar_action, SIGNAL("triggered()"), toggle_text_tool_bar)

show_qt_tool_bar_action = QAction(mw)
show_qt_tool_bar_action.setText("Show icon bar")
show_qt_tool_bar_action.setCheckable(True)
show_qt_tool_bar_action.setChecked(True)
#show_qt_tool_bar_action.setIcon(QIcon(os.path.join(icons_dir, 'browse.png')))
mw.connect(show_qt_tool_bar_action, SIGNAL("triggered()"), toggle_qt_tool_bar)

show_more_tool_bar_action = QAction(mw)
show_more_tool_bar_action.setText("Show more tool bar")
show_more_tool_bar_action.setCheckable(True)
show_more_tool_bar_action.setChecked(True)
show_more_tool_bar_action.setEnabled(False)
#show_more_tool_bar_action.setIcon(QIcon(os.path.join(icons_dir, 'browse.png')))
mw.connect(show_more_tool_bar_action, SIGNAL("triggered()"), toggle_more_tool_bar)


## Add images to actions we already have. I skip a few where no icon
## really fits.

mw.form.actionDocumentation.setIcon(QIcon(os.path.join(icons_dir, 'help.png')))
mw.form.actionDonate.setIcon(QIcon(os.path.join(icons_dir, 'donate.png')))
mw.form.actionAbout.setIcon(QIcon(os.path.join(icons_dir, 'anki.png')))
mw.form.actionUndo.setIcon(QIcon(os.path.join(icons_dir, 'undo.png')))
mw.form.actionSwitchProfile.setIcon(QIcon(os.path.join(icons_dir, 'user-head.png')))
mw.form.actionImport.setIcon(QIcon(os.path.join(icons_dir, 'import.png')))
mw.form.actionExport.setIcon(QIcon(os.path.join(icons_dir, 'export.png')))
mw.form.actionExit.setIcon(QIcon(os.path.join(icons_dir, 'exit.png')))
mw.form.actionDownloadSharedPlugin.setIcon(
    QIcon(os.path.join(icons_dir, 'download-addon.png')))
mw.form.actionFullDatabaseCheck.setIcon(
    QIcon(os.path.join(icons_dir, 'check-db.png')))
mw.form.actionPreferences.setIcon(QIcon(os.path.join(icons_dir, 'preferences.png')))


## Template for adding images:
# mw.form.actionNn.setIcon(QIcon(os.path.join(icons_dir, 'nn.png')))


def add_tool_bar():
    """
    Add a Qt tool bar to Anki2.

    This is a more Anki-1-ish Qt tool bar with a number of rather big,
    colorful icons to replace the Anki 2 DSAB toolbar.
    """
    mw.qt_tool_bar = QToolBar()
    # mw.qt_tool_bar.setAccessibleName('secondary tool bar')
    mw.qt_tool_bar.setObjectName('qt tool bar')
    mw.qt_tool_bar.setIconSize(QSize(32,32))
    mw.qt_tool_bar.setStyleSheet(
        '''QToolBar{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fff, stop:1 #ddd);
border: none;
border-bottom: 1px solid #aaa;
}
''')
    # Conditional setup
    if qt_toolbar_movable:
        mw.qt_tool_bar.setFloatable(True)
        mw.qt_tool_bar.setMovable(True)
        mw.addToolBar(mw.qt_tool_bar)
    else:
        mw.qt_tool_bar.setFloatable(False)
        mw.qt_tool_bar.setMovable(False)
        mw.mainLayout.insertWidget(1, mw.qt_tool_bar)
    # Add the actions here
    mw.qt_tool_bar.addAction(sync_action)
    mw.qt_tool_bar.addAction(decks_action)
    mw.qt_tool_bar.addAction(overview_action)
    mw.qt_tool_bar.addAction(study_action)
    mw.qt_tool_bar.addAction(add_notes_action)
    mw.qt_tool_bar.addAction(browse_cards_action)
    mw.qt_tool_bar.addAction(statistics_action)
    #mw.qt_tool_bar.addAction(_action)




def add_more_tool_bar():
    # This realy belongs to the reviewer. TODO
    try:
        mw.reviewer.more_tool_bar = QToolBar()
    except AttributeError:
        return
    # mw.reviewer.more_tool_bar.setAccessibleName('secondary tool bar')
    mw.reviewer.more_tool_bar.setObjectName('more options tool bar')
    mw.reviewer.more_tool_bar.setIconSize(QSize(24,24))
    mw.reviewer.more_tool_bar.setStyleSheet(
        '''QToolBar{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fff, stop:1 #ddd);
border: none;
border-bottom: 1px solid #aaa;
}
''')
    mw.reviewer.more_tool_bar.setFloatable(False)
    mw.reviewer.more_tool_bar.setMovable(False)
    # Todo: get index of the bottom web button thingy.
    mw.mainLayout.insertWidget(2, mw.reviewer.more_tool_bar)
    # Add the actions here
    mw.reviewer.more_tool_bar.addAction(sync_action)
    more_tool_bar_off()


def add_to_menus():
    """
    Add a number of items to memus.
    
    Put the functions of the DASB old-style tool bar links into
    menus. Sync to the file menu, stats to the tools menu, the DASB,
    together with a study-withouts-overview item to a new go
    menu. Also add items to, d'uh, edit stuff to the edit menu.

    """
    # Add sync to the file memu. It was there in Anki 1.
    mw.form.menuCol.insertAction(mw.form.actionImport, sync_action)
    # Make a new top level menu and insert it.
    view_menu = QMenu("&View", mw)
    mw.form.menubar.insertMenu(mw.form.menuTools.menuAction() , view_menu)
    view_menu.addAction(show_qt_tool_bar_action)
    view_menu.addAction(show_text_tool_bar_action)
    view_menu.addAction(show_more_tool_bar_action)
    # And another one
    go_menu = QMenu("&Go", mw)
    mw.form.menubar.insertMenu(mw.form.menuTools.menuAction() , go_menu)
    # Add DSAB to the new go menu
    go_menu.addAction(decks_action)
    go_menu.addAction(overview_action)
    go_menu.addAction(study_action)
    go_menu.addAction(add_notes_action)
    go_menu.addAction(browse_cards_action)
    # Stats. Maybe this should go to help. Seems somewhat help-ish to
    # me, but not too much.
    mw.form.menuTools.addAction(statistics_action)
    # Add to the edit menu. The undo looked a bit forlorn.
    edit_menu = mw.form.menuEdit
    edit_menu.addAction(edit_current_action)
    edit_menu.addAction(edit_layout_action)



def edit_actions_off():
    """Switch off the edit actions."""
    try:
        edit_current_action.setEnabled(False)
        edit_layout_action.setEnabled(False)
    except AttributeError:
        pass


def edit_actions_on():
    """Switch on the edit actions."""
    try:
        edit_current_action.setEnabled(True)
        edit_layout_action.setEnabled(True)
    except AttributeError:
        pass

def more_tool_bar_off():
    show_more_tool_bar_action.setEnabled(False)
    try: 
        mw.reviewer.more_tool_bar.hide()
    except:
        pass


def maybe_more_tool_bar_on():
    show_more_tool_bar_action.setEnabled(True)
    if show_more_tool_bar_action.isChecked():
        try: 
            mw.reviewer.more_tool_bar.show()
        except:
            pass



def save_toolbars_visible():
    mw.pm.profile['ctb_show_toolbar'] = show_text_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_qt_toolbar'] = show_qt_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_more_toolbar'] = show_more_tool_bar_action.isChecked()


def save_toolbars_visible():
    mw.pm.profile['ctb_show_toolbar'] = show_text_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_qt_toolbar'] = show_qt_tool_bar_action.isChecked()
    mw.pm.profile['ctb_show_more_toolbar'] = show_more_tool_bar_action.isChecked()

def  load_toolbars_visible():
    try:
        ttb_on = mw.pm.profile['ctb_show_toolbar']
    except KeyError:
        ttb_on = False
    show_text_tool_bar_action.setChecked(ttb_on)
    toggle_text_tool_bar()    
    try:
        qtb_on = mw.pm.profile['ctb_show_qt_toolbar']
    except KeyError:
        qtb_on = True
    show_qt_tool_bar_action.setChecked(qtb_on)
    toggle_qt_tool_bar()
    try:
        mtb_on = mw.pm.profile['ctb_show_more_toolbar']
    except KeyError:
        mtb_on = True
    show_more_tool_bar_action.setChecked(mtb_on)
    # Don't toggle the more tool bar yet. It would be shown on the
    # deck browser screen
    # toggle_more_tool_bar()


# Create the menus
add_tool_bar()
add_more_tool_bar()
add_to_menus()
#mw.toolbar.web.hide()
mw.deckBrowser.show = wrap(mw.deckBrowser.show, edit_actions_off) 
mw.overview.show = wrap(mw.overview.show, edit_actions_on)
mw.reviewer.show = wrap(mw.reviewer.show, edit_actions_on)
mw.reviewer.show = wrap(mw.reviewer.show, maybe_more_tool_bar_on)
mw.overview.show = wrap(mw.overview.show, more_tool_bar_off)
mw.deckBrowser.show = wrap(mw.deckBrowser.show, more_tool_bar_off)
addHook("unloadProfile", save_toolbars_visible)
addHook("profileLoaded", load_toolbars_visible)


