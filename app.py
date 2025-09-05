import streamlit as st
import json
from sentence_transformers import SentenceTransformer, util
import torch
import google.generativeai as genai

# --- CONFIGURATION ---
# Configure the Gemini API key
# The API key should be stored in Streamlit's secrets management
# In your project root, create a file: .streamlit/secrets.toml
# Add your key like this: GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    GEMINI_MODEL = genai.GenerativeModel('gemini-1.5-flash-latest')
except (KeyError, FileNotFoundError):
    st.error("Google API Key not found. Please add it to your Streamlit secrets.")
    st.info("Please create a `.streamlit/secrets.toml` file and add your GOOGLE_API_KEY.")
    st.stop()

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Data Science Career Advisor", page_icon="🤖", layout="centered")

# --- MODEL AND DATA LOADING (with caching) ---
@st.cache_resource
def load_retriever():
    """Loads the sentence transformer model."""
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data(filepath="data/data.json"):
    """Loads the FAQ data and pre-computes embeddings for the questions."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    questions = [item['question'] for item in data]
    # The model is loaded from the other cached function
    model = load_retriever()
    embeddings = model.encode(questions, convert_to_tensor=True)
    return data, embeddings

# Load the resources
retriever_model = load_retriever()
faq_data, question_embeddings = load_data()

# --- CORE FUNCTIONS ---
def find_best_match(user_query, model, data, embeddings):
    """Finds the most relevant answer from the FAQ data."""
    if not user_query.strip():
        return None, 0.0

    query_embedding = model.encode(user_query, convert_to_tensor=True)
    # Calculate cosine similarities
    cos_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    # Find the index of the top score
    top_score_index = torch.argmax(cos_scores).item()
    top_score = cos_scores[top_score_index].item()

    # Set a similarity threshold
    SIMILARITY_THRESHOLD = 0.5
    if top_score < SIMILARITY_THRESHOLD:
        return None

    # Return the corresponding answer
    return data[top_score_index]['answer']


def get_gemini_response(user_question, context):
    """Generates a response using the Gemini API based on the provided context."""
    if context is None:
        # A fallback response if no relevant information is found in the data
        prompt = f"""
        You are a helpful AI assistant specializing in data science careers in Indonesia.
        The user asked: "{user_question}".
        You could not find a relevant answer in your knowledge base.
        Apologize and ask the user to rephrase their question or ask another question about data science careers in Indonesia.
        Keep the response in Indonesian.
        """
    else:
        # The main prompt when context is found
        prompt = f"""
        Anda adalah seorang penasihat karir yang ramah dan informatif di bidang data science di Indonesia.
        Tugas Anda adalah menjawab pertanyaan pengguna berdasarkan informasi yang diberikan di bawah ini.
        Buatlah jawaban yang jelas, mudah dimengerti, dan profesional dalam Bahasa Indonesia. 
        Respons anda dibuat pendek sekitar 2-4 kalimat saja tapi banyakan jumlah poin-poin jika memang perlu.
        Tambahkan emoji dibeberapa bagian respons anda agar lebih menarik.

        **Informasi Kontekstual:**
        {context}

        **Pertanyaan Pengguna:**
        {user_question}

        **Jawaban Anda:**
        """
    try:
        response = GEMINI_MODEL.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        return "Maaf, terjadi kesalahan saat mencoba menghasilkan jawaban. Silakan coba lagi nanti."


# --- STREAMLIT UI ---
st.title("🤖 AI Career Advisor for Data Science")
st.markdown("Ajukan pertanyaan seputar prospek karir, gaji, skill, dan lainnya di bidang data science di Indonesia!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo! Ada yang bisa saya bantu terkait karir data science di Indonesia?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Apa pertanyaanmu?"):
    # Display user message in chat message container
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Mencari informasi dan berpikir..."):
            # Find the best matching context from the FAQ data
            context = find_best_match(prompt, retriever_model, faq_data, question_embeddings)
            
            # Generate the response
            response = get_gemini_response(prompt, context)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

