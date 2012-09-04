title: Local CSS
subtitle: Adapt card styles to time and place
id: localcss
main_file: local CSS.py
status: working
type: addon
status_color: green
status_text_color: white
abstract: Add styling from a local CSS file. With this, the card style can be adapted to time (night colors) and place (small fonts on small screens, big fonts on big screens, ...).
first_image: three_styles.png
first_alt: The same card with different styles
ankiweb_id: 2587372325

This loads the local CSS file `user_style.css` and adds the style to the CSS set in the card templates.

It also adds a few classes to the cards.


With this, the look of the cards can be adapted to the time of day
(night colors) and place (small fonts on small screens, big fonts on
big screens, ...)

## Set-up

The add-on loads the file `user_style.css` from the current profile’s
directory, typically `Anki/User 1` or `Anki\User 1`.

Typically the standard styling in the card template isn’t
changed. Like this, reviewing on AnkiWeb and on mobile devices works
as before.

### Classes 

The add-on adds the classes `loc` to all cards. The model and template
names of each card are reduced to the characters `a` to `z`, `A` to `Z`, `0` to `9`
and `_` and added as classes as well, in the form of `model_NN` and
`template_NN`. As an example, the second card (`card1`) of a model or
note type called “Satz Japanese 日本語” and that is called “Hörübung”
would have the css classes `card card1 model_SatzJapanese
template_Hrbung`. These classes can be used to build CSS selectors.

### Standard use

To apply a style to the whole card only on a specific computer, use the
`user_sytle.css` file on that computer. You should use the CSS selector
`.loc.card`. The example in the bottom of the image was done with 
<blockquote><pre><code>.loc.card{ 
    font-family: Linux Biolinum O;
    background-color: #ededff;
    font-size: 58px;}</code></pre></blockquote>

<blockquote class=nb> The selector in the style file must be more
specific than the one used in the template in the collection. When a
setup for <tt>.card</tt> is used in the template, the style file should use
<tt>.loc.card</tt>, not just <tt>.loc</tt> </blockquote>


### Sub-elements

The easiest way to select only parts of a card is to add classes with
the `<div>` or `<span>` elements. For example a
Japanese answer can be written as `<div class="nihongo">{{furigana:Japanese}}</div>` in the back template of a card.

Then, different Japanese fonts can be selected on different computers
by using <tt>.loc .nihongo{font-family: [IPAPMincho](http://ossipedia.ipa.go.jp/ipafont/index.html);}</tt> in one style file
and <tt>.loc .nihongo{font-family: "[Moon font](http://cooltext.com/Download-Font-%E6%9C%88+Moon)";}</tt> in another.

<blockquote class=nb>
As the <tt>loc</tt> and <tt>card</tt> apply to the same object, the selector
<tt>.loc.card</tt> contains <em>no</em> space. When setting the style for a
sub-element, a space <em>must</em> be added. For example, to change the style of the
Japanese text, use <tt>.loc .nihongo</tt> with a space between
the <tt>c</tt> and the <tt>.</tt>.
</blockquote>


## Different cards

Applying different styles to different cards works in a similar way.

As an example, i use a standard style of black on light blue for
standard cards and black ond light red for grammar cards. In the
alternative style i use light colored text on dark background, dark
green for normal cards and dark red for grammar cards. The standard
cards use the the `.loc.card` selector described above. The model name
of the grammar cards is “Grammatik VHS — Japanese” and so i use
<blockquote><pre><code>.loc.card.model_grammatikvhsjapanese{
    background-color: #64354c;
    color: #d9b7ce;}</code></pre></blockquote>
to set up the pink-on-dark-red.


## Night and day

To use different styles at different times, for example a
black-on-white scheme during the day and a light-on-dark scheme in the
evening, simply have two style files like `day_user_style.css` and
`night_user_style.css` handy and replace the file `user_style.css`
with the fitting one. On file systems that support them (i.e. basically
anywhere but on Windows systems), soft links can be used instead: `ln
-sf day_user_style.css user_style.css`.

### Reloading

The user style is loaded when the profile is opend. To reload the
style afer a change go to the “Switch Profiles” dialog and re-open the
profile.
