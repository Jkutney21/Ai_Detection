import os
import re
import tarfile
import pandas as pd
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer

# Step 0: Extract tar.bz2 file
if not os.path.exists("easy_ham"):  # Check if the directory already exists
    with tarfile.open("20021010_easy_ham.tar.bz2", "r:bz2") as tar:
        tar.extractall()  # Extract files into the current directory

# Step 1: Extract and clean email body
def extract_email_body(filepath):
    with open(filepath, "r", encoding="latin1") as file:
        lines = file.readlines()
        blank_idx = next((i for i, line in enumerate(lines) if line.strip() == ""), 0)
        body = " ".join(lines[blank_idx+1:]).lower()
    return re.sub(r'\W+', ' ', body)

# Step 2: Load dataset from directory
EMAIL_DIR = "./easy_ham/"
emails = []
for filename in os.listdir(EMAIL_DIR):
    if filename == "cmds": continue
    filepath = os.path.join(EMAIL_DIR, filename)
    if os.path.isfile(filepath):  # Ensure it's a file, not a directory
        emails.append({
            "filename": filename,
            "text": extract_email_body(filepath),
            "timestamp": os.path.getmtime(filepath)
        })

df = pd.DataFrame(emails)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

# Step 3: Extract Features
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
tfidf_matrix = vectorizer.fit_transform(df['text'])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

df['sender'] = df['filename'].str.extract(r'@(\w+)')
sender_freq = df['sender'].value_counts().to_dict()
df['sender_volume'] = df['sender'].map(sender_freq).fillna(0)

df = df.sort_values('timestamp')
recent_window = pd.Timedelta('2 days')
df['thread_activity'] = df.apply(lambda row: ((df['sender'] == row['sender']) & 
                                              (df['timestamp'] >= row['timestamp'] - recent_window)).sum(), axis=1)

# Step 4: Combine features and rank
feature_df = pd.concat([df[['filename', 'sender_volume', 'thread_activity']], tfidf_df], axis=1)
feature_df['rank_score'] = (
    0.4 * feature_df['sender_volume'] +
    0.3 * feature_df['thread_activity'] +
    0.3 * tfidf_df.sum(axis=1)
)
median_score = feature_df['rank_score'].median()
feature_df['priority'] = feature_df['rank_score'] > median_score

print(feature_df[['filename', 'rank_score', 'priority']].sort_values(by='rank_score', ascending=False))