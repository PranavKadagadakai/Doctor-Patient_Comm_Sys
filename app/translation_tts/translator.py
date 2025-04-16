from transformers import MarianMTModel, MarianTokenizer

model_cache = {}

def load_model(src_lang, tgt_lang):
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    if model_name not in model_cache:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        model_cache[model_name] = (tokenizer, model)
    return model_cache[model_name]

def translate_text(text, target_lang, source_lang='en'):
    tokenizer, model = load_model(source_lang, target_lang)
    tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt")
    translation = model.generate(**tokens)
    return tokenizer.decode(translation[0], skip_special_tokens=True)
