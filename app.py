import os
from collections import defaultdict
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

API_KEY = "ak_9vlx1da6klbcb65x4ahw1s0u"
EMAIL = os.environ.get("EMAIL", "YOUR_LOGGED_IN_EMAIL@example.com")


@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
    resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return resp


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/analytics", methods=["POST", "OPTIONS"])
def analytics():
    if request.method == "OPTIONS":  # CORS preflight (no auth)
        return make_response("", 204)

    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    body = request.get_json(silent=True) or {}
    events = body.get("events") or []

    users = set()
    totals = defaultdict(float)
    revenue = 0.0

    for e in events:
        if not isinstance(e, dict):
            continue
        user = e.get("user")
        users.add(user)
        try:
            amount = float(e.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        if amount > 0:
            revenue += amount
            totals[user] += amount

    top_user = max(totals, key=totals.get) if totals else None

    return jsonify({
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
