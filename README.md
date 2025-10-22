# 🧠 Debate Server

**Debate Server** is the backend for the **AI-Based Debate System**, providing secure APIs, real-time debate handling, AI-driven argument segmentation, and evaluation modules.  
It powers the Debate Client and manages all authentication, debate logic, and AI integrations.

---

## 🚀 Features
- 🔐 **User Authentication & Role Management** — Register, login, logout, change/reset passwords, and manage roles (admin, participant, moderator).
- 💬 **Real-Time Debate Chat** — WebSocket-based debate communication with live message streaming.
- 🧩 **Text Preprocessing & Argument Segmentation** — Tokenization, stop-word removal, lemmatization, and AI-driven segmentation.
- 🧮 **Argument Evaluation & Scoring** — Intelligent argument quality assessment using transformer models.
- 📧 **Email Service (Celery + Redis)** — Handles password reset, email verification, and background tasks.
- ⚙️ **Modular Architecture** — Each feature isolated into independent modules for scalability and clarity.

---

## 🏗️ Tech Stack
| Layer | Technology |
|-------|-------------|
| Framework | **FastAPI** |
| Task Queue | Celery |
| Message Broker | Redis |
| Database | PostgreSQL / SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT / OAuth2 |
| Mail | FastAPI-Mail |
| AI Modules | Transformers, spaCy, NLTK |

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/samiali12/debate-client.git
   cd debate-server
   ```

2. **Create and activate virtual environment**
    ```bash 
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    ```
3. **Install dependencies**
    ```
    pip install -r requirements.txt

    ```
4. **Configure environment variables**
    ```
    DATABASE_URL=mysql+pymysql://mysql:password@localhost:5432/debate_ai
    SECRET_KEY=your_secret_key
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REDIS_URL=redis://localhost:6379/0
    MAIL_USERNAME=youremail@example.com
    MAIL_PASSWORD=yourpassword
    MAIL_FROM=youremail@example.com
    MAIL_PORT=587
    MAIL_SERVER=smtp.gmail.com
    ```
5. **Run database migrations**
    ```
    alembic upgrade head

    ```

6. **Start Celery worker**
    ```
    celery -A app.tasks.celery_worker.celery worker --loglevel=info
    ```

7. **Start the FastAPI server**
   ```
   uvicorn app.main:app --reload
    ```


### 🧾 License
This project is licensed under the MIT License — you are free to use and modify it.

### 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to improve.
