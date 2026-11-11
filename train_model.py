import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def train_and_save_model():
    print("Loading dataset...")
    # Make sure you have the 'fake_job_postings.csv' file in your directory (from Kaggle)
    # If not present, this serves as the blueprint structure
    try:
        df = pd.read_csv('fake_job_postings.csv')
    except FileNotFoundError:
        print("Dataset not found! Please download the 'Real / Fake Job Posting Prediction' dataset from Kaggle.")
        return

    # Fill missing values
    df.fillna(" ", inplace=True)

    # Combine relevant text features into a single master text column
    df['combined_text'] = (
        df['title'] + " " + 
        df['company_profile'] + " " + 
        df['description'] + " " + 
        df['requirements']
    )

    X = df['combined_text']
    y = df['fraudulent'] # Target: 1 for fake, 0 for real

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression model with balanced class weights...")
    # class_weight='balanced' handles the fact that fake jobs are rare compared to real ones
    model = LogisticRegression(class_weight='balanced', max_iter=1000)
    model.fit(X_train_vec, y_train)

    # Evaluate
    predictions = model.predict(X_test_vec)
    print("Model Evaluation:")
    print(classification_report(y_test, predictions))

    # Save artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/fake_job_model.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    print("Model and Vectorizer saved successfully in 'models/' directory!")

if __name__ == "__main__":
    train_and_save_model()