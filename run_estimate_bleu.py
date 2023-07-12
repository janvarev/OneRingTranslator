from nltk.translate.bleu_score import sentence_bleu

# ----------
from oneringcore import OneRingCore

# ----------------- key settings params ----------------
BLEU_PAIRS = "fra->eng,eng->fra,rus->eng,eng->rus" # pairs of language in terms of FLORES dataset https://huggingface.co/datasets/gsarti/flores_101/viewer
BLEU_PAIRS_2LETTERS = "fr->en,en->fr,ru->en,en->ru" # pairs of language codes that will be passed to plugin (from_lang, to_lang params)

#BLEU_PLUGINS = "no_translate,google_translate,fb_nllb_translate" # plugins to estimate
BLEU_PLUGINS = "no_translate,google_translate" # plugins to estimate

BLEU_NUM_PHRASES = 100 # num of phrases to estimate. Between 1 and 100 for now.
BLEU_START_PHRASE = 150 # offset from FLORES dataset to get NUM phrases

BLEU_METRIC = "bleu" # bleu | comet

core:OneRingCore = None

def load_dataset(lang, split, start, num):
    import requests
    req_url = f"https://datasets-server.huggingface.co/rows?dataset=gsarti%2Fflores_101&config={lang}&split={split}&offset={start}&limit={num}"
    #print(req_url)
    #return ""
    r = requests.get(req_url)
    if r.status_code != 200:
        print(f"Error {r.status_code} during get dataset {req_url}")
        quit()
    j = r.json()
    #return j["rows"]

    # we have problems with NUM param when getting results from server, so try to fix it
    rows = j["rows"]
    if len(rows) > num:
        rows = rows[:num]

    return rows




def translate(text:str, from_lang:str = "", to_lang:str = "", translator_plugin:str = "", add_params:str = ""):

    res = core.translate(text,from_lang,to_lang,translator_plugin,add_params)

    if res.get("error") is not None:
        raise ValueError("Error in translate: "+res.get("error"))

    return res.get("result"), res.get("cache")

if __name__ == "__main__":
    from tqdm import trange
    import tqdm
    #multiprocessing.freeze_support()
    core = OneRingCore()
    core.init_with_plugins()

    pairs_ar = BLEU_PAIRS.split(",")
    pairs_ar2 = BLEU_PAIRS_2LETTERS.split(",")
    bleu_plugins_ar = BLEU_PLUGINS.split(",")

    table_bleu = [([bleu_plugins_ar[i]] + (["-"] * len(pairs_ar))) for i in range(len(bleu_plugins_ar))]

    if BLEU_METRIC == "comet":
        from comet import download_model, load_from_checkpoint
        print("Activating COMET model...")
        model_path = download_model("Unbabel/wmt22-comet-da")
        model = load_from_checkpoint(model_path)
        print("COMET model activated!")

    for j in range(len(pairs_ar)):
        pair = pairs_ar[j]
        pair2 = pairs_ar2[j]

        from_lang, to_lang = pair.split("->")
        from_lang_let2, to_lang_let2 = pair2.split("->") # we usually needs 2letter lang codes to transfer to plugins


        from_lines = load_dataset(from_lang, "devtest", BLEU_START_PHRASE, BLEU_NUM_PHRASES)
        to_lines = load_dataset(to_lang, "devtest", BLEU_START_PHRASE, BLEU_NUM_PHRASES)

        for k in range(len(bleu_plugins_ar)):
            plugin = bleu_plugins_ar[k]

            #print(f"--------------\n{plugin} plugin\n--------------\n")

            bleu_sum = 0.0
            bleu_cnt = 0
            print(f"---- Estimating {plugin} for pair {pair}....")
            tqdm_bar = trange(len(from_lines))

            data_comet = []

            for i in tqdm_bar: # tqdm range
                text_need_translate = from_lines[i]["row"]["sentence"]
                text_reference = to_lines[i]["row"]["sentence"]
                text_candidate, is_from_cache = translate(text_need_translate,from_lang_let2,to_lang_let2, plugin)

                if BLEU_METRIC == "bleu":
                    score = sentence_bleu([text_reference.strip().split()],text_candidate.strip().split(),weights=(0.5, 0.5))

                    bleu_sum += score
                    bleu_cnt += 1

                    tqdm_bar.set_description(
                        f"'{plugin}' on '{pair}' pair average {BLEU_METRIC.upper()} score: {'{:8.2f}'.format(bleu_sum * 100 / bleu_cnt)}")
                elif BLEU_METRIC == "comet":
                    data_comet.append(
                        {
                            "src": text_need_translate,
                            "mt": text_candidate,
                            "ref": text_reference
                        }
                    )
                    #score_pred = model.predict(data, batch_size=8, gpus=0)
                    #print(score_pred)
                    tqdm_bar.set_description(
                        f"'{plugin}' on '{pair}' pair, {BLEU_METRIC.upper()} score, getting translations...: ")
                #print(f"Original: {text_need_translate}\nTranslation: {text_candidate}\nReference: {text_reference}\nScore: {score}\n\n")


                # on some web plugin and not from cache result we need delay
                # (cache results must pass without delay)
                if plugin == "openai_chat" and not is_from_cache:
                    import time
                    import random
                    time.sleep(20 + random.random()*3)

            if BLEU_METRIC == "bleu":
                bleu_score = bleu_sum / len(from_lines)

            elif BLEU_METRIC == "comet":
                print("Calculating COMET model...")
                score_pred = model.predict(data_comet, batch_size=8, gpus=0)
                #print(score_pred)

                bleu_score = score_pred.get("system_score")

            print(f"****** Average {BLEU_METRIC.upper()} score for '{plugin}' on '{pair.upper()}' pair ({len(to_lines)} samples): {bleu_score}")

            table_bleu[k][j+1] = "{:8.2f}".format(bleu_score*100)

    from tabulate import tabulate
    res_print_table = tabulate(table_bleu,headers=[" "*60]+pairs_ar,tablefmt="github")

    print("*" * 60)
    print(f"{BLEU_METRIC.upper()} scores")
    print("*" * 60)
    print(res_print_table)

