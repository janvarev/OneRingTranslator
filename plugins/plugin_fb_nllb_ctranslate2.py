# nllb plugin with https://opennmt.net/CTranslate2/index.html support
# author: Vladislav Janvarev

# from https://github.com/facebookresearch/fairseq/tree/nllb

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

model = None
tokenizers:dict = {}

# -------- lang list

langlist_str = """
ace_Arab    | Acehnese (Arabic script)
ace_Latn    | Acehnese (Latin script)
acm_Arab    | Mesopotamian Arabic
acq_Arab    | Ta’izzi-Adeni Arabic
aeb_Arab    | Tunisian Arabic
afr_Latn    | Afrikaans
ajp_Arab    | South Levantine Arabic
aka_Latn    | Akan
als_Latn    | Tosk Albanian
amh_Ethi    | Amharic
apc_Arab    | North Levantine Arabic
arb_Arab    | Modern Standard Arabic
arb_Latn    | Modern Standard Arabic (Romanized)
ars_Arab    | Najdi Arabic
ary_Arab    | Moroccan Arabic
arz_Arab    | Egyptian Arabic
asm_Beng    | Assamese
ast_Latn    | Asturian
awa_Deva    | Awadhi
ayr_Latn    | Central Aymara
azb_Arab    | South Azerbaijani
azj_Latn    | North Azerbaijani
bak_Cyrl    | Bashkir
bam_Latn    | Bambara
ban_Latn    | Balinese
bel_Cyrl    | Belarusian
bem_Latn    | Bemba
ben_Beng    | Bengali
bho_Deva    | Bhojpuri
bjn_Arab    | Banjar (Arabic script)
bjn_Latn    | Banjar (Latin script)
bod_Tibt    | Standard Tibetan
bos_Latn    | Bosnian
bug_Latn    | Buginese
bul_Cyrl    | Bulgarian
cat_Latn    | Catalan
ceb_Latn    | Cebuano
ces_Latn    | Czech
cjk_Latn    | Chokwe
ckb_Arab    | Central Kurdish
crh_Latn    | Crimean Tatar
cym_Latn    | Welsh
dan_Latn    | Danish
deu_Latn    | German
dik_Latn    | Southwestern Dinka
dyu_Latn    | Dyula
dzo_Tibt    | Dzongkha
ell_Grek    | Greek
eng_Latn    | English
epo_Latn    | Esperanto
est_Latn    | Estonian
eus_Latn    | Basque
ewe_Latn    | Ewe
fao_Latn    | Faroese
fij_Latn    | Fijian
fin_Latn    | Finnish
fon_Latn    | Fon
fra_Latn    | French
fur_Latn    | Friulian
fuv_Latn    | Nigerian Fulfulde
gaz_Latn    | West Central Oromo
gla_Latn    | Scottish Gaelic
gle_Latn    | Irish
glg_Latn    | Galician
grn_Latn    | Guarani
guj_Gujr    | Gujarati
hat_Latn    | Haitian Creole
hau_Latn    | Hausa
heb_Hebr    | Hebrew
hin_Deva    | Hindi
hne_Deva    | Chhattisgarhi
hrv_Latn    | Croatian
hun_Latn    | Hungarian
hye_Armn    | Armenian
ibo_Latn    | Igbo
ilo_Latn    | Ilocano
ind_Latn    | Indonesian
isl_Latn    | Icelandic
ita_Latn    | Italian
jav_Latn    | Javanese
jpn_Jpan    | Japanese
kab_Latn    | Kabyle
kac_Latn    | Jingpho
kam_Latn    | Kamba
kan_Knda    | Kannada
kas_Arab    | Kashmiri (Arabic script)
kas_Deva    | Kashmiri (Devanagari script)
kat_Geor    | Georgian
kaz_Cyrl    | Kazakh
kbp_Latn    | Kabiyè
kea_Latn    | Kabuverdianu
khk_Cyrl    | Halh Mongolian
khm_Khmr    | Khmer
kik_Latn    | Kikuyu
kin_Latn    | Kinyarwanda
kir_Cyrl    | Kyrgyz
kmb_Latn    | Kimbundu
kmr_Latn    | Northern Kurdish
knc_Arab    | Central Kanuri (Arabic script)
knc_Latn    | Central Kanuri (Latin script)
kon_Latn    | Kikongo
kor_Hang    | Korean
lao_Laoo    | Lao
lij_Latn    | Ligurian
lim_Latn    | Limburgish
lin_Latn    | Lingala
lit_Latn    | Lithuanian
lmo_Latn    | Lombard
ltg_Latn    | Latgalian
ltz_Latn    | Luxembourgish
lua_Latn    | Luba-Kasai
lug_Latn    | Ganda
luo_Latn    | Luo
lus_Latn    | Mizo
lvs_Latn    | Standard Latvian
mag_Deva    | Magahi
mai_Deva    | Maithili
mal_Mlym    | Malayalam
mar_Deva    | Marathi
min_Arab    | Minangkabau (Arabic script)
min_Latn    | Minangkabau (Latin script)
mkd_Cyrl    | Macedonian
mlt_Latn    | Maltese
mni_Beng    | Meitei (Bengali script)
mos_Latn    | Mossi
mri_Latn    | Maori
mya_Mymr    | Burmese
nld_Latn    | Dutch
nno_Latn    | Norwegian Nynorsk
nob_Latn    | Norwegian Bokmål
npi_Deva    | Nepali
nso_Latn    | Northern Sotho
nus_Latn    | Nuer
nya_Latn    | Nyanja
oci_Latn    | Occitan
ory_Orya    | Odia
pag_Latn    | Pangasinan
pan_Guru    | Eastern Panjabi
pap_Latn    | Papiamento
pbt_Arab    | Southern Pashto
pes_Arab    | Western Persian
plt_Latn    | Plateau Malagasy
pol_Latn    | Polish
por_Latn    | Portuguese
prs_Arab    | Dari
quy_Latn    | Ayacucho Quechua
ron_Latn    | Romanian
run_Latn    | Rundi
rus_Cyrl    | Russian
sag_Latn    | Sango
san_Deva    | Sanskrit
sat_Olck    | Santali
scn_Latn    | Sicilian
shn_Mymr    | Shan
sin_Sinh    | Sinhala
slk_Latn    | Slovak
slv_Latn    | Slovenian
smo_Latn    | Samoan
sna_Latn    | Shona
snd_Arab    | Sindhi
som_Latn    | Somali
sot_Latn    | Southern Sotho
spa_Latn    | Spanish
srd_Latn    | Sardinian
srp_Cyrl    | Serbian
ssw_Latn    | Swati
sun_Latn    | Sundanese
swe_Latn    | Swedish
swh_Latn    | Swahili
szl_Latn    | Silesian
tam_Taml    | Tamil
taq_Latn    | Tamasheq (Latin script)
taq_Tfng    | Tamasheq (Tifinagh script)
tat_Cyrl    | Tatar
tel_Telu    | Telugu
tgk_Cyrl    | Tajik
tgl_Latn    | Tagalog
tha_Thai    | Thai
tir_Ethi    | Tigrinya
tpi_Latn    | Tok Pisin
tsn_Latn    | Tswana
tso_Latn    | Tsonga
tuk_Latn    | Turkmen
tum_Latn    | Tumbuka
tur_Latn    | Turkish
twi_Latn    | Twi
tzm_Tfng    | Central Atlas Tamazight
uig_Arab    | Uyghur
ukr_Cyrl    | Ukrainian
umb_Latn    | Umbundu
urd_Arab    | Urdu
uzn_Latn    | Northern Uzbek
vec_Latn    | Venetian
vie_Latn    | Vietnamese
war_Latn    | Waray
wol_Latn    | Wolof
xho_Latn    | Xhosa
ydd_Hebr    | Eastern Yiddish
yor_Latn    | Yoruba
yue_Hant    | Yue Chinese
zho_Hans    | Chinese (Simplified)
zho_Hant    | Chinese (Traditional)
zsm_Latn    | Standard Malay
zul_Latn    | Zulu
"""

l = langlist_str.split("\n")
langlist = []
for k in l:
    if k != "":
        langlist.append(k[0:8])

#print(langlist)


cuda_opt = -1
to_device = "cpu"
# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "NLLB Translate with CTranslate2", # name
        "version": "2.0", # version

        "translate": {
            "fb_nllb_ctranslate2": (init,translate) # 1 function - init, 2 - translate
        },

        "default_options": {
            "model": "facebook/nllb-200-distilled-600M",  # key model
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
        #to_device = "cuda:{0}".format(cuda_opt)
        to_device = "cuda".format(cuda_opt)
    pass

def init(core:OneRingCore):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    import ctranslate2
    global model

    #print(to_device)
    #model = AutoModelForSeq2SeqLM.from_pretrained(core.plugin_options(modname).get("model")).to(to_device)
    model = ctranslate2.Translator(core.plugin_options(modname).get("model"), device=to_device)

    pass

def convert_lang(input_lang:str) -> str:
    if len(input_lang) == 2 or len(input_lang) == 3:
        if input_lang == "en" or input_lang == "eng":
            return "eng_Latn"
        if input_lang == "ru":
            return "rus_Cyrl"

        for lang in langlist:
            if lang.startswith(input_lang):
                return lang

    else:
        return input_lang

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    from_lang_tr = convert_lang(from_lang)
    to_lang_tr = convert_lang(to_lang)
    if tokenizers.get(from_lang_tr) is None:
        tokenizers[from_lang_tr] = AutoTokenizer.from_pretrained(core.plugin_options(modname).get("model"), src_lang=from_lang_tr)
    # if tokenizers.get(to_lang_tr) is None:
    #     tokenizers[to_lang_tr] = AutoTokenizer.from_pretrained(core.plugin_options(modname).get("model"), src_lang=to_lang_tr)

    tokenizer_from = tokenizers.get(from_lang_tr)
    #source = tokenizer_from(text, return_tensors="pt").to(to_device)
    source = tokenizer_from.convert_ids_to_tokens(tokenizer_from.encode(text))

    #source = tokenizer.convert_ids_to_tokens(tokenizer.encode("Hello world!"))
    target_prefix = [to_lang_tr]
    results = model.translate_batch([source], target_prefix=[target_prefix])
    translated_tokens = results[0].hypotheses[0][1:]

    #res = tokenizer_from.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    res = tokenizer_from.decode(tokenizer_from.convert_tokens_to_ids(translated_tokens))



    return res

