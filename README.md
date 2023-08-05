# WEB API for translation

Simple WEB API REST service for translation.

Features:
- **Plugin support**. If you misses some translation engine, you can add it yourself! 
- **Full offline translation (optionally).** You can setup your own offline https://github.com/LibreTranslate/LibreTranslate service and target this service to use it as endpoint. Or use effective FB NLLB neuronet.
- **Ready to use**. By default use Google Translate service, and ready to use.
- **Simple REST API interface** throw FastApi and openapi.json interface. After install go to `http://127.0.0.1:4990/docs` to see examples.
- **API keys**. (Disabled by default) You can restrict access to your service by set up a list of API keys, needed to access the service.
- **Cache translations** (if necessary)
- **Automatic BLEU and COMET estimation of translation quality** 
  - If you want to test different plugins translation quality on your pair of languages - you can do it! (Supported over 100 languages from FLORES dataset)
  - If you have your own plugin - you can compare it with others!  
- **Unique World Best results by multi_sources plugin!**
  - We have a plugin that gains translations from multiple sources, then estimate them and return only the best
  - It gains the best COMET translation evaluation score against other plugins.
- **Translation routing** Use different translation engines on different language pairs.

## Links

- [Supported translators](#known-supported-translators)
- [Known OneRingTranslator usages](#known-usages)
- **[Install and run](/docs_md/INSTALL.md)**
- [Base settings and plugin logic](/docs_md/SETTINGS.md)
- [Plugins options](/docs_md/PLUGINS.md)
- [REST API usage examples](/docs_md/API.md)
- **[Rating plugins translation quality (BLEU, COMET)](/docs_md/ESTIMATIONS.md)** 
Use it to choose what plugin you want to run for your own translation task. Also you can do your own measures with script here.   


## Known supported translators

### Online

- Google Translate (free)
- Deepl Translate (require API key)
  - [Alt version](https://github.com/janvarev/onering_plugins_chrome_dev) that doesn't require API key 
- Libre Translate (online free, but slow)
- OpenAI Chat interface (ChatGPT, GPT-4), (online or offline emulation)
  - API key required, if you want to connect to OpenAI servers
  - Otherwise, you can connect through this interface to local OpenAI emulation servers.
- Yandex translation ([through browser manipulation](https://github.com/janvarev/onering_plugins_chrome_dev))
- [Lingvanex](https://lingvanex.com/)
- Translation via [OpenRouter](https://openrouter.ai/) LLM online models (require API key):
  - ChatGPT
  - GPT-4
  - Claude Instant v1
  - Claude v1
  - Claude v2
  - Google: PaLM 2 Bison
  - TII: Falcon 40B Instruct

### Offline

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
- No Translate (offline) - dummy translator to compare with
- Opus MT

### Synthetic 

- multi_source - get translations from other plugins, and choose the best one
- use_mid_lang - translate with other plugins by chaining translating to middle-language, usually English (FromLang->En->ToLang)

## Known usages

- https://github.com/HIllya51/LunaTranslator - automatic game translation tool
- https://github.com/janvarev/multi_translate - oobabooga/text-generation-webui plugin for translate conversation with LLM (Large Language Models) UserLanguage<->English
- https://github.com/janvarev/privateGPT - privateGPT multilanguage fork




## Thanks to

https://github.com/jenil/chota Chota project for awesome CSS
