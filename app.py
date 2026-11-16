"""
Flask web app for the FAQ Chatbot — CodeAlpha AI Internship, Task 2.

Routes:
  GET  /     — serves the chat UI (templates/index.html)
  POST /ask  — JSON in:  {"question": "..."}
               JSON out: {"answer": "...", "matched_question": "...",
                          "similarity": 0.0-1.0}

Run with:  python app.py
Then open: http://127.0.0.1:5000
"""

from flask import Flask, jsonify, render_template, request

from chatbot import FAQChatbot

app = Flask(__name__)
bot = FAQChatbot()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "")
    answer, matched_question, score = bot.get_answer(question)
    return jsonify(
        {
            "answer": answer,
            "matched_question": matched_question,
            "similarity": score,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
