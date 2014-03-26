# -*- mode: python ; coding: utf-8 -*-
#
# Copyright © 2012–2014 Roland Sieker <ospalh@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/licenses/agpl.html

"""
Anki-2 add-on to show the learn count in the deck browser
"""

from aqt.deckbrowser import DeckBrowser
from anki.lang import _

__version__ = '0.1.0'

hide_big_numbers = True


def deck_browser_render_deck_tree(deck_browser, nodes, depth=0):
    if not nodes:
        return ""
    if depth == 0:
        buf = """
<tr><th colspan=5 align=left>%s</th><th class=count>%s</th>\
<th class=count>%s</th><th class=count>%s</th><th class=count></th></tr>""" % (
            _("Deck"), _("New"), _("Learn"), _("Due"))
        buf += deck_browser._topLevelDragRow()
    else:
        buf = ""
    for node in nodes:
        buf += deck_browser_deck_row(deck_browser, node, depth, len(nodes))
    if depth == 0:
        buf += deck_browser._topLevelDragRow()
    return buf


def deck_browser_deck_row(deck_browser, node, depth, cnt):
    name, did, due, lrn, new, children = node
    deck = deck_browser.mw.col.decks.get(did)
    if did == 1 and cnt > 1 and not children:
        # if the default deck is empty, hide it
        if not deck_browser.mw.col.db.scalar(
                "select 1 from cards where did = 1"):
            return ""
    # parent toggled for collapsing
    for parent in deck_browser.mw.col.decks.parents(did):
        if parent['collapsed']:
            buff = ""
            return buff
    prefix = "-"
    if deck_browser.mw.col.decks.get(did)['collapsed']:
        prefix = "+"

    def indent():
        return "&nbsp;"*6*depth
    if did == deck_browser.mw.col.conf['curDeck']:
        klass = 'deck current'
    else:
        klass = 'deck'
    buf = "<tr class='%s' id='%d'>" % (klass, did)
    # deck link
    if children:
        collapse = "<a class=collapse href='collapse:%d'>%s</a>" % (
            did, prefix)
    else:
        collapse = "<span class=collapse></span>"
    if deck['dyn']:
        extraclass = "filtered"
    else:
        extraclass = ""
    buf += """
    <td class=decktd colspan=5>%s%s<a class="deck %s" href='open:%d'>%s</a>\
</td>""" % (indent(), collapse, extraclass, did, name)

    # due counts
    def nonzeroColour(cnt, colour):
        if not cnt:
            colour = "#e0e0e0"
        if cnt >= 1000 and hide_big_numbers:
            cnt = "1000+"
        return """<span style='color: {};'>{}</span>""".format(colour, cnt)
    buf += """\
<td align=right>%s</td><td align=right>%s</td><td align=right>%s</td>""" % (
        nonzeroColour(new, "#009"),
        nonzeroColour(lrn, "#900"),
        nonzeroColour(due, "#070"))
    # options
    buf += "<td align=right class=opts>%s</td></tr>" % deck_browser.mw.button(
        link="opts:%d" % did,
        name="<img valign=bottom src='qrc:/icons/gears.png'>&#9662;")
    # children
    buf += deck_browser_render_deck_tree(deck_browser, children, depth+1)
    return buf


DeckBrowser._renderDeckTree = deck_browser_render_deck_tree
DeckBrowser._deckRow = deck_browser_deck_row
