title: Play with mpg123
id: playwithmpg
main_file: play-with-mpgNN.py
type: addon
status: hackish
status_color: yellow
status_text_color: black
abstract: A quick hack add-on to play mp3 files with mpg123 or mpg321
first_image: mpg321.png
first_alt: Console output of mpg321

This is a quick hack to play mp3 files with a dedicated mp3 player,
rather than with mplayer. This intentionally bypasses the mplayer play
queue. The advantage is that replaying the media starts immediately,
even before the first playing is finished. The disadvantage is that
when a card contains several audio files, they are played
simultanounly, which is usually not what we want.
