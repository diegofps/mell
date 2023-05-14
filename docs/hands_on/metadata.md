# The metadata syntax 📜

Mell uses json files to represent metadata. These files represent what we want to generate whereas the style folder represents how to render it. To create an example project, type the following.

```shell
mell --new metadata
cdd metadata
```

Now, consider the following metadata file representing a letter. It may be located in `<root>/meta/letter_basic.json`.

```json
{
    "to": "Juliana",
    "address": "juliana@gmail.com",
    "subject": "Notification",
    "opening": "Dear Ju,",
    "first_paragraph": "I hope you are doing well :)",
    "paragraphs": ["This is a standard message just to remind you to drink water.", "Did you drink water today?"],
    "last_paragraph": "I am always here for you.",
    "ending": "Your friend,",
    "signature": "Bot"
}
```

Currently, the only reserved word we have in a metadata file is `__parent__`. It allows us to generate a new metadata based on a previous one. It works similarly to inheritance in object oriented languages. The following example, located in `<root>/meta/letter_beach.json`, shows an extension to the previous metadata that customizes the attributes first_paragraph, paragraphs, and last_paragraph.

```json
{
    "__parent__": "letter_basic",
    "first_paragraph": "",
    "paragraphs": ["I checked the weather for this weekend and it will be great to go to the beach.", "Would you like me to invite a friend?"],
    "last_paragraph": ""
}
```

We will talk a little bit more about the template syntax in the next section, but given the following template file is saved in `<root>/style/template/letter.txt`.

```php
To: |= meta.to =| <|= meta.address =|>
Subject: |= meta.subject =|

|? if meta.opening ?|
|= meta.opening =|

|? endif ?|
|? if meta.first_paragraph ?|
|= meta.first_paragraph =|

|? endif ?|
|? for paragraph in meta.paragraphs ?|
|= paragraph =|

|? endfor ?|
|? if meta.last_paragraph ?|
|= meta.last_paragraph =|

|? endif ?|
|= meta.ending =|
|= meta.signature =|
```

We may generate a letter with the first content, or the second content depending on the metadata we use. For instance, if we run `mell letter_basic` inside `<root>` we will generate the following content in the file `<root>/generate/letter.txt`:

```
To: Juliana <juliana@gmail.com>
Subject: Notification

Dear Ju,

I hope you are doing well :)

This is a standard message just to remind you to drink water.

Did you drink water today?

I am always here for you.

Your friend,
Bot
```

Whereas `mell letter_beach` would generate the following:

```
To: Juliana <juliana@gmail.com>
Subject: Notification

Dear Ju,

I checked the weather for this weekend and it will be great to go to the beach.

Would you like me to invite a friend?

Your friend,
Bot
```

Alternatively, we could also drop the `__parent__` attribute from `letter_beach.json` and specify two `metadata` files during the command execution, separating their names with a comma. The syntax for this is show bellow.

```shell
# These two syntaxes have the same effect
mell letter_basic,letter_beach
mell letter_basic letter_beach
```

You may also inherit multiple base files in `__parent__`. If we add a third letter type, in `<root>/meta/letter_beach_night.json`, and we keep `letter_beach` without its `__parent__` attribute, the following syntax would combine both parent files.

```json
{
    "__parent__": "letter_basic,letter_beach",
    ...
}
```
