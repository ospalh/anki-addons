# -*- mode: Python ; coding: utf-8 -*-
#
# Copyright © 2013 Roland Sieker <ospalh@gmail.com>
# Parts taken from from anki/latex.py
# Copyright: Damien Elmes <anki@ichi2.net>
#
# The style is from the AnkiDroid code, presumably
# Copyright (c) 2012 Kostas Spyropoulos <inigo.aldana@gmail.com>
#
# License: GNU AGPL, version 3 or later;
# http://www.gnu.org/copyleft/agpl.html

"""
Add-on for Anki 2 to show a chess board.

Add-on for Anki 2 to show a chess board based on data in
Forsyth–Edwards Notation (FEN) in `[fen]`/`[/fen]` tags.
"""

import re
from collections import namedtuple

from anki.cards import Card
from anki.hooks import addHook

__version__ = '1.0.0'

reverse_for_black = True
# reverse_for_black = False

FenData = namedtuple(
    'FenData',
    ['placement', 'active', 'castling', 'enpassant', 'halfmove', 'fullmove'])
piece = dict(zip('KQRBNPkqrbnp',
                 [unichr(s) for s in range(ord(u'♔'), ord(u'♟') + 1)]))
fen_re = re.compile(r"\[fen\](.+?)\[/fen\]", re.DOTALL | re.IGNORECASE)


fen_template = u"""<figure class="chess_diagram"><table class="chess_board">
{rows}
</table>
<figcaption>
<span class="fen_extra active">{act}</span>
<span class="fen_extra castling">{cas},</span>
<span class="fen_extra enp">ep: {enp},</span>
<span class="fen_extra half">½: {half},</span>
<span class="fen_extra full">M: {full}</span>
</figcaption>
</figure>
"""


def chess_card_css(self):
    """Add the chess style to the card style """
    return u"""<style scoped>
.chess_board {
  border:1px solid #333;
  border-spacing:0;
}

.chess_board td {
  background: -webkit-gradient(linear,0 0, 0 100%, from(#fff), to(#eee));
  -webkit-box-shadow: inset 0 0 0 1px #fff;
  font-size: 250%;
  height: 1em;
  width: 1em;
  vertical-align: middle;
  text-align: center;
}

.chess_board tr:nth-child(odd) td:nth-child(even),
.chess_board tr:nth-child(even) td:nth-child(odd) {
  background: -webkit-gradient(linear,0 0, 0 100%, from(#ccc), to(#eee));
  -webkit-box-shadow: inset 0 0 8px rgba(0,0,0,.4);
}
figure.chess_diagram  {
  display: inline-table;
}
figure.chess_diagram table{
  display: inline-block;
}
figure.chess_diagram figcaption{
  display: table-caption;
  caption-side: bottom;
}

</style>""" + old_css(self)


def counted_spaces(match):
    u"""Replace numbers with spaces"""
    return ' ' * int(match.group(0))


def insert_table(fen_match):
    u"""
    Replace well formed FEN data with a chess board diagram.

    This is the worker function that replaces the actual data.
    """
    fen_text = u''
    # Replace each piece with its symbol
    for c in fen_match.group(1):
        try:
            fen_text += piece[c]
        except KeyError:
            fen_text += c
    try:
        fen = FenData(*(fen_text.split()))
    except TypeError:
        # Not FEN data after all.
        return fen_match.group(0)
    rows = fen.placement.split('/')
    # Oops. When it is black’s move we have replaced the b or B with a bishop
    blacks_move = (fen.active == u'♝' or fen.active == u'♗')
    do_reverse = reverse_for_black and blacks_move
    if blacks_move:
        active = u'Black’s move'
    else:
        active = u'White’s move'
    if do_reverse:
        rows.reverse()
        active += u', black’s view'
    active += u'.'
    # We don’t realy care about the length. This should work for large
    # boards as well.
    trows = []
    for r in rows:
        # Replace numbers with spaces
        r = re.sub('[1-9][0-9]?', counted_spaces, r)
        if do_reverse:
            r = list(r)
            r.reverse()
        # And replace the row with an html table row
        tr = u'<tr>'
        for p in r:
            tr += u'<td>{0}</td>'.format(p)
        trows.append(tr + u'</tr>\n')
    return fen_template.format(
        rows=''.join(trows), act=active, cas=fen.castling,
        enp=fen.enpassant, half=fen.halfmove, full=fen.fullmove)


def insert_fen_table(txt, dummy_type, dummy_fields, dummy_model, dummy_data,
                     dummy_col):
    u"""
    Replace well formed  FEN data with a chess board diagram.

    This is a wrapper that looks for `[fen]`, `[/fen]` tags and
    replaces the content.
    """
    return fen_re.sub(insert_table, txt)


old_css = Card.css
Card.css = chess_card_css
addHook("mungeQA", insert_fen_table)
