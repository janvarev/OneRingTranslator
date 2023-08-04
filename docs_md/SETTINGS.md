# Description and settings

## Translation-through-plugins logic

Different translation servers (Google Translate, DeepL, Libre, local FB NLLB translation) are supported through **plugins**. There are several in plugins folder. 

[Available plugins docs here](#plugins). You can setup the default plugin for translation by set `"default_translate_plugin"` option in `options/core.json` file after first run. 

You can adjust options after first fun in file `options/<plugin_name>.json`

Plugins are located in the `plugins` folder and must start with the "plugins_" prefix.

Plugin settings, if any, are located in the "options" folder (created after the first launch).

For developers: plugins supported throw [Jaa.py](https://github.com/janvarev/jaapy) - minimalistic one-file plugin engine. 
Check this project for details "how to dev your own plugin".

## Plugin support

Plugins supported throw [Jaa.py](https://github.com/janvarev/jaapy) - minimalistic one-file plugin engine.

Plugins are located in the plugins folder and must start with the "plugins_" prefix.

Plugin settings, if any, are located in the "options" folder (created after the first launch).

Examples can be found in `plugins` dir.

## Core options description (core.json)

Located in `options/core.json` after first run.

```python
{
    "default_translate_plugin": "google_translate", # default translation engine
    "default_from_lang": "es", # default from language
    "default_to_lang": "en", # default to language
    "api_keys_allowed": [], # set of API keys. If empty - no API key required.
    "debug_input_output": False, # allow debug print input and output in console
    "allow_multithread": True, # allow multithread run of translation engine
    "user_lang": "", # standart user language. Replaces "user" in to_lang or from_lang API params
    "cache_is_use": True, # use cache?
    "cache_save_every": 5,  # every X elements save cache to disk
 
},
```
