# Deepl Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Deepl Translator", # name
        "version": "1.1", # version

        "default_options": {
            "api_key": "",  #
            "is_free_api": True, # use Free version or not
        },

        "translate": {

            "deepl": (init, translate),  # 1 function - init, 2 - translate
            # deprecated
            "deepl_translate": (init, translate)  # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass
def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    from deep_translator import DeeplTranslator
    #custom_url = core.plugin_options(modname).get("custom_url")
    is_free:bool = core.plugin_options(modname).get("is_free_api")
    api_key:str = core.plugin_options(modname).get("api_key")
    #print(custom_url)
    #res = LibreTranslator(source=from_lang, target=to_lang, custom_url=custom_url).translate(text)
    res = DeeplTranslator(api_key, use_free_api=is_free, source=from_lang, target=to_lang).translate(text)


    return res
