# Multisources
# gain translations from different sources and try to select one best
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Multi sources plugin", # name
        "version": "1.1", # version

        "default_options": {
            "model": "google_translate,deepl",  # plugins that will be processed
        },

        "translate": {
            "multi_sources": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    pass

def init(core:OneRingCore):
    from comet import download_model, load_from_checkpoint
    print("Activating COMET model...")
    model_path = download_model("Unbabel/wmt20-comet-qe-da")
    core.comet_model_multi_sources = load_from_checkpoint(model_path)
    print("COMET model activated!")
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    plugins: str = core.plugin_options(modname).get("model").split(",")
    data = []
    for plugin in plugins:
        mt = core.translate(text,from_lang,to_lang,plugin).get("result")
        data.append({"src":text,"mt":mt})

    #print(data)

    pred = core.comet_model_multi_sources.predict(data, batch_size=8, gpus=0)
    #print(model_output)
    scores = pred.get("scores")

    max_ind = scores.index(max(scores))
    #print('Scores:',scores, max_ind)


    return data[max_ind]["mt"]
