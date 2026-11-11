# 🛡️ RecruitShield AI

> **Hybrid Recruitment Fraud & Scam Analyzer**  
> An enterprise-grade AI system that combines text-based machine learning classification with automated contextual heuristics to protect job seekers from sophisticated employment scams.

---

## 📌 Problem Overview & Core Limitation
Traditional open-source fake job detectors rely almost entirely on standard text classification models (such as TF-IDF combined with basic classifiers). 

**The Core Limitation:** Traditional models are *text-blind*. When a scammer drafts a job posting using professional grammar and corporate phrasing—while embedding off-platform contact vectors (e.g., Telegram, WhatsApp) or requesting upfront fees—pure text models falsely mark the listing as **Legitimate**.

---

## 🚀 The RecruitShield AI Solution
**RecruitShield AI** resolves text-blindness by implementing a **Two-Tier Hybrid Verification Engine**:

1. **Tier 1 (NLP Machine Learning Engine):** A Logistic Regression model trained on job posting vectors (via TF-IDF) to evaluate linguistic style, structural anomalies, and word frequency patterns.
2. **Tier 2 (Contextual Heuristic Rule Engine):** A security layer that scans for off-platform communication vectors (*Telegram, WhatsApp*), financial phishing indicators (*registration fees, wire transfers, USDT/crypto*), and anomalous or shortened application URLs (`t.me`, `forms.gle`, `bit.ly`).

---

## ⚙️ How It Works (System Architecture & Execution Flow)

```mermaid
graph TD
    A[User Input: Job Text & Application URL] --> B[Two-Tier Hybrid Verification Engine]
    
    B --> C[Tier 1: ML Engine <br/> TF-IDF + Logistic Regression]
    B --> D[Tier 2: Heuristic Rule Engine <br/> Keyword & URL Check]
    
    C --> E[Base ML Scam Probability Score]
    D --> F[Heuristic Penalty Points]
    
    E --> G[Score Aggregation <br/> Combine ML Score + Penalties]
    F --> G
    
    G --> H[Interactive Modal Report Pop-Up <br/> Final Risk Badge & Red Flags]


1. Input Ingestion: The user submits a job description and optional application link through a clean,   light-mode Streamlit dashboard.

2. Feature Vectorization & Classification (Tier 1): The raw text is transformed into mathematical vectors using TfidfVectorizer and evaluated by a trained LogisticRegression classifier to generate a base scam probability score.

3. Contextual Security Scan (Tier 2): The rule engine inspects the text for suspicious keywords and checks the domain structure of the URL, applying targeted score penalties if high-risk flags are detected.

4. Score Aggregation & Centered Modal Output: The ML score and heuristic penalties merge to calculate the final risk percentage (0–100%). Results launch in a centered pop-up modal displaying a risk badge, metric breakdown, and specific contextual red flags.


📋 Requirements & Dependencies
To run this project locally or deploy it to the cloud, ensure you have Python 3.9+ installed along with the following libraries:

Python Packages (requirements.txt)
streamlit — Interactive Web Framework & UI

scikit-learn — Machine Learning Pipeline (TF-IDF & Logistic Regression)

pandas — Data Processing & Manipulation

joblib — Serialization and loading of model artifacts (.pkl files)


📁 Repository Structure

RecruitShield-AI/
│
├── app.py                   # Main Streamlit web application & UI engine
├── train_model.py           # ML training script for dataset processing
├── requirements.txt         # Production dependency manifest
├── README.md                # Project documentation
│
└── models/                  # Local ML model storage
    ├── fake_job_model.pkl    # Trained Logistic Regression classifier
    └── tfidf_vectorizer.pkl # Fitted TF-IDF feature transformer


🛠️ Local Setup & Execution

1. Clone the Repository:
git clone [https://github.com/AzkaaMulla/RecruitShield-AI.git](https://github.com/AzkaaMulla/RecruitShield-AI.git)

2. Install Dependencies:
pip install -r requirements.txt

3. Train Model Artifacts (If running for the first time):
python train_model.py

4. Launch the Streamlit App:
streamlit run app.py


🔒 Security & Privacy Features
Zero Persistent Data Storage: Input text, company details, and application URLs are processed strictly in-memory during evaluation and immediately discarded.

Proactive Risk Mitigation: Detects phishing traps, financial scam requirements, and unverified contact channels before users interact with fraudulent recruiters.


👤 Author
Developer: Azkaa Mulla

Domain: Computer Science Engineering & Data Analytics