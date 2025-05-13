import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import nltk

nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(text, max_sentences=3):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    word_frequencies = {}

    for word in words:
        if word.lower() not in stop_words and word.isalnum():
            if word.lower() not in word_frequencies.keys():
                word_frequencies[word.lower()] = 1
            else:
                word_frequencies[word.lower()] += 1

    sentence_scores = {}
    sentences = sent_tokenize(text)

    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_scores:
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

    summary_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary

# Streamlit Interface
st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("Text Summarizer App")
st.write("Enter any long paragraph or article to get a short summary.")

text_input = st.text_area("Paste your text here...", height=250)
max_sentences = st.slider("Select number of sentences for summary", 1, 10, 3)

if st.button("Summarize"):
    if text_input.strip():
        summary = summarize_text(text_input, max_sentences)
        st.subheader("Summary:")
        st.success(summary)
    else:
        st.warning("Please paste some text to summarize.")