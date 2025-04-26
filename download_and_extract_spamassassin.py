import os
import tarfile
import urllib.request

# Base URL and filenames
base_url = "https://spamassassin.apache.org/old/publiccorpus/"
files = [
    "20021010_easy_ham.tar.bz2",
    "20021010_hard_ham.tar.bz2",
    "20021010_spam.tar.bz2",
    "20030228_easy_ham.tar.bz2",
    "20030228_easy_ham_2.tar.bz2",
    "20030228_hard_ham.tar.bz2",
    "20030228_spam.tar.bz2",
    "20030228_spam_2.tar.bz2",
    "20050311_spam_2.tar.bz2"
]

# Folder structure
tar_dir = "tars"
extract_dir = "datasets"
os.makedirs(tar_dir, exist_ok=True)
os.makedirs(extract_dir, exist_ok=True)

for fname in files:
    url = base_url + fname
    tar_path = os.path.join(tar_dir, fname)

    # Cleaned output folder name (e.g., "easy_ham", "spam_2")
    cleaned_name = fname.split("_", 1)[1].replace(".tar.bz2", "")
    out_path = os.path.join(extract_dir, cleaned_name)

    # Download tar if needed
    if not os.path.exists(tar_path):
        print(f"⬇️ Downloading {fname}...")
        urllib.request.urlretrieve(url, tar_path)
    else:
        print(f"✅ Already downloaded: {fname}")

    # Extract tar if needed
    if not os.path.exists(out_path):
        print(f"📦 Extracting {fname} into {out_path}...")
        os.makedirs(out_path, exist_ok=True)
        with tarfile.open(tar_path, "r:bz2") as tar:
            tar.extractall(path=out_path)
    else:
        print(f"📁 Already extracted: {cleaned_name}")

print("🎉 Done downloading and extracting.")
