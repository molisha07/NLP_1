import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
# import shutil  # No longer needed
# shutil.rmtree('C:/Users/HP/nltk_data', ignore_errors=True)  # Remove this line

def summarize_text(text, max_sentences=3):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    word_frequencies = {}

    for word in words:
        if word.lower() not in stop_words and word.isalnum():
            word_frequencies[word.lower()] = word_frequencies.get(word.lower(), 0) + 1

    sentence_scores = {}
    sentences = sent_tokenize(text)

    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(" ")) < 30:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    summary_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

# Streamlit UI
st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("📝 Text Summarizer")
st.write("Enter any long paragraph or article to get a short summary.")

text_input = st.text_area("Paste your text here:", height=250)
max_sentences = st.slider("Select number of sentences for summary", 1, 10, 3)

if st.button("Summarize"):
    if text_input.strip():
        summary = summarize_text(text_input, max_sentences)
        st.subheader("Summary:")
        st.success(summary)
    else:
        st.warning("Please enter text to summarize.")
