async function translateText() {
  const myElement = document.getElementById('progress');

  const textToTranslate = document.getElementById('text_to_translate').value;
  const fromLang = document.getElementById('from_lang').value;
  const toLang = document.getElementById('to_lang').value;
  const plugin = document.getElementById('plugin').value;
  const apiKey = document.getElementById('api_key').value;
  const addParams = document.getElementById('add_params').value;

  myElement.style.display = 'inline';

  const params = new URLSearchParams({ text: textToTranslate, from_lang: fromLang, to_lang: toLang,
        translator_plugin: plugin, api_key: apiKey, add_params: addParams});
  const response = await fetch(`/translate?${params}`);
  const data = await response.json();



  const translation = data.result;
  document.getElementById('text_result').value = translation;

  myElement.style.display = 'none';

  return translation;
}



window.onload = () => {
    const trigger = document.getElementById('trigger');
    trigger.onmouseup = () => {
        //trigger.disabled = true;
        translateText();
    };
}