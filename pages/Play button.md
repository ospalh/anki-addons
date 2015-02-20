title: Replay buttons on card
id: playbutton
main_file: play_button.py
date: 2014-07-31
tags: [review replay button]
type: addon
status: working
status_color: green
status_text_color: white
abstract: "Show a replay button for each file on a card."
first_image: play_buttons.png
first_alt: "Flash card with text and play buttons."
ankiweb_id: 498789867

Simple add-on that adds play buttons to the cards for audio and video
files.

With this it is possible to replay individual files. For example just
the pronunciation of a word, or just one example sentences.

<span  class="clear" />
<figure>
<img src="images/browserhide.png" alt=" Part of the Anki review window.
Text: みんなの日本語： に んぎょう.  Below part on the Anki card
browser. One line highlighted. Text: 人形; Japanisch-De...; にんぎょう">
<figcaption>The text <q lang="ja">みんなの日本語：</q> is shown on the card,
but not in the browser.</figcaption>
</figure>
The add-on also hides text with the CSS class `browserhide` in the
card browser. With its help the name of sound and video files is shown in
the card browser instead of the file name of the repaly arrow
image. The class is useful for cards where there is a text repeated
for every card, too. Put text  parts of your card template that
should not appear in the card browser into spans with the class `browserhide`.

The effect of the `browserhide` class is similar to using the
<q>Browser Appearance</q> feature hidden in the <q>More</q> button of
the template editor.

There is another add-on that implements *only* this hiding of text in
the text browser, called [Lean browser qa](Lean%20browser%20qa.html).
