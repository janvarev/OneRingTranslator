# lingvanex Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "lingvanex Translator", # name
        "version": "1.1", # version

        "default_options": {
            "api_key": "",  #
        },

        "translate": {
            "lingvanex": (init, translate)  # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass
def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):

    api_key:str = core.plugin_options(modname).get("api_key")

    import requests

    url = "https://api-b2b.backenster.com/b1/api/v3/translate"

    payload = {
        "platform": "api",
        "from": from_lang,
        "to": to_lang,
        "data": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    #print(respons*e.text)
    response_json = response.json()

    if response_json.get("err") is not None:
        raise ValueError("ERR in ligvanex server call: "+response_json.get("err"))
    #print(response_json)


    return response_json["result"]
