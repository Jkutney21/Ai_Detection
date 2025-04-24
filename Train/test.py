# AI Text Detection Pipeline - Merged Free Datasets Version

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os

# STEP 1: Load both free datasets from Hugging Face
print("Loading DAIGT...")
df_daigt = pd.read_csv("hf://datasets/thedrcat/daigt-v2-train-dataset/train_v2_drcat_02.csv")

print("Loading Dmitva...")
df_dmitva = pd.read_csv("hf://datasets/dmitva/human_ai_generated_text/model_training_dataset.csv")

# STEP 2: Clean and standardize
print("Cleaning DAIGT...")
df_daigt = df_daigt[['text', 'label']].dropna()
df_daigt = df_daigt[df_daigt['text'].str.strip() != '']
df_daigt['label'] = df_daigt['label'].map({'Human': 0, 'AI': 1})
df_daigt = df_daigt.dropna(subset=['label'])
df_daigt['label'] = df_daigt['label'].astype(int)

print("Cleaning Dmitva...")
df_dmitva = df_dmitva[['text', 'label']].dropna()
df_dmitva = df_dmitva[df_dmitva['text'].str.strip() != '']
df_dmitva['label'] = df_dmitva['label'].map({'Human': 0, 'AI': 1})
df_dmitva = df_dmitva.dropna(subset=['label'])
df_dmitva['label'] = df_dmitva['label'].astype(int)

# STEP 3: Merge the datasets
combined_df = pd.concat([df_daigt, df_dmitva], ignore_index=True)
combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

print("\nCombined dataset size:", combined_df.shape)
print("Label distribution:\n", combined_df['label'].value_counts())

# STEP 4: Text Preprocessing
X = combined_df['text']
y = combined_df['label']

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_vect = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

# STEP 5: Train Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("\nLogistic Regression Results:")
print(classification_report(y_test, y_pred))

# STEP 6: (Optional) Lasso Regularization
lasso_model = LogisticRegression(penalty='l1', solver='liblinear')
lasso_model.fit(X_train, y_train)

y_pred_lasso = lasso_model.predict(X_test)
print("\nLasso Regularized Logistic Regression Results:")
print(classification_report(y_test, y_pred_lasso))

# STEP 7: Visualize Top Features
feature_names = vectorizer.get_feature_names_out()
coefs = model.coef_[0]
top_features = np.argsort(coefs)[-20:]

plt.figure(figsize=(10, 6))
plt.barh(feature_names[top_features], coefs[top_features])
plt.xlabel("Coefficient")
plt.title("Top Predictive Words for AI Detection")
plt.tight_layout()
plt.show()
