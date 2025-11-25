# --- PDF MerGING SCRIPT ---
# This script lists all PDFs in a specified Google Drive folder,
# sorts them by the *leading number* in the filename in ascending order, and merges them.

from pypdf import PdfWriter, PdfReader
import pandas as pd
import glob
import os
import re # <-- New import for numerical sorting
from IPython.display import display, HTML

# ----------------------------------------------------
# ⚠ USER INPUT REQUIRED: Set the path to your PDFs
# ----------------------------------------------------
# Example: '/content/drive/MyDrive/MyProject/Reports'
PDF_FOLDER_PATH = '/content/drive/MyDrive/Deep Learning/pdf_files'
# Update the above path to the actual folder in your Drive if different!
# ----------------------------------------------------

MERGED_PDF_FILENAME = "merged_document_for_analysis.pdf"
MERGED_PDF_FULLPATH = os.path.join(PDF_FOLDER_PATH, MERGED_PDF_FILENAME)

# --- Custom Sorting Function for Numerical Order ---
def numerical_sort_key(filepath):
    """
    Extracts the leading number from the filename for correct numerical sorting.
    e.g., "110.pdf" -> 110, "3.pdf" -> 3
    """
    filename = os.path.basename(filepath)
    # Match one or more digits at the start of the filename
    match = re.match(r'(\d+)', filename)
    if match:
        # Convert the matched string (e.g., "10") to an integer (10)
        return int(match.group(1))
    # For files without a leading number, push them to the end of the list
    return float('inf')

# --- Merging Logic ---

print("--- Starting PDF Merging Process ---")

# 1. List all PDF files in the specified folder
all_files = glob.glob(os.path.join(PDF_FOLDER_PATH, "*.pdf"))

# 2. Filter out the final merged file if it exists, and get file paths
pdf_list_paths = [f for f in all_files if os.path.basename(f) != MERGED_PDF_FILENAME]

# 3. Sort files using the custom numerical key
pdf_list_paths.sort(key=numerical_sort_key)

if not pdf_list_paths:
    print(f"❌ Error: No individual PDF files found in the directory: {PDF_FOLDER_PATH}")
    if not os.path.exists(PDF_FOLDER_PATH):
        print("Tip: The folder path itself does not exist. Check for typos.")
else:
    print(f"--- Found {len(pdf_list_paths)} PDF files to merge in folder: {PDF_FOLDER_PATH} ---")

    # Display the order that will be used for merging
    print("Files will be merged in this *numerical ascending* order:")
    file_selection_df = pd.DataFrame({
        'Index': range(1, len(pdf_list_paths) + 1),
        'Filename': [os.path.basename(f) for f in pdf_list_paths]
    })
    display(HTML(file_selection_df.to_html(index=False)))

    # 4. Perform Merging
    merger = PdfWriter()
    print(f"\nStarting merge into: {MERGED_PDF_FILENAME}")

    for pdf_path in pdf_list_paths:
        try:
            merger.append(pdf_path)
            print(f"  - Appended: {os.path.basename(pdf_path)}")
        except Exception as e:
            print(f"  - ⚠ Warning: Could not append {os.path.basename(pdf_path)}. Skipping. Error: {e}")

    # 5. Write the merged PDF
    with open(MERGED_PDF_FULLPATH, "wb") as fout:
        merger.write(fout)
    merger.close()

    print(f"\n✅ Merging complete. New file saved to: {MERGED_PDF_FULLPATH}")
    print("------------------------------------------------------------------")
    print("Now run the 'pdf_analyzer.py' script for theme extraction and summarization.")

# Store the path for the next script to use
# This variable needs to be accessible globally for the next cell
global MERGED_FILE_FOR_ANALYSIS
MERGED_FILE_FOR_ANALYSIS = MERGED_PDF_FULLPATH
