# Python FAQ Chatbot

A simple FAQ chatbot that answers questions about **learning Python programming**.
Built with Python, Flask and scikit-learn (TF-IDF + cosine similarity).

**Author:** Abdullah Bin Haseeb
**Internship:** CodeAlpha AI Internship
**Student ID:** CA/DF1/321398

## What it does

- The bot stores 24 frequently asked questions (with answers) about learning
  Python in `faqs.json` — topics include installing Python, variables, data
  types, functions, loops, lists vs tuples, dictionaries, classes, modules,
  pip, error handling, file handling, virtual environments and more.
- When you type a question, the bot finds the most similar FAQ and returns
  its answer. If no FAQ is similar enough, it says so and suggests asking
  differently.
- A clean chat UI (message bubbles, input box, send button, clickable
  example questions) is served by Flask.

## How the matching works

1. **Preprocessing** — text is lowercased, punctuation is stripped and
   extra spaces are removed (`clean_text` in `chatbot.py`).
2. **TF-IDF vectorization** — each FAQ question is turned into a TF-IDF
   vector with scikit-learn's `TfidfVectorizer` (English stop words removed,
   unigrams + bigrams).
3. **Cosine similarity** — the user's question is vectorized the same way
   and compared against all FAQ questions. The FAQ with the highest cosine
   similarity wins.
4. **Threshold** — if the best similarity is below `0.20`, the bot replies
   with a fallback message ("I don't know the answer to that yet...") and
   suggests rephrasing or asking about a Python topic instead.

## Project structure

```
CodeAlpha_FAQChatbot/
├── app.py                 # Flask app: chat UI + /ask JSON endpoint
├── chatbot.py             # FAQ loading, cleaning, TF-IDF + cosine matching
├── faqs.json              # 24 Python-learning Q&A pairs
├── requirements.txt       # flask, scikit-learn
├── README.md
├── .gitignore
└── templates/
    └── index.html         # Chat UI (bubbles, input box, send button)
```

## Setup and run

```bash
cd CodeAlpha_FAQChatbot

# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the app
python app.py

# 4. Open in your browser
#    http://127.0.0.1:5000
```

## API

`POST /ask` — JSON request and response:

```json
// Request
{ "question": "how do I define a function in Python" }

// Response
{
  "answer": "Use the 'def' keyword ...",
  "matched_question": "How do I define a function in Python?",
  "similarity": 0.68
}
```

`similarity` is a number from 0 to 1. `matched_question` is `null` when the
fallback reply is used.

## Try the chatbot from the command line

```bash
python chatbot.py
```

## Verified behaviour

- `GET /` returns the chat page (HTTP 200).
- Asking "how do I define a function in Python" returns the functions FAQ
  answer with a high similarity score.
- Asking an unrelated question such as "what is the weather" returns the
  fallback response ("I don't know the answer to that yet...").
