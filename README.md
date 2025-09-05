## 🤖 AI Career Advisor for Data Science in Indonesia
This project is a simple, conversational AI chatbot built to answer common questions about pursuing a data science career in Indonesia. It serves as a technical demonstration of an end-to-end LLM-based application, from data preparation to a live, deployed web application.

This project was built as a submission for an AI/Data Scientist technical exam.

### 🚀 Live Demo
You can access and interact with the live application here:

➡️ Click [here](https://datascientistcareer-chatbot.streamlit.app/) to view the live app:
- https://datascientistcareer-chatbot.streamlit.app/

### 🛠️ Tools & Technology Stack
Programming Language: Python

Web Framework: Streamlit
Deployment Platform: Streamlit Community Cloud
Core Libraries:
- sentence-transformers: For semantic search to find the most relevant information in the knowledge base. The all-MiniLM-L6-v2 model was used.
- torch: As a dependency for sentence-transformers.
- google-generativeai: To interact with the Gemini LLM.
- LLM: Google Gemini 1.5 Flash (gemini-1.5-flash-latest)

### ⚙️ Setup and Running the Program
Follow these steps to set up and run the application locally.

Clone the Repository (if applicable)

```
# git clone <your-repo-url>
# cd <your-repo-name>
```

Create and Activate a Virtual Environment

```
# Create the environment
python -m venv .venv

# Activate it (macOS/Linux)
source .venv/bin/activate

# Activate it (Windows)
# .venv\Scripts\activate
```

Install Dependencies

```
pip install -r requirements.txt
```

Add Your API Key (for local development)
- Create a folder named .streamlit in the project's root directory.
- Inside that folder, create a file named secrets.toml.
- Add your Google Gemini API key to the file like this:

```
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
```

Run the Application Locally

```
streamlit run app.py
```

The application should automatically open in your web browser.

## 🧪 Testing Examples & Results
Here are three examples of interactions with the chatbot, demonstrating its functionality.

Example 1
➡️ My Question:

```
Apa itu data science dan kenapa penting untuk negara Indonesia?
```

🤖 Bot's Answer:

```
Data science itu ilmu yang memanfaatkan data untuk memecahkan masalah danmengambil keputusan yang lebih baik, lho! ✨
Di Indonesia, data science penting banget karena bisa membantu berbagai sektor, seperti kesehatan, pertanian, dan ekonomi, untuk berkembang lebih pesat.
Bayangkan saja, kita bisa memprediksi penyakit, meningkatkan hasil panen, atau bahkan mengurangi kemacetan dengan data yang tepat!
📈 Dengan begitu, Indonesia bisa jadi negara yang lebih maju dan sejahtera. 😊
```

📝 Notes:

  The answer was relevant and correctly synthesized the information from the knowledge base.

Example 2
➡️ My Question:

```
Skill apa saja yang diperlukan untuk bisa menjadi Data Scientist yang mahir?
```

🤖 Bot's Answer:

```
Halo! 👋 Untuk jadi Data Scientist handal di Indonesia, kamu butuh pondasi kuat di beberapa bidang, nih!
Kamu perlu menguasai Python & R 💻, statistik & matematika 📊, machine learning & deep learning 🧠,
serta data wrangling, visualisasi data, dan manajemen database (SQL) 🗄️. Semangat ya! 👍
```

📝 Notes:

  The model successfully provided a conversational answer based on the retrieved context, following the prompt's length and style constraints.

Example 3
➡️ My Question:

```
Industri apa saja di Indonesia yang biasanya memerlukan Data Scientist?
```

🤖 Bot's Answer:

```
Wah, pertanyaan yang bagus! 🤔 Di Indonesia, banyak industri yang membutuhkan Data Scientist, seperti
Fintech (keuangan digital) 🚀, E-commerce 🛍️, Perbankan 🏦, Telekomunikasi 📱, dan juga bidang kesehatan
serta pemerintahan 🏥. Bahkan startup pun sekarang sangat membutuhkan keahlian ini! 😊
```

📝 Notes:

  This shows the bot's ability to handle a slightly different phrasing of a question in the dataset.
