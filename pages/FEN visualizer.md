title: FEN chess visualizer
id: fen
main_file: fen_visualizer.py
date: 2013-06-12
tags: [chess fen unicode]
type: addon
status: working
status_color: green
status_text_color: white
abstract: Display FEN data as a chess board.
first_image: excelsior.png
first_alt: "Chess board with the chess problem “excelsior”. See text for
precise position."
first_caption: "“White to mate in five with the least likely piece or
pawn.”"
ankiweb_id: 2923601993



Display a record of a chess position in
[Forsyth–Edwards Notation](http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
as a chess board.

The FEN record has to be complete (with active player, castling
&amp;c.) and it has to be enclosed in a pair of `[fen]` `[/fen]`tags.

This is the way that can be used on AnkiDroid and, apparently by some
old Anki1 add-on as well.


## Example
Just put ` [fen]n1rb4/1p3p1p/1p6/1R5K/8/p3p1PN/1PP1R3/N6k w - - 0 0[/fen]` on a card.

This add-on does the display without any images. When you don’t see
the chess pieces you should install a font with them. Maybe one from
[here](http://www.enpassant.dk/chess/fonteng.htm)
or
[here](http://www.chess.com/downloads/fonts).


## No development

This was a quick hack. I am neither playing chess nor terribly
interested in this, i just stumbled across the code that does the
equivalent for AnkiDroid. If anybody thinks ey can do a better job,
ey’s welcome to take over this add-on.
