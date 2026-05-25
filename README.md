# Her Wellness — AI Health Education for Black Women

An AI-powered health education tool built specifically for Black and African women. Uses a RAG (Retrieval Augmented Generation) pipeline to provide accurate, culturally aware health information grounded in medically reviewed sources.

---

## Live Demo

[Live App](https://her-wellness.streamlit.app)

---

## What It Does

Users select a health topic and ask any question in plain English. The system retrieves relevant information from a curated medical knowledge base and generates a clear, accurate, culturally aware response grounded only in verified sources — never hallucinated.

### Health Topics Covered
- **Fibroids** — symptoms, treatment options, why Black women are disproportionately affected
- **Maternal Health** — maternal mortality disparities, warning signs, advocacy strategies
- **Mental Health** — stigma, barriers to care, finding culturally competent therapists
- **Hypertension** — risk factors, prevention, management for Black women
- **Nutrition** — culturally relevant dietary guidance, managing chronic conditions through diet
- **Navigating Healthcare** — patient rights, self-advocacy, finding culturally competent providers

---

## How It Works
User Question → FAISS Vector Search → Retrieve Relevant Document Chunks → Groq LLM → Culturally Aware Answer
1. **Knowledge Base** — 6 text documents written from NIH, CDC, Office on Women's Health, and Black Women's Health Imperative sources
2. **Embeddings** — HuggingFace all-MiniLM-L6-v2 model converts documents into vector representations
3. **FAISS** — vector similarity search retrieves the most relevant document chunks for each question
4. **Groq LLM** — llama-3.3-70b-versatile generates a response grounded only in retrieved context
5. **Streamlit** — clean elegant UI with black and gold design

---

## Why RAG Instead of a General LLM

A general LLM like ChatGPT can hallucinate medical information — confidently giving wrong answers. RAG grounds every response in specific verified documents. The AI can only answer from what is in the knowledge base making it significantly safer for health information.

Additionally this tool has cultural awareness built into every prompt — it always responds with sensitivity to the specific healthcare barriers Black and African women face including being dismissed by providers cultural stigma around mental health and historical medical mistrust.

---

## Tech Stack

- **Python** — primary language
- **LangChain** — RAG framework and document orchestration
- **FAISS** — vector database for semantic similarity search
- **HuggingFace Sentence Transformers** — document embedding model
- **Groq API** — LLM inference (llama-3.3-70b-versatile)
- **Streamlit** — frontend UI and deployment

---

## Running Locally

**Prerequisites:** Python 3.9+, Groq API key

**1. Clone the repository**
```bash
git clone https://github.com/mekonnes/Her-wellness.git
cd Her-wellness
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
GROQ_API_KEY=your_groq_key_here python3 -m streamlit run app.py
```

App runs at `http://localhost:8501`

---

## Project Structure
her-wellness/
├── app.py                      # Streamlit UI
├── rag.py                      # RAG pipeline
├── requirements.txt            # Python dependencies
├── logo.svg                    # App logo
└── knowledge_base/
├── fibroids.txt
├── maternal_health.txt
├── mental_health.txt
├── hypertension.txt
├── nutrition.txt
└── navigating_healthcare.txt
---

## Knowledge Base Sources

All health information is sourced from medically reviewed organizations:
- National Institutes of Health (NIH)
- Centers for Disease Control and Prevention (CDC)
- Office on Women's Health (womenshealth.gov)
- Black Women's Health Imperative (bwhi.org)

---

## Disclaimer

This tool is for educational purposes only. It is not a substitute for professional medical advice diagnosis or treatment. Always consult a qualified healthcare provider for personal medical guidance.

---

## Author

**Soliana Mekonnen**
Computer Science & Data Science · Augsburg University
[LinkedIn](https://www.linkedin.com/in/soliana-mekonnen) · [GitHub](https://github.com/mekonnes)
