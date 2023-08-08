# Multisources
# gain translations from different sources and try to select one best
# author: Vladislav Janvarev
import asyncio

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Multi sources plugin", # name
        "version": "1.3", # version

        # this is DEFAULT options
        # ACTUAL options is in options/<plugin_name>.json after first run
        "default_options": {
            "model": "google_translate,deepl",  # plugins that will be processed
            "min_symbols_to_full_model": 30,
            "min_plugin": "google_translate", # if symbols less than min, this will be used
            "multithread_model": True, # use this if you use different plugins in model - this speedup by multithread tasks
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

async def run_list(tasks_lists):
    return await asyncio.gather(*tasks_lists)
def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    plugins: str = core.plugin_options(modname).get("model").split(",")

    min_plugin: str = core.plugin_options(modname).get("min_plugin")
    min_symbols: int = core.plugin_options(modname).get("min_symbols_to_full_model")
    is_multithread_model: bool = core.plugin_options(modname).get("multithread_model")
    #print(len(text), min_symbols)
    if len(text) < min_symbols:
        res_text = core.translate(text, from_lang, to_lang, min_plugin, add_params).get("result")
        print(f"Min transl {min_plugin}: {res_text}")
        return res_text


    data0 = []
    if not is_multithread_model:
        data0 = []
        for plugin in plugins:
            data0.append(core.translate(text,from_lang,to_lang,plugin))
    else:
        # ---------- async version - not work inside FastAPI

        # data_async_tasks = []
        # for plugin in plugins:
        #     data_async_tasks.append(asyncio.to_thread(core.translate, text, from_lang, to_lang, plugin,
        #                               add_params))
        #
        # #data0 = asyncio.run(run_list(data_async_tasks))
        # loop = asyncio.new_event_loop()
        # data0 = loop.run_until_complete(run_list(data_async_tasks))

        # ----------- multithread version -----------

        import concurrent.futures

        data0 = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(core.translate, text, from_lang, to_lang, plugin) for plugin in plugins]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                data0.append(result)


    data = []
    for mt_res in data0:
        data.append({"src":text,"mt":mt_res.get("result")})

    #print(data)

    pred = core.comet_model_multi_sources.predict(data, batch_size=8, gpus=0)
    #print(model_output)
    scores = pred.get("scores")

    max_ind = scores.index(max(scores))
    #print('Scores:',scores, max_ind)


    return data[max_ind]["mt"]
