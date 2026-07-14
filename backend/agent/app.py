from flask import Flask, request, jsonify
from agent import handle_query

app = Flask(__name__)

# ✅ Home route (fixes 404)
@app.route("/")
def home():
    return "Backend is running 🚀"


# ✅ Query route
@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return jsonify({
            "message": "Use POST request with JSON body"
        })

    # ✅ Safe JSON handling
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Please provide a 'question' in JSON"
        }), 400

    question = data["question"]

    try:
        answer = handle_query(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)