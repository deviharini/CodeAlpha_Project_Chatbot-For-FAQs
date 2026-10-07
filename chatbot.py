import json
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Download required NLTK data
if nltk is not None:
    nltk.download("stopwords")
    nltk.download("wordnet")
    nltk.download("omw-1.4")


class FAQChatbot:

    def __init__(self, faq_file):

        # Load FAQ data
        with open(faq_file, "r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        self.questions = [
            faq["question"] for faq in self.faqs
        ]

        # NLP tools
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

        # Convert FAQ questions into TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            tokenizer=self.preprocess,
            token_pattern=None
        )

        self.faq_vectors = self.vectorizer.fit_transform(
            self.questions
        )

    def preprocess(self, text):

        # Convert text to lowercase
        text = text.lower()

        # Remove special characters
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # Split text into words
        words = text.split()

        # Remove stopwords and lemmatize
        words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word not in self.stop_words
        ]

        return words

    def get_response(self, user_question):

        # Convert user question into TF-IDF vector
        user_vector = self.vectorizer.transform(
            [user_question]
        )

        # Calculate cosine similarity
        similarities = cosine_similarity(
            user_vector,
            self.faq_vectors
        )

        # Find highest similarity
        best_match_index = similarities.argmax()

        best_score = similarities[0][best_match_index]

        # Minimum similarity required
        threshold = 0.20

        if best_score < threshold:
            return (
                "Sorry, I couldn't find a suitable answer "
                "for your question. Please try asking in a "
                "different way."
            )

        return self.faqs[best_match_index]["answer"]
