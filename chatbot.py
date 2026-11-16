"""
FAQ Chatbot — CodeAlpha AI Internship, Task 2.

Matches a user's question to the most similar FAQ using NLP:
  1. Text is cleaned (lowercased, punctuation stripped, extra spaces removed).
  2. Questions are converted into TF-IDF vectors (scikit-learn).
  3. Cosine similarity ranks the FAQs; the best match above the
     similarity threshold is returned, otherwise a fallback reply.

Run this file directly for a quick command-line test:
    python chatbot.py
"""

import json
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Similarity below this value means "I don't know this one".
SIMILARITY_THRESHOLD = 0.20

FALLBACK_ANSWER = (
    "I'm sorry, I don't know the answer to that yet. "
    "Could you rephrase your question, or ask me something about "
    "learning Python — for example, functions, loops, lists, "
    "dictionaries, or error handling?"
)


def clean_text(text):
    """Lowercase, strip punctuation and collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class FAQChatbot:
    """Loads FAQs from JSON and answers questions by TF-IDF similarity."""

    def __init__(self, faqs_path=None):
        if faqs_path is None:
            faqs_path = os.path.join(os.path.dirname(__file__), "faqs.json")
        with open(faqs_path, "r", encoding="utf-8") as f:
            self.faqs = json.load(f)

        self.questions = [item["question"] for item in self.faqs]

        # TF-IDF over the cleaned FAQ questions. English stop words are
        # removed so matching focuses on the meaningful words.
        self.vectorizer = TfidfVectorizer(
            preprocessor=clean_text,
            stop_words="english",
            ngram_range=(1, 2),
        )
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def get_answer(self, user_question):
        """Return (answer, matched_question, similarity_score)."""
        if not user_question or not user_question.strip():
            return FALLBACK_ANSWER, None, 0.0

        user_vector = self.vectorizer.transform([user_question])
        similarities = cosine_similarity(user_vector, self.question_vectors)[0]
        best_index = int(similarities.argmax())
        best_score = float(similarities[best_index])

        if best_score < SIMILARITY_THRESHOLD:
            return FALLBACK_ANSWER, None, round(best_score, 3)

        matched = self.faqs[best_index]
        return matched["answer"], matched["question"], round(best_score, 3)


if __name__ == "__main__":
    bot = FAQChatbot()
    print(f"FAQ Chatbot ready — {len(bot.faqs)} FAQs loaded.")
    print("Type a question about learning Python (or 'quit' to exit).\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Bot: Goodbye! Keep practising Python.")
            break
        answer, matched, score = bot.get_answer(user_input)
        print(f"Bot: {answer}")
        if matched:
            print(f"     (matched: \"{matched}\" — similarity {score})")
        print()
