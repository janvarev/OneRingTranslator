# plugin_gemini_chat.py
from oneringcore import OneRingCore
import os
import requests
import json

modname = os.path.basename(__file__)[:-3]  # calculating modname

def start(core: OneRingCore):
    manifest = {
        "name": "Translation through Gemini",
        "version": "1.0",
        "description": "After defining apiKey, allow to translate through Gemini.",

        "options_label": {
            "apiKey": "API-key Gemini",
            "apiBaseUrl": "URL for Gemini API. Now using v1beta",
            "system": "System input string."
        },

        "default_options": {
            "apiKey": "",
            "apiBaseUrl": "https://generativelanguage.googleapis.com/v1beta/models",
            "system": "You are a professional translator. Give 1 answer directly without aditional explanations",
            "prompt": "Instruction: Translate this text from {0} to {1}:\n\n{2}",
            "model": "gemini-2.0-flash",
        },

        "translate": {
            "gemini_chat": (init, translate)  # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core: OneRingCore, manifest: dict):
    pass

def init(core: OneRingCore):
    options = core.plugin_options(modname)

    if options["apiKey"] == "":
        raise ValueError("Needed API KEY for access")

    # Initialize any necessary configurations here
    pass

def translate(core: OneRingCore, text: str, from_lang: str = "", to_lang: str = "", add_params: str = ""):
    options = core.plugin_options(modname)

    from_full_lang = core.dict_2let_to_lang.get(from_lang)
    to_full_lang = core.dict_2let_to_lang.get(to_lang)

    prompt = str(options["prompt"]).format(from_full_lang, to_full_lang, text)
    system_text = str(options["system"]).format(from_full_lang, to_full_lang, text)

    response = requests.post(
        url=f"{options['apiBaseUrl']}/{options['model']}:generateContent?key={options['apiKey']}",
        headers={
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "system_instruction":{"parts": {"text": system_text},},
             "contents":{ "parts":{"text":prompt}},
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": int(len(prompt) * 1.5),
                "topP": 0.95,
                "topK": 10
            },

        })
    )

    if response.status_code == 200:
        response_big = json.loads(response.text)
        response = response_big["candidates"][0]["content"]["parts"][0]

        res = str(response["text"]).strip()
        return res
    else:
        raise ValueError(str(response.status_code) + ": " + response.text)