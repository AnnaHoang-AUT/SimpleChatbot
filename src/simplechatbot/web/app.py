"""Flask web application for SimpleChatbot."""

import logging
import os
from flask import Flask, jsonify, render_template, request
from simplechatbot.chatbot import SimpleChatbot
from simplechatbot.config import AVAILABLE_MODELS, ChatbotConfig

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)

config = ChatbotConfig()
try:
    chatbot = SimpleChatbot(config)
except RuntimeError as e:
    logger.error("Failed to initialize chatbot: %s", e)
    chatbot = None


@app.route("/")
def index():
    models = {key: {"display_name": m.display_name, "description": m.description} for key, m in AVAILABLE_MODELS.items()}
    return render_template("index.html", models=models, current_model=config.model_key)


@app.route("/api/chat", methods=["POST"])
def chat():
    if chatbot is None:
        return jsonify({"error": "Chatbot not initialized. Check AWS credentials."}), 503
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field."}), 400
    user_message = data["message"].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400
    requested_model = data.get("model")
    if requested_model and requested_model != config.model_key:
        try:
            chatbot.set_model(requested_model)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    try:
        response_text = chatbot.get_response(user_message)
        return jsonify({"response": response_text, "model": chatbot.current_model_name})
    except RuntimeError as e:
        logger.error("Chat error: %s", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear", methods=["POST"])
def clear_history():
    if chatbot is None:
        return jsonify({"error": "Chatbot not initialized."}), 503
    chatbot.clear_history()
    return jsonify({"status": "ok"})


@app.route("/api/model", methods=["POST"])
def change_model():
    if chatbot is None:
        return jsonify({"error": "Chatbot not initialized."}), 503
    data = request.get_json()
    if not data or "model" not in data:
        return jsonify({"error": "Missing 'model' field."}), 400
    try:
        chatbot.set_model(data["model"])
        return jsonify({"status": "ok", "model": chatbot.current_model_name})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy" if chatbot else "degraded", "model": chatbot.current_model_name if chatbot else None, "region": config.aws_region})


def main():
    app.run(host=config.flask_host, port=config.flask_port, debug=config.flask_debug)


if __name__ == "__main__":
    main()
