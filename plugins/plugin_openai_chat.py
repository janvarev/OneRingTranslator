# Translation throw ChatGPT
# author: Vladislav Janvarev

import os
import openai

from oneringcore import OneRingCore

import json
import os
import openai

# ---------- from https://github.com/stancsz/chatgpt ----------
class ChatApp:
    def __init__(self, model="gpt-3.5-turbo", load_file='', system=''):
        # Setting the API key to use the OpenAI API
        self.model = model
        self.messages = []
        if system != '':
            self.messages.append({"role": "system", "content" : system})
        if load_file != '':
            self.load(load_file)

    def chat(self, message):
        if message == "exit":
            self.save()
            os._exit(1)
        elif message == "save":
            self.save()
            return "(saved)"
        self.messages.append({"role": "user", "content": message})
        print(self.messages)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            n=1,
            max_tokens=int(len(message)*1.5),
            #headers=
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response["choices"][0]["message"]
    def save(self):
        try:
            import time
            import re
            import json
            ts = time.time()
            json_object = json.dumps(self.messages, indent=4)
            filename_prefix=self.messages[0]['content'][0:30]
            filename_prefix = re.sub('[^0-9a-zA-Z]+', '-', f"{filename_prefix}_{ts}")
            with open(f"models/chat_model_{filename_prefix}.json", "w") as outfile:
                outfile.write(json_object)
        except:
            os._exit(1)

    def load(self, load_file):
        with open(load_file) as f:
            data = json.load(f)
            self.messages = data

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:OneRingCore):
    manifest = {
        "name": "Translation through ChatGPT",
        "version": "3.1",
        "description": "After define apiKey allow to translate through ChatGPT.",

        "options_label": {
            "apiKey": "API-key OpenAI", #
            "apiBaseUrl": "URL for OpenAI (allow OpenAI emulation servers)",  #
            "system": "System input string."
        },

        "default_options": {
            "apiKey": "", #
            "apiBaseUrl": "",  #
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

    core.chatapp = ChatApp(model=str(options["model"]),system=system_text) # create new chat

    response = core.chatapp.chat(prompt)  # generate_response(phrase)
    #print(response)
    return response["content"]

