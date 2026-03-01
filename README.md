# 🚢 Titanic AI Chatbot

A production-ready, conversational AI chatbot that answers natural-language questions about the **Titanic passenger dataset** using **LangChain**, **Groq (LLaMA 3)**, **FastAPI**, and **Streamlit**.

---

## 📁 Project Structure

```
titanic-chatbot/
│
├── backend/                    # FastAPI + LangChain backend
│   ├── main.py                 # App entrypoint, CORS, lifecycle events
│   ├── router.py               # Versioned APIRouter (/api/v1)
│   ├── agent.py                # LangChain pandas DataFrame agent
│   ├── tool.py                 # Custom LangChain @tool functions
│   ├── schemas.py              # Pydantic request/response models
│   ├── config.py               # Centralised settings (pydantic-settings)
│   └── logger.py               # Structured logging setup
│
├── frontend/
│   └── app.py                  # Streamlit chat UI
│
├── data/
│   └── titanic.csv             # Titanic passenger dataset
│
├── .env                        # Local environment variables (git-ignored)
├── .env.example                # Template — copy to .env and fill in values
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone & enter the project
```bash
git clone <repo-url>
cd titanic-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux
```
Open `.env` and set your **Groq API key** (get one free at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=gsk_...
```

---

## 🚀 Running the App

### Start the backend (FastAPI)
```bash
cd backend
python main.py
```
The API will be available at `http://localhost:8000`.
Interactive docs: `http://localhost:8000/docs`

### Start the frontend (Streamlit) — in a new terminal
```bash
cd frontend
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔌 API Reference

| Method | Endpoint             | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/api/v1/health`     | Health check                   |
| POST   | `/api/v1/ask`        | Ask a question about Titanic   |
| GET    | `/docs`              | Swagger UI                     |
| GET    | `/redoc`             | ReDoc documentation            |

### Example request
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What was the survival rate for women in first class?"}'
```

### Example response
```json
{
  "question": "What was the survival rate for women in first class?",
  "answer": "The survival rate for women in first class was 96.8% (30 out of 31 survived).",
  "status": "success"
}
```

---

## 🛠️ Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| LLM       | Groq — LLaMA 3 (8B / 70B)         |
| Agent     | LangChain pandas DataFrame agent  |
| Backend   | FastAPI + Uvicorn                 |
| Frontend  | Streamlit                         |
| Config    | pydantic-settings + dotenv        |
| Data      | pandas + Titanic CSV              |

---

## 🔒 Environment Variables

| Variable          | Default              | Description                                      |
|-------------------|----------------------|--------------------------------------------------|
| `GROQ_API_KEY`    | *(required)*         | Your Groq API key                                |
| `LLM_MODEL`       | `llama3-8b-8192`     | Groq model (`llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`) |
| `LLM_TEMPERATURE` | `0.0`                | Model temperature (0 = deterministic)            |
| `DATA_PATH`       | `data/titanic.csv`   | Path to the dataset                              |
| `API_HOST`        | `0.0.0.0`            | API server host                                  |
| `API_PORT`        | `8000`               | API server port                                  |
| `DEBUG`           | `false`              | Enable debug mode & auto-reload                  |

---

## 💡 Sample Questions

- *What was the overall survival rate?*
- *How many passengers were in each class?*
- *What is the average age of survivors vs non-survivors?*
- *Which port had the highest number of passengers?*
- *How many children under 10 survived?*
- *Show a breakdown of fares by class.*
"# titanic_chatbot" 
