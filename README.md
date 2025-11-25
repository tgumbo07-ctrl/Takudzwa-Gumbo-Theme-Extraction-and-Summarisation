# Takudzwa-Gumbo-Theme-Extraction-and-Summarisation
Deep Learning
Automated Analysis Pipeline: Generative AI in Marketing

**Project Overview**

This project processes a corpus of 67 academic documents (1,093 pages) regarding the impact of ChatGPT and Generative AI on the marketing industry.

Instead of manual review, I built a Python-based pipeline to:

Merge disparate PDF files into a single searchable artifact.

Extract and clean text for data mining.

Analyze frequency distributions to identify key research themes.

Generate a formatted executive summary report.

**The Workflow (Methodology)**

Phase 1: Ingestion & Merging

Script: 1_combine_pdfs_v2.py

Logic: Iterates through the directory, sorts files chronologically, and uses pypdf to merge them.

Feature: Generates a dynamic Table of Contents and Interactive Bookmarks for navigation.

Phase 2: Frequency Analysis

Script: 2_analyze_text.py

Logic: Extracts raw text from the combined PDF, filters out "stop words" (common English words), and performs a frequency count on the remaining corpus.

Key Insight: The analysis revealed "ChatGPT" (4,056) and "Ethics/Human" (1,800+) as dominant statistical themes.

Phase 3: Automated Reporting

Script: 3_generate_report.py

Logic: Takes the qualitative and quantitative findings and uses python-docx to programmatically generate a formatted Word Document.

**Key Findings Summary**

Dataset: ~803,500 words across 67 files.

Top Keyword: "2023" (Indicates high recency/cutting-edge research).

Core Conclusion: Marketing is shifting to a "Human-in-the-Loop" model where AI handles content generation, but humans handle strategy and ethical verification.

**How to Run This Code**

Clone the repository.

Install dependencies:

pip install -r requirements.txt


Place your PDF files in the root directory.

Run the scripts in order:

python 1_combine_pdfs_v2.py
python 2_analyze_text.py
python 3_generate_report.py


**Output**

The final analysis is available in this repository as Assignment_Summary_Report.docx.
