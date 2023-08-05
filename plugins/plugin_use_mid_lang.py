# Use mid (mediator) language
# Translate in two phases: from lang->mediator lang, mediator lang->to lang
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os
import time

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Use mediator language", # name
        "version": "1.1", # version

        "default_options": {
            "model": "google_translate->deepl",  # 1 phase plugin, 2 phase plugin
            #  1 phase from lang->mediator lang,
            #  2 phase mediator lang->to lang
            "mid_lang": "en",
        },

        "translate": {
            "use_mid_lang": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    plugins: str = core.plugin_options(modname).get("model").split("->")
    mid_lang: str = core.plugin_options(modname).get("mid_lang")
    res1 = core.translate(text,from_lang,mid_lang,plugins[0]).get("result")
    #print(from_lang,mid_lang,res1)
    #time.sleep(0.02)
    res2 = core.translate(res1,mid_lang,to_lang,plugins[1]).get("result")
    #print(mid_lang,to_lang,res2)

    return res2
