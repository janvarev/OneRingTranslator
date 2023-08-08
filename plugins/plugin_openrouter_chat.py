# Translation throw OpenRouter
# author: Vladislav Janvarev

import os
import openai

from oneringcore import OneRingCore

import json

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:OneRingCore):
    manifest = {
        "name": "Translation through OpenRouter",
        "version": "3.1",
        "description": "After define apiKey allow to translate through OpenRouter.",

        "options_label": {
            "apiKey": "API-key OpenAI", #
            "apiBaseUrl": "URL for OpenAI (allow OpenAI emulation servers)",  #
            "system": "System input string."
        },

        # this is DEFAULT options
        # ACTUAL options is in options/<plugin_name>.json after first run
        "default_options": {
            "apiKey": "", #
            "apiBaseUrl": "https://openrouter.ai/api/v1",  #
            "system": "Please translate the user message from {0} to {1}. Make the translation sound as natural as possible. Don't use any non-related phrases in result, answer with only translation text.",
            "prompt": "{2}",
            "model": "",
        },

        "translate": {
            "openrouter_chat": (init, translate)  # 1 function - init, 2 - translate
        }

    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    options = core.plugin_options(modname)

    if options["apiKey"] == "" and options["apiBaseUrl"] == "":
        raise ValueError("Needed API KEY for access")

    openai.api_key = options["apiKey"]

    if options["apiBaseUrl"] != "":
        openai.api_base = options["apiBaseUrl"]


def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    options = core.plugin_options(modname)

    from_full_lang = core.dict_2let_to_lang.get(from_lang)
    to_full_lang = core.dict_2let_to_lang.get(to_lang)

    #prompt = f"Instruction: Translate this text from {from_full_lang} to {to_full_lang}:\n\n{text}"
    prompt = str(options["prompt"]).format(from_full_lang,to_full_lang,text)
    system_text = str(options["system"]).format(from_full_lang,to_full_lang,text)

    messages = []
    messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": prompt})

    response_big = openai.ChatCompletion.create(
        model=str(options["model"]),
        messages=messages,
        temperature=0.7,
        n=1,
        max_tokens=int(len(prompt) * 1.5),
        headers= { "HTTP-Referer": "https://github.com/janvarev/OneRingTranslator",
          "X-Title": "OneRingTranslator" },
    )
    response = response_big["choices"][0]["message"]

    #core.chatapp = ChatApp(model=str(options["model"]),system=system_text) # create new chat

    #response = core.chatapp.chat(prompt)  # generate_response(phrase)
    #print(response)
    res = str(response["content"]).strip()
    #print(res)
    return res

