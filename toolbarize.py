# -*- mode: Python ; coding: utf-8 -*-
# Copyright: Roland Sieker ( ospalh@gmail.com )
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Images:
# most icons from Anki1
# Exception: study.png,
# Found at http://www.vectorarts.net/vector-icons/free-study-book-icons/ ,
# "Free for Personal and Commercial Use"


from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from aqt import mw


"""
Add a standard tool bar to Anki2.

This Anki2 addon adds a standard tool bar (a QtToolBar) to the Anki
main window. By default a few buttons (QActions) are added, more can
be added by the user.
"""

__version__ = "1.0.0"

## Whether to show the old html-ish tool bar with the text
## html-link-"buttons".
# show_normal_tool_bar = True
show_normal_tool_bar = False

## Position of the new toolbar: either starting out above the old tool
## bar and movable, or below the old tool bar. In that case it can't
## be dragged to another position.
qt_toolbar_movable = True
# qt_toolbar_movable = False

## Add menus and menu items to to replace the old toolbar functions.
put_items_in_menu = True
# put_items_in_menu = False


icons_dir = os.path.join(mw.pm.addonFolder(), 'anki-1-icons')


def go_deck_browse():
    mw.moveToState("deckBrowser")

def go_study():
    mw.col.startTimebox()
    mw.moveToState("review")


# Make all the actions top level, so we can use them for the menu and
# the tool bar.

# _action.setIcon(QIcon(os.path.join(icons_dir, '.png')))

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




def add_tool_bar():
    """
    Add a Qt tool bar to Anki2.

    This is a more Anki-1-ish Qt tool bar with a number of rather big,
    colorful icons to replace the Anki 2 DSAB toolbar.
    """
    mw.qt_tool_bar = QToolBar()
    mw.qt_tool_bar.setAccessibleName('secondary tool bar')
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



def add_go_menu():
    # Add sync to the file memu. It was there in Anki 1.
    mw.form.menuCol.insertAction(mw.form.actionExport, sync_action)
    # Make a new top level menu and insert it.
    go_menu = QMenu("&Go", mw)
    mw.form.menubar.insertMenu(mw.menuBar().actions()[1] , go_menu)
    # Add DSAB to the new go menu
    go_menu.addAction(decks_action)
    go_menu.addAction(overview_action)
    go_menu.addAction(study_action)
    go_menu.addAction(add_notes_action)
    go_menu.addAction(browse_cards_action)
    mw.form.menuTools.addAction(statistics_action)



add_tool_bar()
if put_items_in_menu:
    add_go_menu()
if not show_normal_tool_bar:
    mw.toolbar.web.hide()
