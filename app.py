"""Flask application exposing calculation endpoints."""

from flask import Flask, jsonify, request
from flask_cors import CORS

from logic.calculation import coin_value_from_weight

app = Flask(__name__)
CORS(app)

@app.get('/')
def index():
    """Simple placeholder route."""
    return jsonify({"message": "KbI-Rechner API"})


@app.post('/calculate')
def calculate():
    """Calculate coin value and count from weight measurement.

    Expects JSON with ``coin_value``, ``measured_weight`` and ``tare_weight``.
    Returns the calculated monetary value and number of coins detected.
    """
    data = request.get_json(force=True, silent=True) or {}
    try:
        coin_value = float(data['coin_value'])
        measured_weight = float(data['measured_weight'])
        tare_weight = float(data.get('tare_weight', 0))
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Invalid input"}), 400

    try:
        value, count = coin_value_from_weight(
            measured_weight, coin_value, extra_weight=tare_weight
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"calculated_value": value, "coin_count": count})


if __name__ == '__main__':
    app.run(debug=True)
