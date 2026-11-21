
# 📧 AI Email Assistant Agent

## Project Description
AI Email Assistant Agent is a Python-based application that uses Artificial Intelligence to generate professional emails, suggest replies, and categorize emails.

It uses Ollama and Llama 3.2 to generate AI responses locally.

## Features

- Generate Professional Emails
- Suggest Email Replies
- Categorize Emails as Work, Personal, or Urgent
- Edit Email Subject and Body
- Save Email Drafts
- View Saved Draft History
- Delete Saved Drafts

## Technologies Used

- Python
- Streamlit
- Ollama
- Llama 3.2
- SQLite
- Requests

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/maheswari-python-projects/AI-Email-Assistant-Agent.git
```

### 2. Open Project Folder

```bash
cd AI-Email-Assistant-Agent
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama from:
https://ollama.com/download

### 5. Download AI Model

```bash
ollama pull llama3.2:3b
```

### 6. Run the Application

```bash
python -m streamlit run app.py
```

## Project Structure

```text
AI-Email-Assistant-Agent/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## AI Model

Llama 3.2:3b through Ollama.

## Database

SQLite is used to store email drafts locally.

## Developed By

Maheswari

## License

This project is developed for educational and internship purposes.
