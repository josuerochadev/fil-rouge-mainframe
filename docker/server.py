"""
API web pour executer les programmes COBOL batch compiles avec GnuCOBOL.
Les programmes DB2 et CICS sont presentes en mode documentation (screenshots + rapport).
"""

import os
import subprocess
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)

BIN_DIR = "/app/bin"
DATA_DIR = "/app/01-batch/data"

PROGRAMS = {
    "PJ20RLV": {
        "name": "Releve de compte",
        "description": "Edition d'un releve de compte client avec tri des mouvements par date",
        "input": "Numero de compte (001-020)",
        "phase": "batch",
    },
    "PJ19MOMT": {
        "name": "Mouvements par compte",
        "description": "Extraction et tri des mouvements d'un compte specifique",
        "input": "Numero de compte (001-020)",
        "phase": "batch",
    },
    "PJ21MERG": {
        "name": "Fusion trimestrielle",
        "description": "Fusion des mouvements de 3 mois (Janvier, Fevrier, Mars)",
        "input": None,
        "phase": "batch",
    },
    "PJ16COND": {
        "name": "Analyse par region",
        "description": "Repartition debit/credit par region avec conditions",
        "input": None,
        "phase": "batch",
    },
    "PJ15MONT": {
        "name": "Montants et moyennes",
        "description": "Calcul des montants totaux et moyennes par type",
        "input": None,
        "phase": "batch",
    },
}


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/programs")
def list_programs():
    result = []
    for pgm_id, info in PROGRAMS.items():
        available = os.path.isfile(os.path.join(BIN_DIR, pgm_id))
        result.append({
            "id": pgm_id,
            "available": available,
            **info,
        })
    return jsonify(result)


@app.route("/api/run/<program_id>", methods=["POST"])
def run_program(program_id):
    if program_id not in PROGRAMS:
        return jsonify({"error": "Programme inconnu"}), 404

    binary = os.path.join(BIN_DIR, program_id)
    if not os.path.isfile(binary):
        return jsonify({"error": "Programme non compile"}), 500

    pgm_info = PROGRAMS[program_id]
    stdin_data = ""

    if pgm_info["input"]:
        data = request.get_json(silent=True) or {}
        user_input = data.get("input", "")
        if not user_input:
            return jsonify({"error": f"Entree requise : {pgm_info['input']}"}), 400
        stdin_data = user_input

    env = os.environ.copy()
    env["COB_LIBRARY_PATH"] = BIN_DIR

    try:
        result = subprocess.run(
            [binary],
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=DATA_DIR,
            env=env,
        )
        return jsonify({
            "program": pgm_info["name"],
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout (10s)"}), 504


@app.route("/api/data/<filename>")
def get_data(filename):
    allowed = {"CLIENT.dat", "COMPTE.dat", "PROFES.dat", "REGION.dat"}
    if filename not in allowed:
        return jsonify({"error": "Fichier non autorise"}), 403
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(filepath):
        return jsonify({"error": "Fichier non trouve"}), 404
    with open(filepath, "r") as f:
        lines = f.readlines()
    return jsonify({"filename": filename, "lines": lines, "count": len(lines)})


if __name__ == "__main__":
    # Compiler au demarrage
    os.system("bash /app/compile.sh")
    app.run(host="0.0.0.0", port=8080)
