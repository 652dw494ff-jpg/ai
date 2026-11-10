import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from aura_core.core import AuraCore

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder="static", template_folder="templates")
core = AuraCore(data_dir=ROOT / "data")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/status")
def status():
    return jsonify(core.status())

@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "Napiš zprávu."}), 400
    if len(message) > 1000:
        return jsonify({"error": "Zpráva je příliš dlouhá (max. 1000 znaků)."}), 400
    answer = core.reply(message)
    return jsonify({"reply": answer, "engine": core.engine_name})

@app.post("/api/train")
def train():
    # Intentionally limited to the bundled small corpus. This endpoint does not
    # accept arbitrary uploads or run user-provided code.
    result = core.train()
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
