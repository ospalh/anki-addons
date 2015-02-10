title: Add audio field
id: addaudio
type: subpage
ankiweb_id: 3100585138
parent: Download audio
extra_jq_script: audio_tips.js

The add-on requires a field called <q>Audio</q>, or that contains the word
<q>Audio</q>, to put the downloaded data.

While adding or renaming fields in Anki isn’t too hard, a short guide
might be helpful.

## <span id="one_try">Step one: Try</span>

<figure>
<img src="images/manual_audio.png" alt="Anki with a card shown and the
mouse pointing to the menu item
Edit/Media/Manual audio. ">
<figcaption>When reviewing, activate the
Edit/Media/Manual audio menu.</figcaption>
</figure>
When you downloaded a shared deck that already has some audio data,
it may work without any change. Start reviewing the new deck. On the
first card, try the menu item
<q>Edit/Media/Manual audio</q>.

<span class="clear" />
<figure>
<img src="images/preview_audio.png" alt="Dialog window with text
starting Requests to send to the download sites">
<figcaption>When you get this, dialog, the add-on will go fetch.</figcaption>
</figure>
When a dialog with “Requests to send to the download sites” and with
the right word in the edit box appears you are in luck and your model
already works with this add-on.

<span class="clear" />
<figure>
<img src="images/nothing_to_download.png" alt="Anki with a card shown
and a message reading nothing to download">
<figcaption>When you get this, you need to add an audio field.</figcaption>
</figure>


## Before you go on

Adding fields or changing field names requires a full upload of the
collection. Make sure you sync before you do this.

<blockquote class="nb">When you learn with mobile devices or with
AnkiWeb, sync on these remote clients first. Then sync your desktop
client. Only then start checking the field list.</blockquote>


## Checking the field list

When the download test didn’t work, you should click on the  <q>Edit</q>
button in the bottom left.

<figure style="width: 333px;">
<img src="images/front_back.png" alt="Edit current window with fields
Front and Back. ">
<img src="images/id_franz_de.png" alt="Edit current window with fields
Französisch, Deutsch ...">
<figcaption>Candidates for downloading are the first field or the
field named <q lang='de'>Französisch</q>.</figcaption>
</figure>

Take a look at the field list and decide for which field or
fields you would like to download data.

Then click on the <q>Fields...</q> button.


## Adding an audio field

In the <q>Fields for NN</q> dialog, click on <q>Add</q>

<span class="clear" />
### Add for the first field

<figure>
<img src="images/add_for_base.png" alt="Dialog with text Field name:
and input text Audio.">
<figcaption>Here we want to download for the first field</figcaption>
</figure>

When you want to download for the first field, just type <q>Audio</q> for
the new field name. Then click  <q>OK</q>.

<span class="clear" />
### <span id="otherfield">Add for <span class="qtbase orfirst">other</span> field</span>

<figure>
<img src="images/add_not_first.png" alt="Anki review window with a
picture of a bird in the first field and the word l'oiseau in the
second field. That word and the field name Back are marked. To the
right a dialog with the field names. The word Back is marked. Below a
dialog. Text: Field name. Text input: Back Audio. The
word Back is marked.">
<figcaption>Look for what you want to download, then use that field’s
name in the new field.</figcaption>
</figure>

Alternatively, when the field you want to download for is not the
first field, you should use that field’s name, followed by
<q>Audio</q>. Then click  <q>OK</q> here, too.

In the example, sending pictures of birds to GoogleTTS would not
work. So we look for interesting text in the <q>Edit Current</q>
window: <q lang='fr'>l'oiseau</q>, marked in red with a <q>1</q> in
the image. That text is in the field named <q>Back</q> (blue 2). That
field name appears again in the <q>Fields for NN</q>
dialog. (blue 3). Use this field name together with the word
<q>Audio</q> as the new field name. In this case, use <q>Back
Audio</q>. (blue 4)

<span class="clear" />
### <span id="thewarning">The warning</span>

<figure>
<img src="images/sync_warning.png" alt="Dialog with text The requested
change will require a full upload of the database when you next
synchronize your collection. If you have reviews or other changes
waiting on another device that haven't been synchronized here yet,
they will be lost. Continue?">
<figcaption>Read and decide.</figcaption>
</figure>
At this point, a warning dialog may appear. If you are not sure about
this, click <q>No</q>, sync changes from remote devices to this
collection and do the steps above again. If you are sure, click
<q>Yes</q>.


### More fields

You can add more than one audio field to download from more than one
source field by repeating the [Add for other field](#otherfield)
step.


<span class="clear" />
## <span id="renamefields">Rename fields</span>

<figure>

<img src="images/00906.png" alt="Anki review window. Text:
Übersetzen Ja, mein Herr. Oui monsieur. 00906. Below, a dialog
window. Text: Requests send to the download sites ID 00906">
<figcaption>No Sir. I do not want to learn to pronounce
<q>00906</q>.</figcaption>
</figure>
When the [test above](#one_try)
tried to download from a wrong field, you have to rename the audio
field. Doing this is similar to [adding an audio field](#otherfield).

<figure>
<img src="images/change_name.png" alt="On the left: Window with a list
of fields with their content, ID:00906, Französisch:Oui,
monsieur, Deutsch: Ja, mein Herr and
Audio:sound:00906.mp3. Französisch is marked in blue, Oui,
monsieur in red and Audio in yellow. To the
right a dialog with the field names. Französisch is marked in blue,
Audio is selected and marked in yellow. Below a
dialog. Text: New name. Text input: Französisch Audio. Französisch is
marked in blue, Audio in yellow.">
<figcaption>Change the name of the field <q>Audio</q>. Add
the name of the source field to the name.</figcaption>
</figure>

* Start reviewing.
* From the main window, click the <q>Edit</q> button in the
  bottom left.
* Look at the field list: <ul> <li>There should be a field named
  <q>Audio</q> or <q>Sound</q>. (yellow in the image)</li>
  <li>Identify the interesting text (<q lang='fr'>Oui monsieur.</q>,
  red). Note the field name (<q lang='de'>Französisch</q>, blue)</li>
  </ul>
* Click the <q>Fields...</q> button
* The two field names, (<q lang='de'>Französisch</q> and
  <q>Audio</q>), appear in the list and are marked in blue and yellow.
* Click on <q>Audio</q> to select the field.
* Then click the <q>Rename</q> button.
* As the new name, add the other field’s name to the old
  name. (<q>Französisch Audio</q> or <q>Audio Französisch</q>, either
  will work.)
* Click <q>OK</q>. [The warning](#thewarning) may pop up.

## Go back

When you are finished with setting up the fields, simply click
<q>Close</q> in the <q>Fields for NN</q> dialog and <q>Close</q> again
in the <q>Edit Current</q> dialog.
