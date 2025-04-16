from transformers import pipeline

# Load BART model for summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_len=512):
    if len(text) > 1024:
        text = text[:1024]
    summary = summarizer(text, max_length=max_len, min_length=30, do_sample=False)
    return summary[0]['summary_text']
