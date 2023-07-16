from typing import Optional

from jaa import JaaCore

from termcolor import colored, cprint
import os
import json

version = "6.1.0"

class OneRingCore(JaaCore):
    def __init__(self):
        JaaCore.__init__(self)

        self.translators:dict = {
        }

        self.default_translator:str = ""
        self.default_from_lang:str = ""
        self.default_to_lang:str = ""

        self.api_keys_allowed:list = []

        self.is_debug_input_output:bool = False
        self.is_multithread:bool = True

        self.user_lang:str = ""

        self.cache_is_use = False
        self.cache_save_every = 5
        self.cache_per_model = True

        self.cache_dict:dict[str,dict[str,str]] = {}

        self.inited_translator_engines = []

        self.dict_lang_to_2let = {'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar', 'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be', 'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN', 'Chinese (Traditional)': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr', 'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en', 'Esperanto': 'eo', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr', 'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de', 'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha', 'Hawaiian': 'haw', 'Hebrew': 'iw', 'Hindi': 'hi', 'Hmong': 'hmn', 'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id', 'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jw', 'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo', 'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb', 'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml', 'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn', 'Myanmar (Burmese)': 'my', 'Nepali': 'ne', 'Norwegian': 'no', 'Nyanja (Chichewa)': 'ny', 'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese (Portugal, Brazil)': 'pt', 'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm', 'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn', 'Sindhi': 'sd', 'Sinhala (Sinhalese)': 'si', 'Slovak': 'sk', 'Slovenian': 'sl', 'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw', 'Swedish': 'sv', 'Tagalog (Filipino)': 'tl', 'Tajik': 'tg', 'Tamil': 'ta', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh', 'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'}
        self.dict_2let_to_lang = {}
        for i in self.dict_lang_to_2let.keys():
            self.dict_2let_to_lang[self.dict_lang_to_2let[i]] = i

    # ----------- process plugins functions ------
    def process_plugin_manifest(self, modname, manifest):
        # is req online?
        # adding tts engines from plugin manifest
        if "translate" in manifest:  # process commands
            for cmd in manifest["translate"].keys():
                self.translators[cmd] = manifest["translate"][cmd]

        return manifest

    def init_with_plugins(self):
        self.init_plugins(["core"])
        #self.init_plugins()
        self.display_init_info()

        self.init_translator_engine(self.default_translator)

    # ------------ formatting stuff -------------------
    def display_init_info(self):
        cprint("OneRingCore v{0}:".format(version), "blue", end=' ')
        self.format_print_key_list("translate engines", self.translators.keys())
        print("Default translator:",self.default_translator)

    def format_print_key_list(self, key:str, value:list):
        print(colored(key+": ", "blue")+", ".join(value))

    def print_error(self,err_txt,e:Exception = None):
        cprint(err_txt,"red")
        # if e != None:
        #     cprint(e,"red")
        import traceback
        traceback.print_exc()

    def print_red(self,txt):
        cprint(txt,"red")

    def print_blue(self, txt):
        cprint(txt, "blue")

    # ---------------- init translation stuff ----------------
    def init_translator_engine(self, translator_engine:str):

        if translator_engine in self.inited_translator_engines:
            # already inited
            return

        try:
            self.print_blue("TRY: init translation plugin '{0}'...".format(translator_engine))
            self.translators[translator_engine][0](self)
            self.inited_translator_engines.append(translator_engine)
            self.print_blue("SUCCESS: '{0}' inited!".format(translator_engine))

        except Exception as e:
            self.print_error("Error init translation plugin {0}...".format(translator_engine), e)

    def translate(self, text:str, from_lang:str = "", to_lang:str = "", translator_plugin:str = "", add_params:str = ""):
        if self.is_debug_input_output:
            print("Input: {0}".format(text))


        if translator_plugin == "":
            translator_plugin = self.default_translator

        if from_lang == "":
            from_lang = self.default_from_lang

        if to_lang == "":
            to_lang = self.default_to_lang

        if from_lang == "user":
            from_lang = self.user_lang
            if self.user_lang == "":
                return {"error": "user_lang is blank. Please, setup it in options/core.json file"}

        if to_lang == "user":
            to_lang = self.user_lang
            if self.user_lang == "":
                return {"error": "user_lang is blank. Please, setup it in options/core.json file"}

        cache_id = self.cache_calc_id(from_lang,to_lang,translator_plugin)
        if self.cache_is_use:
            cache_res = self.cache_get(text,cache_id)
            if cache_res is not None:
                if self.is_debug_input_output:
                    print("Output from CACHE: {0}".format(cache_res))
                return {"result": cache_res, "cache": True}

        # init after cache
        if translator_plugin != "":
            self.init_translator_engine(translator_plugin)

            if translator_plugin not in self.inited_translator_engines:
                return {"error": "Translator plugin not inited"}


        res = self.translators[translator_plugin][1](self, text, from_lang, to_lang, add_params)

        if self.is_debug_input_output:
            print("Output: {0}".format(res))

        if self.cache_is_use:
            self.cache_set(text,cache_id,res)

        return {"result": res, "cache": False}

    # -------------- caching functions ----------------
    def cache_calc_id(self, from_lang:str, to_lang:str, translator_plugin:str) -> str:
        res = translator_plugin+"__"+from_lang+"__"+to_lang
        #print(self.cache_per_model)
        if self.cache_per_model:
            # params = self.plugin_manifest(translator_plugin)
            # if params is not None:
            options = self.plugin_options("plugin_"+translator_plugin)
            #print(translator_plugin,options)
            if options is not None:
                model = options.get("model")
                if model is not None:
                    model_normalized = str(model).replace("/","_").replace("\\","_").replace(":","_")
                    res += "__"+model_normalized
        return res

    def cache_calc_filepath(self, cache_id:str) -> str:
        return os.path.dirname(__file__)+os.path.sep+"cache"+os.path.sep+cache_id+".json"

    def cache_load_if_not_exists(self, cache_id:str):
        if self.cache_dict.get(cache_id) is None:
            if os.path.exists(self.cache_calc_filepath(cache_id)):
                with open(self.cache_calc_filepath(cache_id), 'r', encoding="utf-8") as f:
                    # Load the JSON data from the file into a Python dictionary
                    data = json.load(f)

                    self.cache_dict[cache_id] = data
            else:
                self.cache_dict[cache_id] = {}
    def cache_get(self, text:str, cache_id:str) -> Optional[str]:
        self.cache_load_if_not_exists(cache_id)

        return self.cache_dict.get(cache_id).get(text)

    def cache_set(self, text:str, cache_id:str, text_translated:str):
        self.cache_load_if_not_exists(cache_id)

        self.cache_dict[cache_id][text] = text_translated

        #print(cache_id,self.cache_dict[cache_id])

        if len(self.cache_dict[cache_id]) % self.cache_save_every == 0:
            self.cache_save(cache_id)
            #print("saved!")

    def cache_save(self, cache_id:str):
        with open(self.cache_calc_filepath(cache_id), 'w', encoding="utf-8") as f:
            json.dump(self.cache_dict[cache_id], f, indent=2, ensure_ascii=False)

