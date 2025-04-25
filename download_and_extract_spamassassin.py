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

# Download + extract folder
os.makedirs("datasets", exist_ok=True)

for fname in files:
    url = base_url + fname
    filepath = os.path.join("datasets", fname)
    extract_dir = os.path.join("datasets", fname.replace(".tar.bz2", ""))

    # Download
    if not os.path.exists(filepath):
        print(f"Downloading {fname}...")
        urllib.request.urlretrieve(url, filepath)
    else:
        print(f"Already downloaded: {fname}")

    # Extract
    if not os.path.exists(extract_dir):
        print(f"Extracting {fname} to {extract_dir}...")
        with tarfile.open(filepath, "r:bz2") as tar:
            tar.extractall(path=extract_dir)
    else:
        print(f"Already extracted: {fname}")

print("✅ Done downloading and extracting all datasets.")
