# mbart plugin
# author: Vladislav Janvarev

# from https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

model = None
tokenizers:dict = {}

# -------- lang list

#langlist_str = "ar_AR,cs_CZ,de_DE,en_XX,es_XX,et_EE,fi_FI,fr_XX,gu_IN,hi_IN,it_IT,ja_XX,kk_KZ,ko_KR,lt_LT,lv_LV,my_MM,ne_NP,nl_XX,ro_RO,ru_RU,si_LK,tr_TR,vi_VN,zh_CN"

#langlist = langlist_str.split(",")
langlist_str = "Arabic (ar_AR), Czech (cs_CZ), German (de_DE), English (en_XX), Spanish (es_XX), Estonian (et_EE), Finnish (fi_FI), French (fr_XX), Gujarati (gu_IN), Hindi (hi_IN), Italian (it_IT), Japanese (ja_XX), Kazakh (kk_KZ), Korean (ko_KR), Lithuanian (lt_LT), Latvian (lv_LV), Burmese (my_MM), Nepali (ne_NP), Dutch (nl_XX), Romanian (ro_RO), Russian (ru_RU), Sinhala (si_LK), Turkish (tr_TR), Vietnamese (vi_VN), Chinese (zh_CN), Afrikaans (af_ZA), Azerbaijani (az_AZ), Bengali (bn_IN), Persian (fa_IR), Hebrew (he_IL), Croatian (hr_HR), Indonesian (id_ID), Georgian (ka_GE), Khmer (km_KH), Macedonian (mk_MK), Malayalam (ml_IN), Mongolian (mn_MN), Marathi (mr_IN), Polish (pl_PL), Pashto (ps_AF), Portuguese (pt_XX), Swedish (sv_SE), Swahili (sw_KE), Tamil (ta_IN), Telugu (te_IN), Thai (th_TH), Tagalog (tl_XX), Ukrainian (uk_UA), Urdu (ur_PK), Xhosa (xh_ZA), Galician (gl_ES), Slovene (sl_SI)"
l = langlist_str.split(", ")
langlist = []
for k in l:
    if k != "":
        langlist.append(k[-6:-1])
#print(langlist)


cuda_opt = -1
to_device = "cpu"
# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "MBART 50 Translate", # name
        "version": "2.0", # version

        "translate": {
            "fb_mbart50": (init,translate) # 1 function - init, 2 - translate
        },

        "default_options": {
            "model": "facebook/mbart-large-50-many-to-many-mmt",  # key model
            "cuda": -1, # -1 if you want run on CPU, 0 - if on CUDA
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
    from transformers import MBartForConditionalGeneration

    global model

    #print(to_device)
    model = MBartForConditionalGeneration.from_pretrained(core.plugin_options(modname).get("model")).to(to_device)


    pass

def convert_lang(input_lang:str) -> str:
    if len(input_lang) == 2:
        # if input_lang == "en" or input_lang == "eng":
        #     return "eng_Latn"
        # if input_lang == "ru":
        #     return "rus_Cyrl"

        for lang in langlist:
            if lang.startswith(input_lang):
                return lang

    else:
        return input_lang

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    from transformers import MBartForConditionalGeneration, MBart50Tokenizer

    from_lang_tr = convert_lang(from_lang)
    to_lang_tr = convert_lang(to_lang)

    full_id = f"{from_lang_tr}__{to_lang_tr}"

    # print(from_lang_tr)
    # print(to_lang_tr)

    if tokenizers.get(full_id) is None:
        tokenizers[full_id] = MBart50Tokenizer.from_pretrained(core.plugin_options(modname).get("model"), src_lang=from_lang_tr, tgt_lang=to_lang_tr)
    # if tokenizers.get(to_lang_tr) is None:
    #     tokenizers[to_lang_tr] = AutoTokenizer.from_pretrained(core.plugin_options(modname).get("model"), src_lang=to_lang_tr)

    tokenizer_from = tokenizers.get(full_id)
    inputs = tokenizer_from(text, return_tensors="pt").to(to_device)

    translated_tokens = model.generate(
                            #**inputs, forced_bos_token_id=tokenizer_from.lang_code_to_id[to_lang_tr], max_length=int(len(text)*5)
                            **inputs, forced_bos_token_id=tokenizer_from.lang_code_to_id[to_lang_tr], max_length=int(len(text) * 5)
                        )
    res = tokenizer_from.batch_decode(translated_tokens, skip_special_tokens=True)[0]



    return res

