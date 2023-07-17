# opus mt
# author: Vladislav Janvarev

# from https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-hu-en

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

model = None
tokenizer = None

cuda_opt = -1
to_device = "cpu"
# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Opus MT Translate", # name
        "version": "1.0", # version

        "translate": {
            "opus_mt": (init,translate) # 1 function - init, 2 - translate
        },

        "default_options": {
            "model": "Helsinki-NLP/opus-mt-en-ru",  # key model
            "cuda": -1, # -1 if you want run on CPU, 0 - if on CUDA
            "text_prefix": "" # for models like https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-he-itc
            # be like >>hbs<< etc.
        },
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    global cuda_opt
    global to_device
    cuda_opt = manifest["options"].get("cuda")
    if cuda_opt == -1:
        to_device = "cpu"
    else:
        to_device = "cuda:{0}".format(cuda_opt)
    pass

def init(core:OneRingCore):
    from transformers import MarianMTModel, MarianTokenizer

    global model, tokenizer

    #print(to_device)
    model_name = core.plugin_options(modname).get("model")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).to(to_device)


def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    src_text = [core.plugin_options(modname).get("text_prefix")+text]
    translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True).to(to_device))
    res = tokenizer.decode(translated[0], skip_special_tokens=True)
    return res