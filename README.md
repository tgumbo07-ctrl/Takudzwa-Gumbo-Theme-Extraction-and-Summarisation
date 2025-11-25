Takudzwa-Gumbo-Theme-Extraction-and-Summarisation

Domain: Deep Learning | Automated Analysis Pipeline: Generative AI in Marketing

Project Overview

This project processes a corpus of 67 academic PDFs (~1,093 pages) examining the impact of ChatGPT and Generative AI on marketing.

Instead of manually reviewing each document, this Python-based pipeline automatically:

Merges multiple PDFs into a single searchable file.

Extracts and cleans text for data mining.

Performs neural topic modeling using BERTopic.

Generates a formatted Word report summarizing themes and key findings.

Workflow (Methodology)
Phase 1: Ingestion & Merging

Script: 01_extraction.py
Logic:

Iterates through a folder of PDFs, sorts them numerically by filename, and merges them using pypdf.

Produces a single merged PDF for analysis.

Output: merged_document_for_analysis.pdf

Phase 2: Neural Theme Extraction & Analysis

Script: 02_analysis.py
Logic:

Loads the merged PDF text.

Tokenizes sentences using NLTK.

Uses BERTopic with all-MiniLM-L6-v2 embeddings to extract semantic topics.

Generates an extractive summary by selecting representative sentences from top topics.

Output: analysis_data_step2.pkl (contains topics, executive summary, and metadata)

Phase 3: Automated Report Generation

Script: 03_generate_report.py
Logic:

Loads Step 2 analysis results.

Programmatically generates a structured Word document using python-docx.

Includes sections: Executive Summary, Quantitative/Thematic Evidence, Detailed Theme Breakdown, and Methodology Notes.

Output: Deep_Learning_Analysis_Report.docx

Key Findings Summary

Dataset: ~803,500 words across 67 PDFs.

Top Keywords: "2023" (highly recent research), "ChatGPT", "Ethics/Human".

Core Conclusion: Marketing is evolving toward a Human-in-the-Loop approach, where AI handles content generation and humans oversee strategy and ethics.
