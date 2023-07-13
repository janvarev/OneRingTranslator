# WEB API for translation

Simple WEB API REST service for translation.

Features:
- **Plugin support**. If you misses some translation engine, you can add it yourself! 
- **Full offline translation (optionally).** You can setup your own offline https://github.com/LibreTranslate/LibreTranslate service and target this service to use it as endpoint. Or use effective FB NLLB neuronet.
- **Ready to use**. By default use Google Translate service, and ready to use.
- Simple REST interface throw FastApi and openapi.json interface. After install go to `http://127.0.0.1:4990/docs` to see examples.
- **API keys**. (Disabled by default) You can restrict access to your service by set up a list of API keys, needed to access the service.
- **Cache translations** (if necessary)
- **Automatic BLEU and COMET estimation of translation quality** 
  - If you want to test different plugins translation quality on your pair of languages - you can do it! (Supported over 100 languages from FLORES dataset)
  - If you have your own plugin - you can compare it with others!  

## Known supported translators

- Google Translate (online, free)
- Deepl Translate (online, require API key)
  - [Alt version](https://github.com/janvarev/onering_plugins_chrome_dev) that doesn't require API key 
- Libre Translate (online or offline)
- FB NLLB neuronet (offline)
  - Also support [CTranslate2](https://opennmt.net/CTranslate2/index.html) realization of neuronet
- FB MBart50 (imho worser then NLLB) 
- KoboldAPI endpoint (offline mostly due to target localhost)
  - KoboldAPI is a REST interface for lots of LLM servers (like [koboldcpp](https://github.com/LostRuins/koboldcpp/releases), [text-generation-webui](https://github.com/oobabooga/text-generation-webui))
  - If you load some LLM model inside this LLM server, you can translate texts using them!
  - (Now plugin uses Alpaca template to set translation task. Change it if you want)
- OpenAI Chat interface (ChatGPT), (online or offline emulation)
  - API key required, if you want to connect to OpenAI servers
  - Otherwise, you can connect through this interface to local OpenAI emulation servers.
- Yandex translation ([through browser manipulation](https://github.com/janvarev/onering_plugins_chrome_dev))
- No Translate (offline) - dummy translator to compare with

## Known usages

- https://github.com/HIllya51/LunaTranslator - automatic game translation tool
- https://github.com/janvarev/multi_translate - oobabooga/text-generation-webui plugin for translate conversation with LLM (Large Language Models) UserLanguage<->English
- https://github.com/janvarev/privateGPT - privateGPT multilanguage fork

## Installation and run

### Install 
- If you're on Windows, you can use **fast one click installer**: Go here: https://github.com/janvarev/OneRingTranslator-installer and follow instructions.
  - If you **plan to use offline translation plugins**, please choose B on install query and install "torch" packet.  
- If you're on other system   
  - Install python 3.10.x (if needed)
  - Install requirements by cmd ```pip install -r requirements.txt```
  - If you plan to use offline translation ```pip install -r requirements-offline.txt```

### Run
- If you've used one click installer for Windows just run `start-webapi.bat`
- If you are on other system, run `run_webapi.py`

### Fast configuration for online translation

If you're ok to use **online** translation:

**Congratulations, you're done!** By default OneRingTranslator just transfer your calls to Google Translate. 

Visit docs and simple Web interface: http://127.0.0.1:4990/

### Fast configuration for offline translation

If you plan to use **offline** translation:
- Run webapi at least one time.
- Open file `options/core.json`
- Set `"default_translate_plugin": "fb_nllb_translate"`, and save file 
- Run. During the first run neuronet model will be downloaded from huggingface hub, it takes time

- **You're done!**

Visit docs and simple Web interface: http://127.0.0.1:4990/

## Translation-through-plugins logic

Different translation servers (Google Translate, DeepL, Libre, local FB NLLB translation) are supported through **plugins**. There are several in plugins folder. 

[Available plugins docs here](#plugins). You can setup the default plugin for translation by set `"default_translate_plugin"` option in `options/core.json` file after first run. 

You can adjust options after first fun in file `options/<plugin_name>.json`

Plugins are located in the `plugins` folder and must start with the "plugins_" prefix.

Plugin settings, if any, are located in the "options" folder (created after the first launch).

For developers: plugins supported throw [Jaa.py](https://github.com/janvarev/jaapy) - minimalistic one-file plugin engine. 
Check this project for details "how to dev your own plugin".

## Average BLEU and COMET results for translation quality

BLEU (bilingual evaluation understudy) is an automatic algorithm for evaluating the quality of text which has been machine-translated from one natural language to another.

Use this results just for reference.

BLEU scores (higher is better, no_translate can be used as baseline. Average on 100 examples from FLORES, offset = 150):

|                                                                |   fra->eng |   eng->fra |   rus->eng |   eng->rus |
|----------------------------------------------------------------|------------|------------|------------|------------|
| no_translate                                                   |       3.98 |       3.9  |       0.57 |       0.56 |
| libre_translate                                                |      47.66 |      49.62 |      32.43 |      30.99 |
| fb_nllb_translate nllb-200-distilled-600M                      |      51.92 |      52.73 |      41.38 |      31.41 |
| fb_nllb_translate nllb-200-distilled-1.3B                      |      56.81 |       55   |      46.03 |      33.98 |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16     |      54.87 |      56.73 |      48.45 |      36.85 |
| fb_nllb_ctranslate2 JustFr-ik/nllb-200-distilled-1.3B-ct2-int8 |      56.12 |      56.45 |      46.07 |      34.56 |
| google_translate                                               |      58.08 |      59.99 |      47.7  |      37.98 |
| deepl_translate                                                |      57.67 |      59.93 |      50.09 |      38.91 |
| yandex_dev                                                     |      ----- |      ----- |      46.09 |      40.23 |
| openai_chat gpt-3.5-turbo (aka ChatGPT)                        |      ----- |      ----- |      41.49 |      30.9  |
| koboldapi_translate (alpaca7B-4bit)                            |      43.51 |      30.54 |      32    |      14.19 |
| koboldapi_translate (alpaca30B-4bit)                           |      ----- |      ----- |      ----- |      24.0  |
| fb_mbart50  facebook/mbart-large-50-one-to-many-mmt            |      ----- |      48.79 |      ----- |      28.55 |
| fb_mbart50  facebook/mbart-large-50-many-to-many-mmt           |      50.26 |      48.93 |      42.47 |      28.56 |

Average BLEU results with different LLMs:

|                                            |   rus->eng |   eng->rus |
|--------------------------------------------|------------|------------|
| no_translate                               |       0.57 |       0.56 |
| libre_translate                            |      32.43 |      30.99 |
| koboldapi_translate (alpaca7B-4bit)        |      32    |      14.19 |
| koboldapi_translate (alpaca30B-4bit)       |      -     |      24.0  |
| openai_chat gpt-3.5-turbo (aka ChatGPT)    |      41.49 |      30.9  |

'koboldapi_translate' on 'eng->rus' pair average BLEU score:     7.00: 80/100
on IlyaGusev-saiga_7b_lora_llamacpp-ggml-model-q4_1.bin, may be adjusting for input prompt needed

COMET scores (higher is better, no_translate2 can be used as baseline. Average on 100 examples from FLORES, offset = 150):

|                                                                |   fra->eng |   eng->fra |   rus->eng |   eng->rus |
|----------------------------------------------------------------|------------|------------|------------|------------|
| no_translate2                                                  |      31.66 |      32.06 |      33.03 |      25.58 |
| libre_translate                                                |      86.66 |      82.36 |      80.36 |      83.34 |
| fb_nllb_translate nllb-200-distilled-1.3B                      |      89.01 |      87.95 |      86.91 |      88.57 |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16     |      ----- |      ----- |      87.29 |      88.79 |
| google_translate                                               |      89.67 |      88.9  |      87.53 |      89.63 |
| deepl_translate                                                |      ----- |      ----- |      87.77 |      89.73 |
| yandex_dev                                                     |      ----- |      ----- |      87.34 |      90.27 |
| multi_sources google_translate,deepl_translate,yandex_dev      |      ----- |      ----- |      87.74 |      90.63 |


**IMPORTANT:** You interested how it will work on YOUR language pairs? It's easy, script already included, see "Automatic BLEU measurement" chapter.

## Plugins

### google_translate

Used by default. 

Options: no

Translate with Google Translate.

### deepl_translate

Translate via Deepl. API key required. 

```python
"options": {
    "api_key": "",  #
    "is_free_api": True, # use Free version or not
},
```

### libre_translate

Libre Translate service

Options:
- `custom_url` If you want, setup your https://github.com/LibreTranslate/LibreTranslate server locally, and target custom_url to gain translation from your server)

### fb_nllb_translate

Translate by neuronet from https://github.com/facebookresearch/fairseq/tree/nllb

Options
- `model` define model to use 
- `cuda"`: -1, # -1 if you want run on CPU, 0 - if on CUDA

Details:
- You need to install transfomers and torch to use this.
- This will use original BCP 47 Code to target language: https://github.com/facebookresearch/flores/blob/main/toxicity/README.md
Plugin try to recognize 2-language-codes to transform them to BCP 47 Code, but better will be pass them manually (by from_lang, to_lang params)  

### fb_nllb_ctranslate2

Translate by NLLB neuronet with [CTranslate2](https://opennmt.net/CTranslate2/index.html) support.

CTranslate2 allow you to use quantization (fp16 and int8) to speed up and lower GPU memory req.

This plugin require some preparations:
- You need specially prepared NLLB models (converted with CTranslate2). I found some of them here: https://huggingface.co/JustFrederik
- You need download them MANUALLY, and place in some folder under OneRingTranslator installation, and set model to path to this folder. 
Models will not download automatically.

Options
- `model` define model to use 
- `cuda"`: -1, # -1 if you want run on CPU, 0 - if on CUDA

### fb_mbart50

Realize mBART-50 network from here: https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt

IMHO just worser in translation than FB NLLB.

Options
- `model` define model to use 
- `cuda"`: -1, # -1 if you want run on CPU, 0 - if on CUDA


### no_translate

Dummy plugins that just return original text. 

Options: no

### no_translate2

Dummy plugins that just return blank text (good for COMET eval). 

Options: no

### koboldapi_translate

Translate by sending prompt to LLM throw KoboldAPI (REST) interface. 

Options:
- `custom_url` Kobold API endpoint
- `prompt`: prompt template. Default is Alpaca-style: "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n### Instruction:\nTranslate this text from {0} to {1}:\n\n{2}\n\n\n### Response:"

KoboldAPI is a REST interface for lots of LLM servers (like [koboldcpp](https://github.com/LostRuins/koboldcpp/releases), [text-generation-webui](https://github.com/oobabooga/text-generation-webui))

If you load some LLM model inside this LLM server, you can translate texts using them!

(Now plugin uses Alpaca template to set translation task. Change it if you want)

In `prompt` {0}, {1} and {2} will be replaced to: 
- en name of source lang
- en name of target lang
- text to translate

### openai_chat

Translate by OpenAI Chat interface

Default options:
- "apiKey": "", #
- "apiBaseUrl": "",  #
- "system": "You are a professional translator."
- "prompt": "Instruction: Translate this text from {0} to {1}:\n\n{2}"

Description:
- "apiKey": "API-key OpenAI", #
- "apiBaseUrl": "URL for OpenAI (allow OpenAI emulation servers)",  #
- "system": "System input string."

In `system` and `prompt` {0}, {1} and {2} will be replaced to: 
- en name of source lang
- en name of target lang
- text to translate

### multi_sources

Plugins, that choose best translation from results from several other plugins (sources). 
Uses COMET-no-reference neuronet model to find best result.

Options
- `plugins` list of plugins to get translations  

### More plugins

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
    "cache_is_use": True, # use cache?
    "cache_save_every": 5,  # every X elements save cache to disk
 
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

## Automatic BLEU estimation

There are builded package to run BLEU estimation of plugin translation on different languages.

There are pretty simple estimation based on FLORES dataset: https://huggingface.co/datasets/gsarti/flores_101/viewer

To estimate:
1. install requirements-bleu.txt
2. setup params in run_estimate_bleu.py (at beginning of file)
3. run run_estimate_bleu.py

RECOMMENDATIONS: 
1. debug separate plugins first!
2. To debug, use less BLEU_NUM_PHRASES.

Settings params:
```python
# ----------------- key settings params ----------------
BLEU_PAIRS = "fra->eng,eng->fra,rus->eng,eng->rus" # pairs of language in terms of FLORES dataset https://huggingface.co/datasets/gsarti/flores_101/viewer
BLEU_PAIRS_2LETTERS = "fr->en,en->fr,ru->en,en->ru" # pairs of language codes that will be passed to plugin (from_lang, to_lang params)

BLEU_PLUGINS = "no_translate,google_translate" # plugins to estimate, separated by ,

BLEU_NUM_PHRASES = 100 # num of phrases to estimate. Between 1 and 100 for now.
BLEU_START_PHRASE = 150 # offset from FLORES dataset to get NUM phrases

BLEU_METRIC = "bleu" # bleu | comet
```

## Thanks to

https://github.com/jenil/chota Chota project for awesome CSS
