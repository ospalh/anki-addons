title: Somebody else’s problem
id: sep
main_file: somebody_elses_problem.py
type: addon
date: 2013-06-07
status: working
status_color: green
status_text_color: white
abstract: Quick hack to hide field content only on the desktop client.
first_image: ipu.png
first_image_attributes: 'style="background-color: white;"'
first_alt: The Invisible Pink Unicorn.
first_caption: "An SEP-field is an easy way to make things
invisible."
ankiweb_id: 4073019785

This is a quick hack to hide field content only on the desktop client.

Put fields you don’t want to see on the desktop into `{{sep:NN}}`
templates, and they become
[somebody else’s problem](http://hitchhikers.wikia.com/wiki/Somebody_Else%27s_Problem_field).

On AnkiWeb and AnkiDroid (and AnkiMobile), the template is unknown and
default behavior is to show the text without modification – the field
becomes visible again.

This is only needed for audio/video files. Text or images can be
hidden with clever CSS:

`<span class=justdt>Shown on desktop</span>
<span class=justmobile>Shown on mobile</span>`

in the card template and
<pre><code>.justdt {display:none;}
.mobile .justmobile {display:inline;}
.mobile .justdt {display:none;}</code></pre>
in the card CSS.

The
[problem](https://groups.google.com/forum/?fromgroups=&hl=en#!topic/ankisrs/jK3Jh4EzwKE)
was that i didn’t want to copy a bunch of video files to my Android
device to save FAT
[directory entries](http://en.wikipedia.org/wiki/File_Allocation_Table#VFAT_long_file_names),
which are in short supply if you have a collection with many files
with long non-ASCII names.

<blockquote class="nb">
Due to a <a
href="https://code.google.com/p/ankidroid/issues/detail?id=1458">problem
in AnkiDroid</a>, you should make sure that the files copied to the
Android device appear first on the cards.
</blockquote>
