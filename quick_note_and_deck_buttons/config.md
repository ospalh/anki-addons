#### general

The buttons you see to quickly change 

- ... the note type are defined by "model_button_rows"
- ... the deck are defined by "deck_button_rows"

#### Details

- `model_button_rows` and `deck_button_rows` each contain a list of lists. Each nested list represents one row.
- The buttons in each row are defined by a list of dictionaries.
- Each dictionary must contain:
    - label: the text of the button
    - name:  the name of the note or deck to change to. The deck is created if it doesn’t
      exist already.
    - shortcut (optional): the shortcut key
- Closely follow the examples. Use the correct symbols like brackets, curly braces, etc.
- The examples from this readme might not be shown properly in the config window of Anki. To see the examples with proper 
  line breaks have a look at the site on AnkiWeb or on Github.

#### example with one row 

```
{
    "model_button_rows": [
        [
            {
                "label": "C",
                "shortcut": "Ctrl+1",
                "name": "Cloze"
            },
            {
                "label": "B",
                "shortcut": "Ctrl+2",
                "name": "Basic"
            }
        ]
    ],
    "deck_button_rows": [
        [
            {
                "label": "Deck1",
                "name": "Deck1"
            },
            {
                "label": "my subdeck",
                "name": "Deck1::my subdeck"
            }
        ]
    ]
}
```

#### example with two rows 

```
{
    "model_button_rows": [
        [
            {
                "label": "C",
                "shortcut": "Ctrl+1",
                "name": "Cloze"
            },
            {
                "label": "B",
                "shortcut": "Ctrl+2",
                "name": "Basic"
            }
        ],
        [
            {
                "label": "with reverse",
                "shortcut": "Ctrl+3",
                "name": "Basic (and reversed card)"
            }
        ]
    ],
    "deck_button_rows": [
        [
            {
                "label": "Deck1",
                "name": "Deck1"
            },
            {
                "label": "my subdeck",
                "name": "Deck1::my subdeck"
            }
        ],
        [
            {
                "label": "Deck 2",
                "name": "Deck 2"
            }
        ]
    ]
}
```

