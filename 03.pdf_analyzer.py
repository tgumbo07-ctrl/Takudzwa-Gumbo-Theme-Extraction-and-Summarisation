# --- PDF ANALYSIS SCRIPT ---
# This script extracts text from the merged PDF, performs theme extraction (BERTopic),
# and generates a structured report mirroring the requested format.

from pypdf import PdfReader
import nltk
from nltk.tokenize import sent_tokenize
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from IPython.display import display, HTML
import os
import datetime # Import for generating the timestamp

# ----------------------------------------------------
# ⚠️ Ensure this path matches the output from the merger script!
# ----------------------------------------------------
PDF_FOLDER_PATH = '/content/drive/MyDrive/Deep Learning/pdf_files'
MERGED_PDF_FILENAME = "merged_document_for_analysis.pdf"
MERGED_PDF_FULLPATH = os.path.join(PDF_FOLDER_PATH, MERGED_PDF_FILENAME)
# ----------------------------------------------------

print("\n--- Starting Text Extraction and Theme Analysis ---")

# 1. Extract text from the merged PDF
raw_text = ""
total_pages = 0
try:
    with open(MERGED_PDF_FULLPATH, "rb") as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                raw_text += page_text + " "

    raw_text = raw_text.replace('\n', ' ')
    char_count = len(raw_text)
    word_count = len(raw_text.split())

    print(f"✅ Text extracted successfully. Total characters: {char_count}")
except FileNotFoundError:
    raw_text = None
    print(f"❌ File not found at {MERGED_PDF_FULLPATH}. Please run the merging script first.")
except Exception as e:
    raw_text = None
    print(f"❌ Error during text extraction: {e}")

# 2. Theme Extraction and Summarization
if raw_text is None or not raw_text.strip():
    print("\n❌ Cannot proceed to theme analysis. Extracted content is empty.")
else:
    # --- FIX: Download all required NLTK resources to prevent LookupError ---
    print("\nAttempting to download required NLTK tokenizers...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        print("✅ NLTK dependencies installed/verified.")
    except Exception as e:
        print(f"❌ NLTK download failed: {e}. Cannot proceed with analysis.")
        raw_text = None

if raw_text is not None:
    # A. Sentence Tokenization
    sentences = [s.strip() for s in sent_tokenize(raw_text) if len(s.strip()) > 30]

    if not sentences:
        print("\n❌ ERROR: Could not find any meaningful sentences in the text (too short or poorly formatted).")
    else:
        print(f"\n--- Starting Theme Modeling (BERTopic) ---")
        print(f"Total sentences for analysis: {len(sentences)}")

        # B. BERTopic Theme Extraction
        vectorizer_model = CountVectorizer(stop_words="english")
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer_model,
            min_topic_size=15,
            n_gram_range=(1, 2),
            verbose=False
        )

        topics, _ = topic_model.fit_transform(sentences)
        topic_info = topic_model.get_topic_info()

        # C. Extractive Summarization (for Executive Summary)
        summary_sentences = []
        top_topics = topic_info[topic_info['Topic'] != -1]['Topic'].head(3)

        if not top_topics.empty:
            for topic_id in top_topics:
                rep_docs = topic_model.get_representative_docs(topic_id)
                summary_sentences.extend(rep_docs[:2])

            executive_summary = " ".join(summary_sentences)
        else:
            executive_summary = "The analysis could not identify distinct, strong themes to generate a comprehensive executive summary."

        # --------------------------------------------------------------
        # --- GENERATING STRUCTURED REPORT OUTPUT (Similar to DOCX) ----
        # --------------------------------------------------------------

        report_output = f"""
        <div style="font-family: Arial, sans-serif; max-width: 900px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h1 style="text-align: center; color: #1e40af; border-bottom: 2px solid #1e40af; padding-bottom: 10px;">COMPREHENSIVE DOCUMENT ANALYSIS</h1>

            <div style="background-color: #f4f6ff; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <h2 style="color: #3b82f6; font-size: 1.5em; margin-top: 0;">AI-Generated Fact-Based Summary</h2>
                <p><strong>Source Document:</strong> {MERGED_PDF_FILENAME}</p>
                <p><strong>Total Pages Analyzed:</strong> {total_pages}</p>
                <p><strong>Total Estimated Words:</strong> {word_count}</p>
                <p><strong>Generated:</strong> {datetime.datetime.now().strftime("%B %d, %Y at %H:%M %p")}</p>
                <p><strong>Method:</strong> Advanced BERTopic Neural Topic Modeling & Extractive Summarization</p>
            </div>

            <h2 style="color: #1e40af; margin-top: 30px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;">EXECUTIVE SUMMARY</h2>
            <p style="line-height: 1.6; text-align: justify;">
                This document presents a comprehensive AI-generated analysis of the merged research material. The key findings, extracted via semantic analysis, suggest that the core content is centered around the following major themes (see detailed section below).

                The most representative statements extracted from the leading thematic areas are:

                <em style="display: block; margin: 10px 0; padding: 10px; border-left: 3px solid #3b82f6; background-color: #e0f2fe;">"{executive_summary}"</em>
            </p>

            <h2 style="color: #1e40af; margin-top: 30px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;">KEY FINDINGS OVERVIEW</h2>
            <p>The analysis of the content revealed <strong>{len(top_topics)}</strong> major thematic areas (excluding outliers) and <strong>{len(sentences)}</strong> meaningful sentences were used for modeling.</p>
            <p><strong>Most Frequent Meaningful Themes (Top 10):</strong></p>
            <ul style="list-style-type: none; padding-left: 0;">
                {[f'<li style="margin-bottom: 5px; background-color: #f7f7f7; padding: 5px; border-radius: 4px;"><strong>Topic {row["Topic"]} ({row["Count"]} times)</strong>: {row["Name"]} (Keywords: {", ".join(row["Representation"])})</li>' for index, row in topic_info.head(10).iterrows()]}
            </ul>

            <h2 style="color: #1e40af; margin-top: 30px; border-bottom: 1px dashed #ccc; padding-bottom: 5px;">METHODOLOGY NOTES</h2>
            <p style="line-height: 1.6; text-align: justify;">
                The thematic analysis utilized the <strong>BERTopic</strong> framework. This technique leverages transformer-based embeddings (specifically <strong>all-MiniLM-L6-v2</strong>) to map document segments (sentences) into a semantic space. It then uses UMAP for dimensionality reduction and HDBSCAN for clustering to identify dense clusters, which represent the themes. The model employs a c-TF-IDF score to determine the most representative words for each cluster (theme), thus providing the Theme Label and Keywords. This analysis specifically avoided common stop words to ensure the identified themes focus on the core research substance.
            </p>

        </div>
        """

        print("\n" + "="*80)
        print("✅ THEME EXTRACTION COMPLETE - REPORT GENERATED")
        print("="*80)

        # Display the formatted report
        display(HTML(report_output))

        print("\n" + "="*80)
