## Average results for translation quality

**BLEU (bilingual evaluation understudy)** is an automatic algorithm for evaluating the quality of text which has been machine-translated from one natural language to another.

**COMET** is also an automatic algorithm for evaluating the quality of translated text, based on neuronets.

**From author**: BLEU was introduced in 2002, and COMET in 2020. As for now, I recommend COMET scores more than BLEU. 

Use this results just for reference.

### BLEU scores 

Higher is better, no_translate can be used as baseline. Average on 100 examples from FLORES, offset = 150:

|                                                                |   fra->eng |   eng->fra |   rus->eng |   eng->rus |
|----------------------------------------------------------------|------------|------------|------------|------------|
| no_translate                                                   |       3.98 |       3.9  |       0.57 |       0.56 |
| libre_translate                                                |      47.66 |      49.62 |      32.43 |      30.99 |
| fb_nllb_translate nllb-200-distilled-600M                      |      51.92 |      52.73 |      41.38 |      31.41 |
| fb_nllb_translate nllb-200-distilled-1.3B                      |      56.81 |       55   |      46.03 |      33.98 |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16     |      54.87 |      56.73 |      48.45 |      36.85 |
| fb_nllb_ctranslate2 JustFr-ik/nllb-200-distilled-1.3B-ct2-int8 |      56.12 |      56.45 |      46.07 |      34.56 |
| google_translate                                               |      58.08 |      59.99 |      47.7  |      37.98 |
| deepl_translate                                                |      57.67 |      59.93 |  **50.09** |      38.91 |
| yandex_dev                                                     |      ----- |      ----- |      46.09 |  **40.23** |
| openai_chat gpt-3.5-turbo (aka ChatGPT)                        |      ----- |      ----- |      41.49 |      30.9  |
| koboldapi_translate (alpaca7B-4bit)                            |      43.51 |      30.54 |      32    |      14.19 |
| koboldapi_translate (alpaca30B-4bit)                           |      ----- |      ----- |      ----- |      24.0  |
| fb_mbart50  facebook/mbart-large-50-one-to-many-mmt            |      ----- |      48.79 |      ----- |      28.55 |
| fb_mbart50  facebook/mbart-large-50-many-to-many-mmt           |      50.26 |      48.93 |      42.47 |      28.56 |
| vsegpt_chat openai/gpt-3.5-turbo                               |      ----- |      ----- |      41.93 |      31.12 |
| vsegpt_chat openai/gpt-4                                       |      ----- |      ----- |      44.16 |      34.88 |
| vsegpt_chat anthropic/claude-instant-v1                        |      ----- |      ----- |      41.88 |      29.67 |
| vsegpt_chat anthropic/claude-2                                 |      54.91 |      56.09 |      46.38 |      34.13 |
| opus_mt Helsinki-NLP/opus-mt-en-ru                             |      ----- |      ----- |      ----- |      30.41 |


**LLMs with errors:**

- vsegpt_chat tiiuae/falcon-40b-instruct - a lot of fails
- vsegpt_chat google/palm-2-chat-bison - "I'm not able to help with that, as I'm only a language model."
- 'koboldapi_translate' on 'eng->rus' pair average BLEU score:     7.00: 80/100
on IlyaGusev-saiga_7b_lora_llamacpp-ggml-model-q4_1.bin, may be adjusting for input prompt needed

### COMET scores  

SOTA for opensource realization: 
- multi_sources vsegpt_chat:lizpreciatior/lzlv-70b-fp16-hf,fb_nllb_ctranslate2 - this comparable to DeepL and Google Translate (realistic)
- vsegpt_chat nvidia/nemotron-4-340b-instruct - this require a LOT OF computational resources

Higher is better, no_translate2 can be used as baseline. Average on 100 examples from FLORES, offset = 150:

|                                                                              |   fra->eng |   eng->fra |   rus->eng | eng->rus  |
|------------------------------------------------------------------------------|------------|------------|------------|-----------|
| no_translate2                                                                |      31.66 |      32.06 |      33.03 | 25.58     |
| no_translate                                                                 |      79.2  |      70.19 |       69.3 | 44.82     |
| opus_mt Helsinki-NLP/opus-mt-en-ru                                           |      ----- |      ----- |      ----- | 82.22     |
| libre_translate                                                              |      86.66 |      82.36 |      80.36 | 83.34     |
| lingvanex                                                                    |      87.92 |      86.99 |      84.75 | 86.3      |
| bloomz bigscience/bloomz-1b7                                                 |      87.86 |       84.1 |      ----- | -----     |
| vsegpt_chat recursal/eagle-7b                                                |      87.18 |      83.67 |      84.56 | 75.94     |
| koboldapi_translate NikolayKozloff/ALMA-13B-GGUF                             |      ----- |      ----- |      84.64 | 87.92     |
| t5_mt utrobinmv/t5_translate_en_ru_zh_large_1024                             |      ----- |      ----- |      86.05 | 86.53     |
| fb_nllb_translate nllb-200-distilled-1.3B                                    |      89.01 |      87.95 |      86.91 | 88.57     |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16                   |      88.74 |      88.32 |      87.25 | 88.83     |
| vsegpt_chat mistralai/mixtral-8x7b-instruct                                  |      88.45 |       87.2 |      86.94 | 87.85     |
| vsegpt_chat mistralai/mistral-small-24b-instruct-2501                        |       89.1 |      88.81 |      87.28 |      88.83|
| vsegpt_chat lizpreciatior/lzlv-70b-fp16-hf                                   |      88.69 |      87.17 |      86.91 | 88.15     |
| multi_sources vsegpt_chat:lizpreciatior/lzlv-70b-fp16-hf,fb_nllb_ctranslate2 |      89.14 |      88.22 |      87.22 | 89.87     |
| vsegpt_chat OMF-R-Vikhr-Nemo-12B-Instruct-R-21-09-24                         |      ----- |      ----- |      ----- |      87.93|
| google_translate                                                             |  **89.69** |      88.9  |      87.53 | 89.63     |
| deepl                                                                        |      89.39 |      89.27 |  **87.93** | 89.82     |
| vsegpt_chat google/gemma-2-27b-it                                            |      ----- |      ----- |      ----- |      89.07|
| vsegpt_chat google/gemma-2-9b-it                                             |      ----- |      ----- |      ----- |      88.32|
| vsegpt_chat meta-llama/llama-3.1-405b-instruct                               |      ----- |      ----- |      ----- |      89.72|
| vsegpt_chat meta-llama/llama-3.1-70b-instruct                                |      ----- |      ----- |      ----- |      89.93|
| vsegpt_chat meta-llama/llama-3.1-8b-instruct                                 |      ----- |      ----- |      ----- |      86.98|
| vsegpt_chat meta-llama/llama-3-70b-instruct                                  |      ----- |      ----- |      ----- |      88.84|
| vsegpt_chat meta-llama/llama-3.3-70b-instruct                                |      ----- |      ----- |      ----- | 89.69     |
| vsegpt_chat google/deepseek/deepseek-chat v3                                 |      ----- |      ----- |      ----- | 90.22     |
| multi_sources google_translate,vsegpt_chat:meta-llama/llama-3.1-70b-instruct |      ----- |      ----- |      ----- |      90.35|
| vsegpt_chat openai/gpt-4o-mini                                               |      89.38 |      88.45 |      87.31 |      89.55|
| vsegpt_chat cot_openai/gpt-4o-mini                                           |      ----- |      ----- |      ----- |      88.93|
| vsegpt_chat anthropic/claude-instant-v1                                      |      ----- |      ----- |      85.73 | 88.13     |
| vsegpt_chat openai/gpt-3.5-turbo                                             |      ----- |      ----- |      86.87 | 88.76     |
| vsegpt_chat openai/gpt-3.5-turbo-instruct                                    |      ----- |      ----- | 85.23      | 87.46     |
| vsegpt_chat openai/gpt-4                                                     |      ----- |      ----- |      87.02 | 89.54     |
| vsegpt_chat openai/gpt-4-1106-preview                                        |      ----- |      ----- |      ----- | 89.85     |
| vsegpt_chat openai/gpt-4-turbo                                               |      ----- |      ----- |      ----- | 89.76     |
| vsegpt_chat openai/gpt-4o                                                    |      ----- |      ----- |      ----- | 90.06     |
| vsegpt_chat cohere/command-r-plus                                            |      ----- |      ----- |      ----- | 89.45     |
| vsegpt_chat qwen/qwen-2-72b-instruct                                         |      ----- |      ----- |      ----- | 89.38     |
| vsegpt_chat qwen/qwen-2.5-72b-instruct                                       |      ----- |      ----- |      ----- |      87.85|
| vsegpt_chat nvidia/nemotron-4-340b-instruct                                  |      ----- |      ----- |      ----- | 90.07     |
| vsegpt_chat anthropic/claude-2                                               |      89.27 |      89.17 |      87.47 | 89.85     |
| vsegpt_chat anthropic/claude-3-haiku                                         |      ----- |      ----- |      ----- | 89.5      |
| vsegpt_chat anthropic/claude-3-5-haiku                                       |      ----- |      ----- |      ----- | 89.64     |
| vsegpt_chat anthropic/claude-3-sonnet                                        |      ----- |      ----- |      ----- | 89.49     |
| vsegpt_chat anthropic/claude-3-opus                                          |      ----- |      ----- |      ----- | 90.75     |
| vsegpt_chat anthropic/claude-3.5-sonnet-20240620                             |      ----- |      ----- |      ----- | 90.78     |
| vsegpt_chat anthropic/claude-3.5-sonnet-20241022                             |      ----- |      ----- |      ----- | 90.62     |
| vsegpt_chat cot_anthropic/claude-3.5-sonnet                                  |      ----- |      ----- |      ----- |      89.94|
| vsegpt_chat google/gemini-flash-1.5-8b                                       |      ----- |      ----- |      ----- | 88.34     |
| vsegpt_chat google/gemini-flash-1.5                                          |      ----- |      ----- |      ----- | 89.27     |
| vsegpt_chat google/gemini-pro                                                |      ----- |      ----- |      ----- | 89.69     |
| vsegpt_chat google/gemini-flash-1.5 (002)                                    |      ----- |      ----- |      ----- | 89.57     |
| vsegpt_chat google/gemini-pro-1.5 (002)                                      |      ----- |      ----- |      ----- | 89.55     |
| multi_sources google_translate,deepl                                         |      89.66 |  **89.85** |       87.8 | 90.42     |
| multi_sources google_translate,deepl,vsegpt_chat*                            |      89.66 |  **89.85** |      87.76 | 90.67     |
| yandex_dev                                                                   |      ----- |      ----- |      87.34 | 90.27     |
| multi_sources google_translate,yandex_dev                                    |      ----- |      ----- |      87.64 | 90.39     |
| multi_sources deepl,yandex_dev                                               |      ----- |      ----- |      87.64 | 90.62     |
| multi_sources google_translate,deepl,yandex_dev                              |      ----- |      ----- |      87.74 | 90.63     |
| multi_sources google_translate,deepl,yandex_dev,vsegpt_chat*                 |      ----- |      ----- |      87.71 | 90.66     |
| multi_sources deepl,yandex_dev,vsegpt_chat*                                  |      ----- |      ----- |      87.67 | 90.77     |
| multi_sources deepl,yandex_dev,vsegpt_chat**                                 |      ----- |      ----- |      ----- | **91.02** |
| multi_sources deepl,yandex_dev,vsegpt_chat***                                |      ----- |      ----- |      ----- | **91.05** |
| multi_sources deepl,yandex_dev,vsegpt_chat****                               |      ----- |      ----- |      ----- | **91.06** |

(yandex_dev represents Yandex.Translate service)

\* vsegpt_chat with anthropic/claude-2
\** vsegpt_chat with anthropic/claude-3-opus
\*** vsegpt_chat:openai/gpt-4o,vsegpt_chat:anthropic/claude-3-opus
\**** vsegpt_chat:openai/gpt-4o,vsegpt_chat:nvidia/nemotron-4-340b-instruct,vsegpt_chat:anthropic/claude-3-opus,vsegpt_chat:anthropic/claude-3.5-sonnet

**IMPORTANT:** You interested how it will work on YOUR language pairs? It's easy, script already included, see "Automatic BLEU measurement" chapter.

### Chain translation results (use_mid_lang plugin)

Chain translation allow to translate phrases with mid-language (usually English)

BLEU scores

|                                                                          |   jpn->rus |
|--------------------------------------------------------------------------|------------|
| no_translate                                                             |       0    |
| google_translate                                                         |      27.63 |
| deepl                                                                    |      27.48 |
| use_mid_lang google_translate,deepl                                      |      28.34 |
| use_mid_lang google_translate,google_translate                           |      27.62 |
| use_mid_lang deepl,deepl                                                 |      27.62 |

COMET scores

|                                                                          |   jpn->rus |
|--------------------------------------------------------------------------|------------|
| no_translate                                                             |      56.85 |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16               |      86.46 |
| google_translate                                                         |      87.93 |
| deepl                                                                    |      88.11 |
| use_mid_lang deepl->yandex_dev                                           |      87.56 |
| use_mid_lang google_translate->deepl                                     |      88.37 |
| use_mid_lang google_translate->google_translate                          |      87.67 |
| use_mid_lang deepl->deepl                                                |      88.43 |
| multi_sources google_translate,deepl                                     |      88.88 |
| use_mid_lang multi_sources->multi_sources*                               |       88.9 |
| multi_sources google_translate,deepl,use_mid_lang**                      |      89.05 |

- \* multi_sources with "google_translate,deepl"
- \** use_mid_lang with "google_translate,deepl"

vsegpt_chat with anthropic/claude-2 get a lot of fails ("Can't understand", "Can't translate")

More results on different multi_sources settings:

|                                                                                                                           |   jpn->rus |
|---------------------------------------------------------------------------------------------------------------------------|------------|
| multi_sources google_translate,deepl,use_mid_lang:google_translate->deepl,use_mid_lang:google_translate->google_translate |      89.05 |
| multi_sources google_translate,deepl,use_mid_lang:google_translate->deepl,use_mid_lang:deepl->deepl                       |      89.15 |
| multi_sources google_translate,deepl,use_mid_lang:deepl->deepl                                                            |      89.04 |
| multi_sources****                                                                                                         |      89.25 |

\**** model: google_translate,deepl,use_mid_lang:deepl->deepl,use_mid_lang:google_translate->deepl,use_mid_lang:google_translate->google_translate,use_mid_lang:deepl->google_translate 

## Automatic BLEU and COMET estimation

There are builded package to run BLEU and COMET estimation of plugin translation on different languages - so, you usually can reproduce our results.

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

BLEU_PLUGINS_AR = ["google_translate", "deepl", "multi_sources:google_translate,deepl"] 
    # plugins to estimate, array
    # now you can run them in format "plugin:model", that works only if plugin support "on-the-fly" model change (usually YES for synthetic and online plugins, and NO for offline)

BLEU_NUM_PHRASES = 100 # num of phrases to estimate. Between 1 and 100 for now.
BLEU_START_PHRASE = 150 # offset from FLORES dataset to get NUM phrases

BLEU_METRIC = "bleu" # bleu | comet
```
