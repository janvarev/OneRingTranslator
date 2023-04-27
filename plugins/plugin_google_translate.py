# Google Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Google Translate", # name
        "version": "1.0", # version

        "translate": {
            "google_translate": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    # просто выводим текст в консоль
    from deep_translator import GoogleTranslator
    res = GoogleTranslator(source=from_lang, target=to_lang).translate(text)
    return res
