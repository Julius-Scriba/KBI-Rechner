from flask import Flask, jsonify

app = Flask(__name__)

@app.get('/')
def index():
    """Simple placeholder route."""
    return jsonify({"message": "KbI-Rechner API"})


if __name__ == '__main__':
    app.run(debug=True)
