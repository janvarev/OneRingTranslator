# Libre Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Libre Translator", # name
        "version": "1.0", # version

        "default_options": {
            "custom_url": "https://translate.argosopentech.com/",  # mirror for LibreTranslator service
        },

        "translate": {
            "libre_translate": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass
def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    # просто выводим текст в консоль
    from deep_translator import LibreTranslator
    res = LibreTranslator(source=from_lang, target=to_lang, custom_url=core.plugin_options(modname).get("custom_url")).translate(text)
    return res
