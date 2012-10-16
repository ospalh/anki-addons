title: Quick replay
id: playwithmpg
main_file: Quick replay.py
type: addon
status: hackish
status_color: yellow
status_text_color: black
abstract: Play sound files with dedicated programs, bypassing the mplayer play queue. Like this, when you hit replay, the replay starts at once.
first_image: mpg321.png
first_alt: Console output of mpg321

Play mp3 files with mpg321, and flac and ogg files with play (that is,
sox). This bypasses the mplayer play queue. Like this, when you hit
replay, the replay starts at once.

<blockquote class="nb">Some versions of sox for Windows may not be
able to play sound. In this case, you may want to uninstall this
add-on.</blockquote>

The add-on checks if mpg321 and play are installed, but does nothing
to fix it if they are not there.

The advantage over the Play-with-mpgNN and Play with ogg add-ons is
that this plays all sound files of a card one after the other for each
play or replay, avoiding the ugly situation that several files are
played at once.
