# WEB API for translation

Simple WEB API REST service for translation.

Features:
- **Plugin support**. If you misses some translation engine, you can add it yourself! 
- **Full offline translation (optionally).** You can setup your own offlie https://github.com/LibreTranslate/LibreTranslate service and target this service to use it as endpoint.
- **Ready to use**. By default use Google Translate service, and ready to use.
- Simple REST interface throw FastApi and openapi.json interface. After install go to `http://127.0.0.1:4990/docs` to see examples.
- **API keys**. (Disabled by default) You can restrict access to your service by set up a list of API keys, needed to access the service. 

## One-click installer for Windows

Go here: https://github.com/janvarev/OneRingTranslator-installer and follow instructions.

## Install and run

To run: 
1. Install requirements ```pip install -r requirements.txt```
2. Run run_webapi.py.

Docs and test run: `http://127.0.0.1:4990/docs`

## Plugins

By default, two plugins provided
- **google_translate** (no options)
- **libre_translate** (custom_url option. If you want, setup your https://github.com/LibreTranslate/LibreTranslate server locally, and target custom_url to gain translation from your server)

Please, post your additional plugins here:
https://github.com/janvarev/OneRingTranslator/issues/1

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
    "allow_multithread": True # allow multithread run of translation engine 
},
```