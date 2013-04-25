title: Backdoor
id: backdoor
main_file: Backdoor.py
type: addon
date: 2012-05-14
status: working
status_color: green
status_text_color: white
abstract: Use one specific password to access accounts “locked” with a password.
first_image: Julia_and_her_sister.jpg
first_caption: Julia and her sister
first_alt: "Two little girls sitting on a wooden staircase."

As Bruce Schneier [said](http://en.wikiquote.org/wiki/Bruce_Schneier)

> There are two kinds of cryptography in this world: cryptography that
  will stop your kid sister from reading your files, and cryptography
  that will stop major governments from reading your files.

Providing a password prompt and setting it up with the expression
“*Lock* account with password” suggests more than the first
kind. Alas, it is not so.

This add-on allows even kid sisters to access accounts where a password is set.

### Installation
* Method 1: Copy
  [the file](https://github.com/ospalh/anki-addons/blob/master/Backdoor.py)
  to the Anki add-ons folder. I would suggest to rename it, so the name
  is less conspicuous. You probably also want to remove the comment
  about Bruce Schneier.
* Method 2: Insert the  part of the file from “`def shortLoad`” to the
  end into another add-on already in the add-ons folder.
* Method 3: If you are using a source installation, you may also patch
  the “`load`”-method from
  “[`ankiqt/aqt/profiles.py`](https://github.com/dae/ankiqt/blob/master/aqt/profiles.py)”,
  so that it looks like “`shortLoad`” in the add-on file.

### Usage

<figure>
<img src="images/kid_sister.png" alt="Anki profile selection
dialog. List of users on the left, buttons on the right. At the bottom
a text input field labeled “Password:” with ten bullets. Bubble help
text “kid sister” pointing at it.">
<figcaption>The profile selection dialog. Type “kid sister”
here."</figcaption>
</figure>
In the profile selection dialog, when prompted for a password, type
“`kid sister`”.
