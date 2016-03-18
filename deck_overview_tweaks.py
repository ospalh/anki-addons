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

__version__ = '1.0.0'

hide_big_numbers = True
big_number = 1000
subdecks_hidden_bullet = u"+"
# subdecks_hidden_bullet = u"➢"
subdecks_shown_bullet = u"-"
# subdecks_shown_bullet = u"⌄"
# no_subdecks_bullet = u""
no_subdecks_bullet = u"•"
zero_style = "color: #e0e0e0;"
new_style = "color: #009;"
learn_style = "color: #900;"
due_style = "color: #070;"
sum_style = "color: black;"
deck_browser_css = """
.count {
  width: unset; padding-left: 0.75em;
}
.decktd {
  width: 100%;
}
"""


def nonzero_style(cnt, style):
    """Style text"""
    if cnt > big_number and hide_big_numbers:
        cnt = "&gt;{bn}".format(bn=big_number)
    if not cnt:
        style = zero_style
    return '<span style="{};">{}</span>'.format(style, cnt)


def deck_browser_render_deck_tree(deck_browser, nodes, depth=0):
    if not nodes:
        return ""
    sum_new = 0
    sum_lrn = 0
    sum_due = 0
    if depth == 0:
        buf = u"""\
<thead>
  <tr>
    <th align=left>{}</th>
    <th class=count>{}</th>
    <th class=count>{}</th>
    <th class=count>{}</th>
    <th class=count></th>
  </tr>
</thead>
<tbody>
""".format(_(u"Deck"), _(u"New"), _(u"Learn"), _(u"Due"))
        buf += deck_browser._topLevelDragRow()
    else:
        buf = ""
    for node in nodes:
        dummy_name, dummy_did, due, lrn, new, dummy_children = node
        sum_due += due
        sum_lrn += lrn
        sum_new += new
        buf += deck_browser_deck_row(deck_browser, node, depth, len(nodes))
    if depth == 0:
        buf += deck_browser._topLevelDragRow()
        buf += u"""\
</tbody>
<tfoot>
  <tr>
    <th align=left>{}</th>
    <th class=count>{}</th>
    <th class=count>{}</th>
    <th class=count>{}</th>
    <th class=count>{}</th>
  </tr>
</tfoot>
""".format(_(u"Sum"), nonzero_style(sum_new, new_style),
           nonzero_style(sum_lrn, learn_style),
           nonzero_style(sum_due, due_style),
           nonzero_style(sum_new + sum_lrn + sum_due, sum_style))
    return buf


def deck_browser_deck_row(deck_browser, node, depth, cnt):
    name, did, due, lrn, new, children = node
    deck = deck_browser.mw.col.decks.get(did)
    if did == 1 and cnt > 1 and not children:
        # If the default deck is empty, hide it
        if not deck_browser.mw.col.db.scalar(
                "select 1 from cards where did = 1"):
            return ""
    # Parent toggled for collapsing
    for parent in deck_browser.mw.col.decks.parents(did):
        if parent['collapsed']:
            buff = ""
            return buff
    bullet = subdecks_shown_bullet
    if deck_browser.mw.col.decks.get(did)['collapsed']:
        bullet = subdecks_hidden_bullet

    def indent():
        return "&nbsp;"*6*depth
    if did == deck_browser.mw.col.conf['curDeck']:
        klass = 'deck current'
    else:
        klass = 'deck'
    buf = "<tr class='%s' id='%d'>" % (klass, did)
    # Deck link
    if children:
        collapse = \
            u"<a class=collapse href='collapse:{did}'>{bullet}</a>".format(
                did=did, bullet=bullet)
    else:
        collapse = u"<span class=collapse>{bullet}</span>".format(
            bullet=no_subdecks_bullet)
    if deck['dyn']:
        extraclass = "filtered"
    else:
        extraclass = ""
    buf += u"""\
    <td class=decktd>%s%s<a class="deck %s"\
 href='open:%d'>%s</a></td>""" % (
        indent(), collapse, extraclass, did, name)
    # Due counts
    buf += u"""<td align=right>{}</td><td align=right>{}</td>\
<td align=right>{}</td>""".format(
        nonzero_style(new, new_style),
        nonzero_style(lrn, learn_style),
        nonzero_style(due, due_style))
    # Options
    buf += u"<td align=right class=opts>%s</td></tr>" % deck_browser.mw.button(
        link="opts:%d" % did,
        name=u"<img valign=bottom src='qrc:/icons/gears.png'>▾")
    # Children
    buf += deck_browser._renderDeckTree(children, depth+1)
    return buf


DeckBrowser._renderDeckTree = deck_browser_render_deck_tree
DeckBrowser._deckRow = deck_browser_deck_row
DeckBrowser._css += deck_browser_css
