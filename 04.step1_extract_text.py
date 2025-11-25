#!/usr/bin/env python3
"""
STEP 1/3: Extracts text content and calculates metrics from the merged PDF.
Saves the results to 'analysis_data_step1.pkl'.
"""
from pypdf import PdfReader
import os
import pickle
import datetime

# --- Global Configuration ---
# ⚠️ Adjust this path if your merged PDF is located elsewhere!
PDF_FOLDER_PATH = '/content/drive/MyDrive/Deep Learning/pdf_files'
MERGED_PDF_FILENAME = "merged_document_for_analysis.pdf"
MERGED_PDF_FULLPATH = os.path.join(PDF_FOLDER_PATH, MERGED_PDF_FILENAME)
# --- Output File ---
OUTPUT_DATA_FILE = 'analysis_data_step1.pkl'

print("\n--- Starting Text Extraction (STEP 1/3) ---")

raw_text = ""
total_pages = 0
word_count = 0
char_count = 0

try:
    # 1. Extract text from the merged PDF
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

    print(f"✅ Text extracted successfully from {total_pages:,} pages.")
    print(f"   Total estimated words: {word_count:,}")

    # 2. Save the extracted data
    analysis_data = {
        'raw_text': raw_text,
        'total_pages': total_pages,
        'word_count': word_count,
        'char_count': char_count,
        'timestamp': datetime.datetime.now().strftime("%B %d, %Y at %H:%M %p")
    }

    with open(OUTPUT_DATA_FILE, 'wb') as f:
        pickle.dump(analysis_data, f)

    print(f"✅ Data saved successfully to '{OUTPUT_DATA_FILE}' for the next step.")

except FileNotFoundError:
    print(f"❌ File not found at {MERGED_PDF_FULLPATH}. Ensure the path is correct and the file exists.")
except Exception as e:
    print(f"❌ Error during text extraction: {e}")
