# API example usage

Translate from en to fr
```
http://127.0.0.1:4990/translate?text=Hi%21&from_lang=en&to_lang=fr
```

Translate from en to user language (user language defines in plugins/core.json)
```
http://127.0.0.1:4990/translate?text=Hi%21&from_lang=en&to_lang=user
```

Full Python usage example:
```python
custom_url = params['custom_url']
if custom_url == "":
    res = "Please, setup custom_url for OneRingTranslator (usually http://127.0.0.1:4990/)"
else:
    import requests
    response_orig = requests.get(f"{custom_url}translate", params={"text":string,"from_lang":from_lang,"to_lang":to_lang})
    if response_orig.status_code == 200:
        response = response_orig.json()
        #print("OneRingTranslator result:",response)

        if response.get("error") is not None:
            print(response)
            res = "ERROR: "+response.get("error")
        elif response.get("result") is not None:
            res = response.get("result")
        else:
            print(response)
            res = "Unknown result from OneRingTranslator"
    elif response_orig.status_code == 404:
        res = "404 error: can't find endpoint"
    elif response_orig.status_code == 500:
        res = "500 error: OneRingTranslator server error"
    else:
        res = f"{response_orig.status_code} error"
```
