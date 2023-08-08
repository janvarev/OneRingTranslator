## Installation and run

### Install 
- If you're on Windows, you can use **fast one click installer**: Go here: https://github.com/janvarev/OneRingTranslator-installer and follow instructions.
  - If you **plan to use offline translation plugins**, please choose B on install query and install "torch" packet.  
- If you're on other system   
  - Install python 3.10.x (if needed)
  - Install requirements by cmd ```pip install -r requirements.txt```
  - If you plan to use offline translation ```pip install -r requirements-offline.txt```

### Run
- If you've used one click installer for Windows just run `start-webapi.bat`
- If you are on other system, run `run_webapi.py`

### Fast configuration for online translation

If you're ok to use **online** translation:

**Congratulations, you're done!** By default OneRingTranslator just transfer your calls to Google Translate. 

Visit docs and simple Web interface: http://127.0.0.1:4990/

### Fast configuration for offline translation

If you plan to use **offline** translation:
- Run webapi at least one time.
- Open file `options/core.json`
- Set `"default_translate_plugin": "fb_nllb_translate"`, `"allow_multithread": false,`  and save file 
- Run. During the first run neuronet model will be downloaded from huggingface hub, it takes time

- **You're done!**

Visit docs and simple Web interface: http://127.0.0.1:4990/
