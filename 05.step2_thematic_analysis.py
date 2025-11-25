#!/usr/bin/env python3
"""
STEP 2/3: Loads extracted text, performs BERTopic neural topic modeling,
and saves the thematic analysis results to 'analysis_data_step2.pkl'.
"""
import pickle
import nltk
from nltk.tokenize import sent_tokenize
import os
import datetime

# Try to import necessary libraries, installing them if missing
try:
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import CountVectorizer
except ImportError:
    print("Installing required libraries (bertopic, sentence-transformers, sklearn)...")
    !pip install bertopic sentence-transformers umap-learn hdbscan
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer
    from sklearn.feature_extraction.text import CountVectorizer

# --- Input/Output Files ---
INPUT_DATA_FILE = 'analysis_data_step1.pkl'
OUTPUT_DATA_FILE = 'analysis_data_step2.pkl'

print("\n--- Starting Thematic Analysis (STEP 2/3) ---")

# 1. Load data from Step 1
try:
    with open(INPUT_DATA_FILE, 'rb') as f:
        data = pickle.load(f)
        raw_text = data['raw_text']
        metadata = data
    print(f"✅ Extracted data loaded successfully from '{INPUT_DATA_FILE}'.")
except FileNotFoundError:
    print(f"❌ Input file '{INPUT_DATA_FILE}' not found. Please run '01_extraction.py' first.")
    exit()
except Exception as e:
    print(f"❌ Error loading data: {e}")
    exit()

if not raw_text or not raw_text.strip():
    print("❌ Cannot proceed to theme analysis. Extracted content is empty.")
    exit()

# --- FIX: Download all required NLTK resources to prevent LookupError ---
print("Attempting to download required NLTK tokenizers...")
try:
    nltk.download('punkt', quiet=True)
    print("✅ NLTK dependencies installed/verified.")
except Exception as e:
    print(f"❌ NLTK download failed: {e}. Cannot proceed with analysis.")
    exit()

# A. Sentence Tokenization
sentences = [s.strip() for s in sent_tokenize(raw_text) if len(s.strip()) > 30]

if not sentences:
    print("\n❌ ERROR: Could not find any meaningful sentences in the text (too short or poorly formatted).")
    exit()

print(f"Total sentences for modeling: {len(sentences):,}")

# B. BERTopic Theme Extraction
print("\nInitiating BERTopic Model training (this may take a few minutes for large documents)...")
vectorizer_model = CountVectorizer(stop_words="english")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

topic_model = BERTopic(
    embedding_model=embedding_model,
    vectorizer_model=vectorizer_model,
    min_topic_size=15,
    n_gram_range=(1, 2),
    verbose=False
)

# Fit model to sentences
topics, _ = topic_model.fit_transform(sentences)
topic_info = topic_model.get_topic_info()

# C. Extractive Summarization (for Executive Summary)
summary_sentences = []
# Try to grab representative docs from the top 3 NON-OUTLIER topics
top_topics = topic_info[topic_info['Topic'] != -1]['Topic'].head(3)

if not top_topics.empty:
    for topic_id in top_topics:
        rep_docs = topic_model.get_representative_docs(topic_id)
        summary_sentences.extend(rep_docs[:2])

    executive_summary = " ".join(summary_sentences)
else:
    executive_summary = "The analysis could not identify distinct, strong themes to generate a comprehensive extractive summary. The document appears to lack clear, repeating thematic structures, or the content is highly varied."

print("\n" + "="*80)
print("✅ THEME EXTRACTION COMPLETE - Results Summary:")
print(f"Identified {len(topic_info) - 1} distinct themes.")
print(f"Top Theme: {topic_info.iloc[0]['Name']} (Count: {topic_info.iloc[0]['Count']})")
print("="*80)

# 3. Save the full analysis data for the report
report_data = {
    'executive_summary': executive_summary,
    'topic_info': topic_info,
    'sentences_analyzed': len(sentences),
    # Merge metadata from step 1
    **metadata
}

with open(OUTPUT_DATA_FILE, 'wb') as f:
    pickle.dump(report_data, f)

print(f"✅ Analysis results saved successfully to '{OUTPUT_DATA_FILE}' for the final report.")
