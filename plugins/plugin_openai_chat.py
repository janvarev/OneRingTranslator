# Translation throw ChatGPT
# works only with native POST requests, not openai lib
# author: Vladislav Janvarev

from oneringcore import OneRingCore


import os
import requests
import json

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:OneRingCore):
    manifest = {
        "name": "Translation through ChatGPT",
        "version": "3.2",
        "description": "After define apiKey allow to translate through ChatGPT.",

        "options_label": {
            "apiKey": "API-key OpenAI", #
            "apiBaseUrl": "URL for OpenAI (allow OpenAI emulation servers)",  #
            "system": "System input string."
        },

        "default_options": {
            "apiKey": "", #
            "apiBaseUrl": "https://api.openai.com/v1",  #
            "system": "You are a professional translator.",
            "prompt": "Instruction: Translate this text from {0} to {1}:\n\n{2}",
            "model": "gpt-3.5-turbo",
        },

        "translate": {
            "openai_chat": (init, translate)  # 1 function - init, 2 - translate
        }

    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    options = core.plugin_options(modname)

    # if options["apiKey"] == "" and options["apiBaseUrl"] == "":
    #     raise ValueError("Needed API KEY for access")

    # openai.api_key = options["apiKey"]
    # if options["apiBaseUrl"] != "":
    #     openai.api_base = options["apiBaseUrl"]
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):

    options = core.plugin_options(modname)

    from_full_lang = core.dict_2let_to_lang.get(from_lang)
    to_full_lang = core.dict_2let_to_lang.get(to_lang)

    #prompt = f"Instruction: Translate this text from {from_full_lang} to {to_full_lang}:\n\n{text}"
    prompt = str(options["prompt"]).format(from_full_lang,to_full_lang,text)
    system_text = str(options["system"]).format(from_full_lang,to_full_lang,text)

    response = requests.post(
        url=f"{options['apiBaseUrl']}/chat/completions",
        headers={
            "Authorization": f"Bearer {options['apiKey']}",
            "Content-Type": "application/json"
        },
        data = json.dumps({
            "model": str(options["model"]),  # Optional
            "messages": [
                {"role": "system", "content": system_text},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.05,
            "top_p": 0.95,
            "n": 1,
            "max_tokens": int(len(prompt) * 1.5)
            })
    )

    if response.status_code == 200:
        response_big = json.loads(response.text)
        response = response_big["choices"][0]["message"]

        res = str(response["content"]).strip()
        return res
    else:
        raise ValueError(str(response.status_code)+": "+response.text)


