import streamlit as st
import joblib
import os

# 1. Page Configuration
st.set_page_config(
    page_title="RecruitShield AI | Hybrid Scam Detector", 
    page_icon="🛡️", 
    layout="centered"
)

# 2. Professional Light-Mode SaaS Styling (Vercel/Stripe Inspired)
st.markdown("""
    <style>
    /* Global Light Theme */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Banner */
    .saas-header {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: #1e3a8a;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
    }
    .saas-header h1 {
        color: #1e40af !important;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .saas-header p {
        color: #3b82f6 !important;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Primary Buttons */
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: #1d4ed8 !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }

    /* Input Fields styling */
    .stTextArea textarea, .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #0f172a !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Load Model and Vectorizer (Cached)
@st.cache_resource
def load_artifacts():
    model = joblib.load('models/fake_job_model.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    return model, vectorizer

try:
    model, vectorizer = load_artifacts()
except Exception as e:
    st.error("⚠️ Model files not found! Please run `python train_model.py` first.")
    st.stop()

# 4. SaaS Header Banner
st.markdown("""
    <div class="saas-header">
        <h1>🛡️ RecruitShield AI</h1>
        <p>Enterprise-grade Hybrid Recruitment Fraud & Scam Analyzer</p>
    </div>
""", unsafe_allow_html=True)

# 5. Quick Demo Data Presets (To easily test the app!)
st.markdown("##### ⚡ Quick Test Presets:")
preset_col1, preset_col2, preset_col3 = st.columns(3)

sample_safe = "We are seeking a mid-level Python Developer to build backend infrastructure. Experience with Django, PostgreSQL, and REST APIs required. Competitive salary and health benefits provided."
sample_mod = "Urgent hiring for Remote Data Assistant! Earn $300 daily entering forms online. No experience required. Apply immediately via Google Form link."
sample_scam = "URGENT HIRING: Financial Processing Specialist! Earn $1,500/week working 2 hours daily. Candidates must register via Telegram and pay a $50 refundable training fee via Wire Transfer or USDT."

if preset_col1.button("📋 Load Safe Job Preset"):
    st.session_state['job_text'] = sample_safe
    st.session_state['url_text'] = "https://careers.techcorp.com/jobs"
if preset_col2.button("⚠️ Load Moderate Preset"):
    st.session_state['job_text'] = sample_mod
    st.session_state['url_text'] = "https://forms.gle/job-form-123"
if preset_col3.button("🚨 Load High Scam Preset"):
    st.session_state['job_text'] = sample_scam
    st.session_state['url_text'] = "https://t.me/fake_recruiter"

# 6. Main Input Form Container
with st.container(border=True):
    st.markdown("### 📝 Job Details Input")
    
    default_text = st.session_state.get('job_text', '')
    job_text_input = st.text_area(
        "Paste Job Description / Requirements Here:", 
        value=default_text,
        height=220, 
        placeholder="Paste full job description text here..."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        company_name = st.text_input("Company Name (Optional):", placeholder="e.g., Google, Amazon")
    with col_b:
        default_url = st.session_state.get('url_text', '')
        application_link = st.text_input("Application URL / Contact Info (Optional):", value=default_url, placeholder="e.g., t.me/recruiter_xyz")

# 7. Heuristic Rule-Checking Engine
def run_heuristic_checks(text, url):
    flags = []
    score_penalty = 0
    
    suspicious_keywords = [
        'telegram', 'whatsapp', 'viber', 'wire transfer', 
        'registration fee', 'training fee', 'apple gift card', 'crypto', 'usdt'
    ]
    for word in suspicious_keywords:
        if word in text.lower():
            flags.append(f"⚠️ Suspicious term found: **'{word}'** (Commonly tied to financial and recruitment scams).")
            score_penalty += 15

    if url:
        free_domains = ['t.me', 'whatsapp.com', 'forms.gle', 'bit.ly', 'tinyurl.com']
        if any(domain in url.lower() for domain in free_domains):
            flags.append(f"⚠️ Unofficial or shortened application link detected (`{url}`). Legitimate enterprises use official domain infrastructure.")
            score_penalty += 20
            
    return flags, score_penalty

# 8. Centered Modal Dialog Pop-Up for Results (With Non-Technical Guide)
@st.dialog("🛡️ RecruitShield Analysis Report", width="large")
def show_results_modal(final_fake_score, ml_probability, penalty, heuristic_flags, ml_prediction):
    st.markdown("### Evaluation Summary Dashboard")
    
    if final_fake_score > 50:
        st.error(f"🚨 **High Risk: Potential Scam Detected!**\n\n**Calculated Risk Score:** `{final_fake_score:.1f}%`")
    else:
        st.success(f"✅ **Low Risk: Appears Safe & Legitimate**\n\n**Calculated Risk Score:** `{final_fake_score:.1f}%`")
        
    metric_col1, metric_col2 = st.columns(2)
    with metric_col1:
        st.markdown(f"**Base ML Text Probability:** `{ml_probability:.1f}%`")
        st.markdown(f"**Heuristic Rule Penalties:** `+{penalty} pts`")
        
    with metric_col2:
        st.markdown("**Contextual Risk Flags:**")
        if heuristic_flags:
            for flag in heuristic_flags:
                st.markdown(flag)
        else:
            st.markdown("✨ No high-risk communication channels or anomalous URLs detected.")
            
    # --- NEW: Non-Technical User Guide ---
    with st.expander("💡 New User Guide: What do these scores mean?"):
        st.markdown("""
        * **Calculated Risk Score:** The final safety rating (0% to 100%). Over 50% means the job has major red flags.
        * **Base ML Text Probability:** What the computer's learning model thinks based strictly on the wording and grammar.
        * **Heuristic Penalties:** Extra warning points added because the app found suspicious text (like requests for money or untrusted chat links).
        * **Contextual Risk Flags:** Specific warnings pointing out dangerous communication apps (like Telegram) or fake links.
        """)
        
    with st.expander("🔍 View Technical Architecture Breakdown (For Developers)"):
        st.write(f"**Raw Model Classification:** {'Fraudulent' if ml_prediction == 1 else 'Legitimate'}")
        st.write("**Architecture Note:** Combines TF-IDF vectorization with an automated heuristic rule-engine to filter out sophisticated phishing vectors that standard text models miss.")
        
    if st.button("Close Report", type="primary", use_container_width=True):
        st.rerun()

# 9. Trigger Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Analyze Job Posting Now", use_container_width=True):
    if not job_text_input.strip():
        st.warning("⚠️ Please paste a job description before running the analysis.")
    else:
        with st.spinner("Analyzing linguistic patterns and cross-referencing heuristic risk factors..."):
            # Tier 1: Machine Learning Prediction
            input_vec = vectorizer.transform([job_text_input])
            ml_prediction = model.predict(input_vec)[0]
            ml_probability = model.predict_proba(input_vec)[0][1] * 100 
            
            # Tier 2: Heuristic Rule Checks
            heuristic_flags, penalty = run_heuristic_checks(job_text_input, application_link)
            
            # Combine Risk Score
            final_fake_score = min(100, max(0, ml_probability + penalty))
            
            # Open Centered Modal Dialog Pop-up
            show_results_modal(final_fake_score, ml_probability, penalty, heuristic_flags, ml_prediction)