import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq

def load_knowledge_base():
    documents = []
    kb_path = "knowledge_base"
    for filename in os.listdir(kb_path):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(kb_path, filename))
            documents.extend(loader.load())
    return documents

def build_vector_store(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def get_answer(question, vector_store, api_key, topic=None):
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    relevant_docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])

    topic_context = f"The user is asking about {topic}. " if topic else ""

    prompt = f"""You are a compassionate and knowledgeable health education assistant specifically supporting Black and African women. You provide accurate, culturally aware health information.

{topic_context}Use ONLY the information provided below to answer the question.

IMPORTANT RULES:
- If the question is not related to women's health, Black women's health, or the health topics in the context, respond with: "I'm only able to answer questions related to women's health topics including fibroids, maternal health, mental health, hypertension, nutrition, and navigating healthcare. Please ask a health-related question."
- If the question is health-related but the specific answer is not in the context, say you don't have that specific information and encourage the user to consult a healthcare provider.
- Never answer questions unrelated to health.
- Always end your response with a brief reminder to consult a healthcare provider for personal medical advice.

Context:
{context}

Question: {question}

Answer:"""

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()