from oneringcore import OneRingCore

core = OneRingCore()
core.init_with_plugins()

res = core.translate("Hello! How are you?", "en", "ru", "openrouter_chat")

print(res.get("result"))