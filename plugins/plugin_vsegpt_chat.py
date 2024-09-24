# Translation throw VseGPT
# author: Vladislav Janvarev

import os
import time

import openai

from oneringcore import OneRingCore

import json

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:OneRingCore):
    manifest = {
        "name": "Translation through VseGPT",
        "version": "1.3",
        "description": "After define apiKey allow to translate through VseGPT.",

        "options_label": {
            "apiKey": "API-key OpenAI (VseGPT)", #
            "apiBaseUrl": "URL for OpenAI (allow OpenAI emulation servers)",  #
            "system": "System input string.",
            "max_token_mult_factor": "Multiplicator for calculate max_tokens param based on input string. 2 for EN<->FR languages, 6 for Chinese->EN",
            "split_result_by": "If not empty, split result by "
        },

        # this is DEFAULT options
        # ACTUAL options is in options/<plugin_name>.json after first run
        "default_options": {
            "apiKey": "", #
            "apiBaseUrl": "https://api.vsegpt.ru/v1",  #
            "system": "Please translate the user message from {0} to {1}. Make the translation sound as natural as possible. Don't use any non-related phrases in result, answer with only translation text.",
            "prompt": "{2}",
            "model": "openai/gpt-3.5-turbo",
            "max_token_mult_factor": 2.0,
            # "is_use_chain_of_thought": False,
            "cot_system": "Please translate the user message from {0} to {1}. \nStart your response with \"Let's work this out in a step by step way to be sure we have the right answer:\" and work this out in a step by step way separately from providing answer to the task, to be sure you have the right answer.\nMake the final translation sound as natural as possible.\nAfterwards, provide final translation using the step by step as guidance, after phrase \"FINAL ANSWER:\"",
            "cot_prompt": "{2}",
            "cot_split_result_by": "FINAL ANSWER:"
        },

        "translate": {
            "vsegpt_chat": (init, translate)  # 1 function - init, 2 - translate
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

    model = str(options["model"])
    #prompt = f"Instruction: Translate this text from {from_full_lang} to {to_full_lang}:\n\n{text}"
    is_cot:bool = model.startswith("cot_")
    if is_cot:
        model = model[4:]
        prompt = str(options["cot_prompt"]).format(from_full_lang, to_full_lang, text)
        system_text = str(options["cot_system"]).format(from_full_lang, to_full_lang, text)
    else:
        prompt = str(options["prompt"]).format(from_full_lang,to_full_lang,text)
        system_text = str(options["system"]).format(from_full_lang,to_full_lang,text)
    mult_factor:float = options["max_token_mult_factor"]

    messages = []
    messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": prompt})

    # with no_ssl_verification():
    try:
        response_big = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.05,
            # temperature=0.5,
            top_p=0.95,
            n=1,
            max_tokens=int(len(prompt) * mult_factor),
            headers={"X-Title": "OneRingTranslator"},
        )
    except openai.error.RateLimitError as e: # in case of rate limit error
        #
        time.sleep(2.0)
        response_big = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.05,
            # temperature=0.5,
            top_p=0.95,
            n=1,
            max_tokens=int(len(prompt) * mult_factor),
            headers={"X-Title": "OneRingTranslator"},
        )
    except openai.error.APIError as e: # in case of server error
        #
        if e.http_status > 499 or e.http_status == 430: # something on server, try once more
            time.sleep(2.0)
            response_big = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.05,
                # temperature=0.5,
                top_p=0.95,
                n=1,
                max_tokens=int(len(prompt) * mult_factor),
                headers={"X-Title": "OneRingTranslator"},
            )
        else:
            raise e
    #print("Response BIG:",response_big)
    response = response_big["choices"][0]["message"]



    res:str = str(response["content"]).strip()
    if is_cot:
        print("COT:",res)
        res2 = res.split(options["cot_split_result_by"],1)
        res = str(res2[1]).strip()
    # print(res)
    return res

