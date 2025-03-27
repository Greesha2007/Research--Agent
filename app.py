from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "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"  # Replace with your actual API key
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_ai_response(prompt):
    """Get chatbot response from OpenRouter API using gpt-3.5-turbo."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",  # Correct OpenRouter model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        response_json = response.json()

        if "error" in response_json:
            return f"Error: {response_json['error'].get('message', 'Unknown error')}"

        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["message"]["content"]

        return "Error: Unexpected response format."

    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "")
    ai_response = get_ai_response(user_message)
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)