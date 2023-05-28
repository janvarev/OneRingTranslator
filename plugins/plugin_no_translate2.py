# No Translate dummy plugin - return blank
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "No Translate2 dummy plugin", # name
        "version": "1.0", # version

        "translate": {
            "no_translate2": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    return ""
