title: More audio cards
id: morecards
type: subpage
ankiweb_id: 3100585138
parent: Download audio

One way to use the downloaded audio is to create a special card for
hearing comprehension.

## Template editor

<figure style="width:648px;">
<img src="images/card_types.png" alt="Window with tabs reading Forward
Reverse Example at the top. The left of the main area is split in
three parts, Front template, Styling and Back template. The right is
split in two: Front preview and Back preview.">
<figcaption>The card template editor for a moderately complex note type.</figcaption>
</figure>
To get the template editor, start reviewing. Then click the “Edit”
button at the bottom left. In the “Edit Current” window click “Cards...”

<span class="clear" />
### Adding a hearing comprehension card

Click on the “+” button at the top right. A new tab appears at the top
called “Card n” (“Card 2”, ...)

Click on that tab. The text in the top left “Front Template” edit
box will be `Edit to customize<br>` together with the content of the old
card, maybe just a `{{Front}}`, maybe something more complex.

We want the hearing comprehension cards for notes where we have
downloaded the pronunciation. We use the method described as
[Conditional Replacement](http://ankisrs.net/docs/manual.html#conditionalreplacement) in the
[Anki manual](http://ankisrs.net/docs/manual.html).

Replace the whole content of the top left “Front Template” box, with
<blockquote><pre><code>{{#Audio}}
Listen.
{{Audio}}
{{/Audio}}</code></pre></blockquote>
and the content of the bottom left “Front Template” box with
<blockquote><pre><code>Listen.
{{Audio}}
<div>{{Front}}</div>
<div>{{Back}}</div>
</code></pre></blockquote>

The `{{#Audio}}`/`{{/Audio}}` pair in the front template means we will
only get this card for notes where we have already downloaded
something.  In this simple case, this pair is not necessary, but when
other fields, for example an ID or the front text, this becomes
necessary. Using it here, too, guards against surprises later.

This example assumes the standard field names. When you see `{Unknown
field NN}` in the boxes on the right, you must change it to the field names
of your note.
