import os
import re
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler

# --- Utility Functions ---
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_plot(fig, save_path):
    fig.savefig(save_path, bbox_inches='tight')
    plt.close(fig)

# --- Extract email text ---
def extract_email_body(filepath):
    with open(filepath, "r", encoding="latin1") as file:
        lines = file.readlines()
        blank_idx = next((i for i, line in enumerate(lines) if line.strip() == ""), 0)
        body = " ".join(lines[blank_idx+1:]).lower()
    return re.sub(r'\W+', ' ', body)

# --- Load emails ---
def load_emails(folder, label=None):
    emails = []
    if not os.path.exists(folder):
        return emails
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath):
            body = extract_email_body(fpath)
            item = {
                'filename': fname,
                'text': body,
                'full_path': fpath,
            }
            if label is not None:
                item['label'] = label
            emails.append(item)
    return emails

# --- Process Folder ---
def process_folder(folder_name, ham_list, spam_list):
    print(f"\n=== Processing {folder_name} ===")

    plot_folder = f"plots/{folder_name}"
    ensure_dir(plot_folder)

    # Prepare dataset
    all_emails = ham_list + spam_list
    df = pd.DataFrame(all_emails)

    if df.empty:
        print("No emails found.")
        return

    # --- Smart stopwords ---
    custom_stopwords = [
        "http", "https", "www", "com", "org", "net", "email", "mail", "subject",
        "message", "spamassassin", "noreply", "please", "click", "unsubscribe"
    ]
    all_stopwords = ENGLISH_STOP_WORDS.union(custom_stopwords)

    # --- FIX: Convert stopwords to a list! ---
    vectorizer = TfidfVectorizer(stop_words=list(all_stopwords), max_features=1000)

    X_tfidf = vectorizer.fit_transform(df["text"])
    y = df["label"]

    if len(df["label"].unique()) < 2:
        print(f"Only one class found in {folder_name}, skipping model training.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, stratify=y)
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    # --- Classification Report ---
    print(classification_report(y_test, y_pred))

    # --- Confusion Matrix ---
    if len(np.unique(y_test)) > 1:
        fig, ax = plt.subplots(figsize=(6, 4))
        cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["ham", "spam"], yticklabels=["ham", "spam"], ax=ax)
        ax.set_title(f"Confusion Matrix - {folder_name}")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("True")
        save_plot(fig, f"{plot_folder}/confusion_matrix.png")

    # --- Top TF-IDF Features ---
    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sorting = np.argsort(X_tfidf.sum(axis=0).A1)[::-1]
    top_n = 20
    top_features = feature_array[tfidf_sorting][:top_n]

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(x=X_tfidf.sum(axis=0).A1[tfidf_sorting][:top_n], y=top_features, ax=ax)
    ax.set_title(f"Top TF-IDF Features - {folder_name}")
    ax.set_xlabel("TF-IDF Score")
    save_plot(fig, f"{plot_folder}/top_tfidf_features.png")

    # --- Score and Analyze Ham Emails ---
    ham_df = pd.DataFrame(ham_list)
    if ham_df.empty:
        print(f"No ham emails found for {folder_name}.")
        return

    ham_df["timestamp"] = pd.to_datetime(
        [os.path.getmtime(f) for f in ham_df["full_path"]],
        unit='s'
    )

    X_ham_tfidf = vectorizer.transform(ham_df["text"])
    ham_df["spam_prob"] = clf.predict_proba(X_ham_tfidf)[:, clf.classes_.tolist().index("spam")]
    ham_df["spam_score"] = 1 - ham_df["spam_prob"]

    # --- Fake Sender Assignment ---
    possible_senders = [f"user{i}@example.com" for i in range(20)]  # 20 fake senders
    ham_df["sender"] = [random.choice(possible_senders) for _ in range(len(ham_df))]

    ham_df = ham_df.sort_values("timestamp")
    window = pd.Timedelta("2 days")
    ham_df["sender_volume"] = ham_df["sender"].map(ham_df["sender"].value_counts()).fillna(0)

    ham_df["thread_activity"] = ham_df.apply(
        lambda row: ((ham_df["sender"] == row["sender"]) &
                     (ham_df["timestamp"] >= row["timestamp"] - window)).sum(),
        axis=1
    )

    scaler = MinMaxScaler()
    priority_inputs = scaler.fit_transform(ham_df[["sender_volume", "thread_activity"]])
    ham_df["priority_score"] = 0.5 * priority_inputs[:, 0] + 0.5 * priority_inputs[:, 1]

    ham_df["final_score"] = 0.5 * ham_df["spam_score"] + 0.5 * ham_df["priority_score"]
    ham_df = ham_df.sort_values("final_score", ascending=False)

    # --- Top Priority Emails ---
    print("\nTop Priority Emails:")
    print(ham_df[["filename", "spam_score", "priority_score", "final_score"]].head(10))

    # --- Spam Score vs Priority Score Scatterplot ---
    if len(ham_df) > 1:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=ham_df, x="spam_score", y="priority_score", hue="final_score", palette="viridis", size="final_score", sizes=(20,200), ax=ax)
        ax.set_title(f"Spam Score vs Priority Score - {folder_name}")
        ax.set_xlabel("Spam Score (higher = safer)")
        ax.set_ylabel("Priority Score (higher = more important)")
        ax.legend()
        save_plot(fig, f"{plot_folder}/spam_vs_priority.png")
    else:
        print(f"Not enough ham emails to plot spam vs priority for {folder_name}.")

    # --- Sender Volume ---
    if ham_df["sender"].notnull().sum() > 0:
        fig, ax = plt.subplots(figsize=(10,4))
        top_senders = ham_df["sender"].value_counts().head(20)
        sns.barplot(x=top_senders.values, y=top_senders.index, ax=ax)
        ax.set_title(f"Top 20 Senders - {folder_name}")
        ax.set_xlabel("Email Count")
        ax.set_ylabel("Sender")
        save_plot(fig, f"{plot_folder}/sender_volume.png")
    else:
        print(f"No valid senders to plot for {folder_name}.")

# --- Master Runner ---
def main():
    folders_to_process = [
        ("easy_ham", "easy_ham", "spam"),
        ("easy_ham_2", "easy_ham_2", "spam"),
        ("hard_ham", "hard_ham", "spam"),
        ("spam", "easy_ham", "spam"),
        ("spam_2", "easy_ham", "spam_2"),
    ]

    for folder_name, ham_folder, spam_folder in folders_to_process:
        ham_list = load_emails(f"datasets/{ham_folder}", label="ham")
        spam_list = load_emails(f"datasets/{spam_folder}", label="spam")
        process_folder(folder_name, ham_list, spam_list)

# --- Entry Point ---
if __name__ == "__main__":
    main()
