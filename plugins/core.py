# Core plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore

# start function
def start(core:OneRingCore):
    manifest = {
        "name": "Core plugin",
        "version": "1.0",

        "default_options": {
            "default_translate_plugin": "google_translate", # default translation engine
            "default_from_lang": "es", # default from language
            "default_to_lang": "en", # default to language
            "api_keys_allowed": [], # set of API keys. If empty - no API key required.
            "debug_input_output": False, # allow debug print input and output in console
            "allow_multithread": True # allow multithread run of translation engine
        },

    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    #print(manifest["options"])
    options = manifest["options"]

    core.default_translator = options["default_translate_plugin"]
    core.default_from_lang = options["default_from_lang"]
    core.default_to_lang = options["default_to_lang"]
    core.api_keys_allowed = options["api_keys_allowed"]

    core.is_multithread = options["allow_multithread"]
    core.is_debug_input_output = options["debug_input_output"]

    return manifest
