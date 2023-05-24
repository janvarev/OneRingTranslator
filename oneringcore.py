from jaa import JaaCore

from termcolor import colored, cprint

version = "2.2.0"

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
            # alreaduy inited
            return

        try:
            self.print_blue("TRY: init translation plugin '{0}'...".format(translator_engine))
            self.translators[translator_engine][0](self)
            self.inited_translator_engines.append(translator_engine)
            self.print_blue("SUCCESS: '{0}' inited!".format(translator_engine))

        except Exception as e:
            self.print_error("Error init translation plugin {0}...".format(translator_engine), e)


