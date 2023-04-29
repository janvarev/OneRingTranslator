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
    "allow_multithread": True, # allow multithread run of translation engine
    "user_lang": "", # standart user language. Replaces "user" in to_lang or from_lang API params 
},
```

## API example usage

Translate from en to fr
```
http://127.0.0.1:4990/translate?text=Hi%21&from_lang=en&to_lang=fr
```

Translate from en to user language (user language defines in plugins/core.json)
```
http://127.0.0.1:4990/translate?text=Hi%21&from_lang=en&to_lang=user
```

Full Python usage example:
```python
custom_url = params['custom_url']
if custom_url == "":
    res = "Please, setup custom_url for OneRingTranslator (usually http://127.0.0.1:4990/)"
else:
    import requests
    response_orig = requests.get(f"{custom_url}translate", params={"text":string,"from_lang":from_lang,"to_lang":to_lang})
    if response_orig.status_code == 200:
        response = response_orig.json()
        #print("OneRingTranslator result:",response)

        if response.get("error") is not None:
            print(response)
            res = "ERROR: "+response.get("error")
        elif response.get("result") is not None:
            res = response.get("result")
        else:
            print(response)
            res = "Unknown result from OneRingTranslator"
    elif response_orig.status_code == 404:
        res = "404 error: can't find endpoint"
    elif response_orig.status_code == 500:
        res = "500 error: OneRingTranslator server error"
    else:
        res = f"{response_orig.status_code} error"
```
