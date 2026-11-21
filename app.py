
import streamlit as st
import requests
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------

def create_database():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            body TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_draft(subject, body):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO drafts (subject, body, created_at) VALUES (?, ?, ?)",
        (subject, body, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()


def get_drafts():
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, subject, body, created_at FROM drafts ORDER BY id DESC"
    )

    drafts = cursor.fetchall()
    conn.close()
    return drafts


def delete_draft(draft_id):
    conn = sqlite3.connect("emails.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM drafts WHERE id = ?", (draft_id,))

    conn.commit()
    conn.close()


# ---------------- AI FUNCTION ----------------

def ask_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="centered"
)

create_database()

if "subject" not in st.session_state:
    st.session_state["subject"] = ""

if "body" not in st.session_state:
    st.session_state["body"] = ""

if "draft_ready" not in st.session_state:
    st.session_state["draft_ready"] = False


# ---------------- MAIN PAGE ----------------

st.title("📧 AI Email Assistant Agent")

st.write(
    "Create professional emails using Artificial Intelligence."
)

st.divider()

action = st.selectbox(
    "Choose your task",
    [
        "Generate Email",
        "Suggest Reply",
        "Categorize Email",
        "View Saved Drafts"
    ]
)


# ---------------- GENERATE / REPLY / CATEGORIZE ----------------

if action != "View Saved Drafts":

    user_input = st.text_area(
        "Enter your instruction or paste an email:"
    )

    if st.button("Generate with AI"):

        if not user_input.strip():
            st.warning("Please enter your instruction.")

        else:
            try:
                with st.spinner("AI is working..."):

                    if action == "Generate Email":

                        prompt = f"""
                        Write a professional email based on this instruction:

                        {user_input}

                        Return the result in this format:

                        Subject: [Email Subject]

                        [Email Body]
                        Do not invent missing details.
                        """

                    elif action == "Suggest Reply":

                        prompt = f"""
                        Write a polite and professional reply
                        to this incoming email:

                        {user_input}

                        Return the result in this format:

                        Subject: Reply to Email

                        [Reply Body]
                        Do not invent facts.
                        """

                    else:

                        prompt = f"""
                        Categorize this email into exactly one category:
                        Work, Personal, or Urgent.

                        Give a short reason.

                        Email:
                        {user_input}
                        """

                    result = ask_ai(prompt)

                if action == "Categorize Email":

                    st.subheader("AI Email Category")
                    st.success(result)

                else:

                    lines = result.splitlines()
                    subject = "AI Generated Email"
                    body_lines = []
                    subject_found = False

                    for line in lines:

                        if line.strip().lower().startswith("subject:") and not subject_found:
                            subject = line.split(":", 1)[1].strip()
                            subject_found = True

                        elif subject_found:
                            body_lines.append(line)

                    body = "\n".join(body_lines).strip()

                    if not subject_found:
                        body = result

                    st.session_state["subject"] = subject
                    st.session_state["body"] = body
                    st.session_state["draft_ready"] = True

                    st.rerun()

            except requests.exceptions.ConnectionError:
                st.error("Ollama is not running. Please start Ollama.")

            except Exception as e:
                st.error(f"Error: {e}")


# ---------------- EDIT EMAIL ----------------

if action in ["Generate Email", "Suggest Reply"]:

    if st.session_state["draft_ready"]:

        st.divider()
        st.subheader("✏️ Edit Your Email")

        subject = st.text_input(
            "Email Subject",
            key="subject"
        )

        body = st.text_area(
            "Email Body",
            key="body",
            height=250
        )

        if st.button("💾 Save Draft"):

            if subject.strip() and body.strip():

                save_draft(subject, body)

                st.success("Email draft saved successfully!")

            else:
                st.warning("Subject and body cannot be empty.")


# ---------------- SAVED DRAFT HISTORY ----------------

if action == "View Saved Drafts":

    st.subheader("📂 Saved Email Drafts")

    drafts = get_drafts()

    if drafts:

        for draft in drafts:

            draft_id, subject, body, created_at = draft

            with st.expander(f"📧 {subject} | {created_at}"):

                st.write("**Subject:**", subject)

                st.text_area(
                    "Email Content",
                    value=body,
                    height=150,
                    key=f"history_{draft_id}"
                )

                if st.button("Delete Draft", key=f"delete_{draft_id}"):

                    delete_draft(draft_id)

                    st.success("Draft deleted!")

                    st.rerun()

    else:

        st.info("No saved drafts yet.")

st.divider()

st.caption("AI Email Assistant Agent | Powered by Ollama and Llama 3.2")
