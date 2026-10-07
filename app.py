from flask import Flask, render_template, request, jsonify  # type: ignore[import-not-found]
from chatbot import FAQChatbot


app = Flask(__name__)

# Create chatbot
chatbot = FAQChatbot("faq_data.json")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_question = data.get("question", "").strip()

    if not user_question:
        return jsonify({
            "answer": "Please enter a question."
        })

    answer = chatbot.get_response(user_question)

    return jsonify({
        "answer": answer
    })


if __name__ == "__main__":
    app.run(debug=True)
