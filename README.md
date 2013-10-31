anki-replaceall
===============

Experimental anki add-on which fills an expression into a given field of all notes in an Anki model.

Disclaimer: Only use this add-on if you know exactly what you are doing! It may irreversibly alter a large number of notes in your collection!

Motivation
----------

As per the [Anki documentation](http://ankisrs.net/docs/manual.html#_media_amp_latex_references), media references to fields in a template (such as `[sound:{{Word}}]`) are not officially supported, and will generally not play in mobile clients like [AnkiDroid](https://code.google.com/p/ankidroid/).

However, sometimes it's convenient to use a naming convention for media files based on the content of other fields. For example we might have a model with a field `Expression`, and we want to have a corresponding audio file using the naming convention `{{Expression}}.mp3`. 

If our model is only used by three notes, with values for `Expression` ("Dog", "Cat", "Mouse"), and a field for the audio file `Audio`, then it would not be much work to just manually write the following values to the `Audio` field ("[sound:Dog.mp3]","[sound:Cat.mp3]","[sound:Mouse.mp3]") which would allow us to include the media in our flash cards.

However, if our model is used by hundreds or thousands of notes, this would be very laborious. It would be much more convenient to have a "replaceall" feature which automatically writes `[sound:{{Expression}}.mp3]` to the `Audio` field of all notes of a given model in our collection. This is exactly what this plugin does.

Usage
-----

**Note: before using this plugin, it is highly recommended that you sync with AnkiWeb, and also make a physical backup of your collection.anki2 file.**

To use the plugin, simply copy the file `replaceall.py` to the addons folder in the Anki directory of your PC, restart Anki, and a new item will appear in the Tools menu called "Replace All". Choose the model, destination field (e.g. the `Audio` field in above example), and optionally a tag which you want to limit the replacement to, then finally enter an expression such as `[sound:{{Expression}}.mp3]` which will be rendered and added to the destination field for all matching notes upon pressing the "Replace All" button.
