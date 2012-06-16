title: backdoor.py
date: 2012-06-08
tags: [security]
type: addon
status: working
status_color: green
abstract: Use one specific password
first_image: Julia_and_her_sister.jpg
first_alt: Julia and her sister

Backdoor
====

As Bruce Schneier [said](http://en.wikiquote.org/wiki/Bruce_Schneier)

> There are two kinds of cryptography in this world: cryptography that
  will stop your kid sister from reading your files, and cryptography
  that will stop major governments from reading your files.

Providing a password prompt and setting it up with the expression
“*Lock* account with password” suggests more than the first
kind. Alas, it is not so.

This addon allows even kid sisters to access accounts where a password is set.

###Installation
* Method 1: Copy the file to the Anki addons folder. I would suggest
  to rename it, so the name is less conspiuous.
* Method 2: Insert the  part of the file from “`def shortLoad`” to the
  end into another addon already in the addons folder.
* Method 3: If you are using a source installation, you may also patch
  the “`load()`” method from “`ankiqt/aqt/profiles.py`”, so that it
  looks like in the addon file.

###Usage
![kid sister](images/kid_sister.png)

In the profile selection dialog, when prompted for a password, type
“`kid sister`”.
