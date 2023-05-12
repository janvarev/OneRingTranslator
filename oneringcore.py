from jaa import JaaCore

from termcolor import colored, cprint

version = "1.2.0"

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


