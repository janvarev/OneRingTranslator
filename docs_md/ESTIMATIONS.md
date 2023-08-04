## Average BLEU and COMET results for translation quality

**BLEU (bilingual evaluation understudy)** is an automatic algorithm for evaluating the quality of text which has been machine-translated from one natural language to another.

**COMET** is also an automatic algorithm for evaluating the quality of translated text, based on neuronets.

**From author**: BLEU was introduced in 2002, and COMET in 2020. As for now, I recommend COMET scores more than BLEU. 

Use this results just for reference.

**BLEU scores** (higher is better, no_translate can be used as baseline. Average on 100 examples from FLORES, offset = 150):

|                                                                 |   fra->eng |   eng->fra |   rus->eng |   eng->rus |
|-----------------------------------------------------------------|------------|------------|------------|------------|
| no_translate                                                    |       3.98 |       3.9  |       0.57 |       0.56 |
| libre_translate                                                 |      47.66 |      49.62 |      32.43 |      30.99 |
| fb_nllb_translate nllb-200-distilled-600M                       |      51.92 |      52.73 |      41.38 |      31.41 |
| fb_nllb_translate nllb-200-distilled-1.3B                       |      56.81 |       55   |      46.03 |      33.98 |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16      |      54.87 |      56.73 |      48.45 |      36.85 |
| fb_nllb_ctranslate2 JustFr-ik/nllb-200-distilled-1.3B-ct2-int8  |      56.12 |      56.45 |      46.07 |      34.56 |
| google_translate                                                |      58.08 |      59.99 |      47.7  |      37.98 |
| deepl_translate                                                 |      57.67 |      59.93 |  **50.09** |      38.91 |
| yandex_dev                                                      |      ----- |      ----- |      46.09 |  **40.23** |
| openai_chat gpt-3.5-turbo (aka ChatGPT)                         |      ----- |      ----- |      41.49 |      30.9  |
| koboldapi_translate (alpaca7B-4bit)                             |      43.51 |      30.54 |      32    |      14.19 |
| koboldapi_translate (alpaca30B-4bit)                            |      ----- |      ----- |      ----- |      24.0  |
| fb_mbart50  facebook/mbart-large-50-one-to-many-mmt             |      ----- |      48.79 |      ----- |      28.55 |
| fb_mbart50  facebook/mbart-large-50-many-to-many-mmt            |      50.26 |      48.93 |      42.47 |      28.56 |
| openrouter_chat openai/gpt-3.5-turbo                            |      ----- |      ----- |      41.93 |      31.12 |
| openrouter_chat openai/gpt-4                                    |      ----- |      ----- |      44.16 |      34.88 |
| openrouter_chat anthropic/claude-instant-v1                     |      ----- |      ----- |      41.88 |      29.67 |
| openrouter_chat anthropic/claude-2                              |      54.91 |      56.09 |      46.38 |      34.13 |
| opus_mt Helsinki-NLP/opus-mt-en-ru                              |      ----- |      ----- |      ----- |      30.41 |


**LLMs with errors:**

- openrouter_chat tiiuae/falcon-40b-instruct - a lot of fails
- openrouter_chat google/palm-2-chat-bison - "I'm not able to help with that, as I'm only a language model."
- 'koboldapi_translate' on 'eng->rus' pair average BLEU score:     7.00: 80/100
on IlyaGusev-saiga_7b_lora_llamacpp-ggml-model-q4_1.bin, may be adjusting for input prompt needed

**COMET scores** (higher is better, no_translate2 can be used as baseline. Average on 100 examples from FLORES, offset = 150):

|                                                                  |   fra->eng |   eng->fra |   rus->eng | eng->rus  |
|------------------------------------------------------------------|------------|------------|------------|-----------|
| no_translate2                                                    |      31.66 |      32.06 |      33.03 | 25.58     |
| no_translate                                                     |      79.2  |      70.19 |       69.3 |      44.82|
| opus_mt Helsinki-NLP/opus-mt-en-ru                               |      ----- |      ----- |      ----- |      82.22|
| libre_translate                                                  |      86.66 |      82.36 |      80.36 | 83.34     |
| lingvanex                                                        |      87.92 |      86.99 |      84.75 |       86.3|
| fb_nllb_translate nllb-200-distilled-1.3B                        |      89.01 |      87.95 |      86.91 | 88.57     |
| fb_nllb_ctranslate2 JustFrederik/nllb-200-3.3B-ct2-float16       |      88.74 |      88.32 |      87.25 |      88.83|
| google_translate                                                 |  **89.67** |      88.9  |      87.53 | 89.63     |
| deepl                                                            |      89.39 |      89.27 |  **87.93** |      89.82|
| openrouter_chat anthropic/claude-instant-v1                      |      ----- |      ----- |      85.73 | 88.13     |
| openrouter_chat openai/gpt-4                                     |      ----- |      ----- |      87.02 | 89.54     |
| openrouter_chat anthropic/claude-2                               |      89.27 |      89.17 |      87.47 | 89.85     |
| multi_sources google_translate,deepl                             |      89.66 |  **89.85** |       87.8 |      90.42|
| multi_sources google_translate,deepl,openrouter_chat*            |      89.66 |  **89.85** |      87.76 |     90.67 |
| yandex_dev                                                       |      ----- |      ----- |      87.34 | 90.27     |
| multi_sources deepl,yandex_dev                                   |      ----- |      ----- |      87.64 | 90.62     |
| multi_sources google_translate,deepl,yandex_dev                  |      ----- |      ----- |      87.74 | 90.63     |
| multi_sources google_translate,deepl,yandex_dev,openrouter_chat* |      ----- |      ----- |      87.71 | 90.66     |
| multi_sources deepl,yandex_dev,openrouter_chat*                  |      ----- |      ----- |      87.67 | **90.77** |

\* openrouter_chat with anthropic/claude-2

**IMPORTANT:** You interested how it will work on YOUR language pairs? It's easy, script already included, see "Automatic BLEU measurement" chapter.

**Chain translation results (use_mid_lang plugin)**

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
| google_translate                                                         |      87.93 |
| deepl                                                                    |      88.11 |
| use_mid_lang google_translate,deepl                                      |      88.37 |
| use_mid_lang google_translate,google_translate                           |      87.67 |
| use_mid_lang deepl,deepl                                                 |      88.43 |
| multi_sources google_translate,deepl                                     |      88.88 |
| use_mid_lang multi_sources,multi_sources*                                |       88.9 |
| multi_sources google_translate,deepl,use_mid_lang**                      |      89.05 |

- \* multi_sources with "google_translate,deepl"
- \** use_mid_lang with "google_translate,deepl"

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

BLEU_PLUGINS = "no_translate,google_translate" # plugins to estimate, separated by ,

BLEU_NUM_PHRASES = 100 # num of phrases to estimate. Between 1 and 100 for now.
BLEU_START_PHRASE = 150 # offset from FLORES dataset to get NUM phrases

BLEU_METRIC = "bleu" # bleu | comet
```
