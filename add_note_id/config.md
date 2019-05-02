Three things can be configured:

* 'NoteIdFieldName': The name you picked for the first field. The standard “Note ID” has worked well for me.
* 'ShowMenu': Whether the menu item should appear. Once you have added the note id to your old cards, you don’t really need the “Add note id” item cluttering up the menu. Change this value to “false” then.
* 'ShowFullNoteId': Whether the full note id should be displayed. By default the value 15e11 will be subtracted from the note id. The note id is basically Unix epoch in seconds, so subtracting this value is safe. However you might still want the full value. Change this value to “true” then.
