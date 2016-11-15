title: Backdoor
main_file: backdoor.py
layout: addon
date: 2013-05-07
status: working
status_color: green
status_text_color: white
abstract: Use one specific password to access accounts <q>locked</q> with a password.
first_image: Julia_and_her_sister.jpg
first_caption: Julia and her sister
first_alt: "Two little girls sitting on a wooden staircase."

As Bruce Schneier [said](http://en.wikiquote.org/wiki/Bruce_Schneier)

> There are two kinds of cryptography in this world: cryptography that
  will stop your kid sister from reading your files, and cryptography
  that will stop major governments from reading your files.

Providing a password prompt and setting it up with the expression
<q>*Lock* account with password</q> suggests more than the first
kind. Alas, it is not so.

This add-on allows even kid sisters to access accounts where a password is set.

### Installation
* Method 1: Copy
  [the file](https://github.com/ospalh/anki-addons/blob/master/backdoor.py)
  to the Anki add-ons folder. I would suggest to rename it, so the name
  is less conspicuous. You probably also want to remove the comment
  about Bruce Schneier.
* Method 2: Insert the  part of the file from <q>`def shortLoad`</q> to the
  end into another add-on already in the add-ons folder.
* Method 3: If you are using a source installation, you may also patch
  the <q>`load`</q>-method from
  <q>[`ankiqt/aqt/profiles.py`](https://github.com/dae/anki/blob/master/aqt/profiles.py)</q>,
  so that it looks like <q>`shortLoad`</q> in the add-on file.

### Usage

<figure>
<img src="images/kid_sister.png" alt="The password input line at the
bottom is marked.">
<figcaption>The profile selection dialog. Type <q>kid sister</q>
here.</figcaption>
</figure>
In the profile selection dialog, when prompted for a password, type
<q>`kid sister`</q>.
