# Core plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore

# start function
def start(core:OneRingCore):
    manifest = {
        "name": "Core plugin",
        "version": "1.4",

        # this is DEFAULT options
        # ACTUAL options located in options/<plugin_name>.json after first run
        "default_options": {
            "default_translate_plugin": "google_translate", # default translation engine
            "default_from_lang": "es", # default from language
            "default_to_lang": "en", # default to language
            "api_keys_allowed": [], # set of API keys. If empty - no API key required.
            "debug_input_output": False, # allow debug print input and output in console
            "allow_multithread": True, # allow multithread run of translation engine
            "user_lang": "", # standart user language. Replaces "user" in to_lang or from_lang API params
            "cache_is_use": True, # use cache?
            "cache_save_every": 5,  # every X elements save cache to disk
            "cache_per_model": True, # differentiate cache per model
            "default_translate_router": { # routing for default translation engine on different language pairs
                "fr->es": "no_translate", # this is just an example, adjust in to your needs
                "fr->fn": "no_translate2",
            }
        },

    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    #print(manifest["options"])
    options = manifest["options"]

    core.default_translator = options["default_translate_plugin"]
    core.default_from_lang = options["default_from_lang"]
    core.default_to_lang = options["default_to_lang"]
    core.default_translate_router = options["default_translate_router"]

    core.api_keys_allowed = options["api_keys_allowed"]

    core.is_multithread = options["allow_multithread"]
    core.is_debug_input_output = options["debug_input_output"]

    core.user_lang = options["user_lang"]

    core.cache_is_use = options["cache_is_use"]
    core.cache_save_every = options["cache_save_every"]
    core.cache_per_model = options["cache_per_model"]

    return manifest
