# --- Google Drive Mounting ---
from google.colab import drive
import os

drive.mount('/content/drive', force_remount=False)
print("✅ Google Drive mounted at /content/drive")

# --- Install Required Libraries ---
!pip install pypdf bertopic sentence-transformers umap-learn hdbscan nltk -q
print("✅ Libraries installed.")
