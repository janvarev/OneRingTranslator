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

### openrouter_chat

Translate by OpenRouter https://openrouter.ai/

Default options:
```python
"default_options": {
      "apiKey": "", #
      "apiBaseUrl": "https://openrouter.ai/api/v1",  #
      "system": "Please translate the user message from {0} to {1}. Make the translation sound as natural as possible. Don't use any non-related phrases in result, answer with only translation text.",
      "prompt": "{2}",
      "model": "",
  },
```
Description:
- "apiKey": "API-key OpenRouter", #
- "apiBaseUrl": "URL for OpenRouter",  #
- "system": "System input string."
- "prompt": prompt
- "model": model,

In `system` and `prompt` {0}, {1} and {2} will be replaced to: 
- en name of source lang
- en name of target lang
- text to translate


### multi_sources

Choose the best translation from results from several other plugins (sources). 
Uses COMET-no-reference neuronet model to find best result.

**Required:** `pip install unbabel-comet`

Options
```python
"default_options": {
    "model": "google_translate,deepl",  # plugins that will be processed
    "min_symbols_to_full_model": 30,
    "min_plugin": "google_translate", # if symbols less than min, this will be used
    "multithread_model": True, # use this if you use different plugins in model - this speedup by multithread tasks
},
```



### More plugins

Please, post your additional plugins here:
https://github.com/janvarev/OneRingTranslator/issues/1
