"""
API web pour le projet fil-rouge-mainframe.
- Batch : programmes COBOL compiles avec GnuCOBOL
- DB2 : simulation via SQLite (meme schema, memes donnees)
- CICS : replay des ecrans BMS en ASCII art
"""

import os
import subprocess
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from db2_sim import init_db, run_query, QUERIES
from cics_screens import get_screens_list, get_screen

app = Flask(__name__, static_folder="static")
CORS(app)

BIN_DIR = "/app/bin"
DATA_DIR = "/app/01-batch/data"

PROGRAMS = {
    "PJ10ACT": {
        "name": "Edition par activite",
        "description": "Liste des clients tries par activite professionnelle",
        "input": None,
        "phase": "batch",
    },
    "PJ10REG": {
        "name": "Edition par region",
        "description": "Liste des clients tries par region",
        "input": None,
        "phase": "batch",
    },
    "PJ14MAIN": {
        "name": "Tables de reference",
        "description": "Edition des 3 tables (regions, comptes, professions)",
        "input": None,
        "phase": "batch",
    },
    "PJ15MONT": {
        "name": "Montants et moyennes",
        "description": "Calcul des montants totaux et moyennes par type",
        "input": None,
        "phase": "batch",
    },
    "PJ16COND": {
        "name": "Analyse par region",
        "description": "Repartition debit/credit par region avec conditions",
        "input": None,
        "phase": "batch",
    },
    "PJ17TOP5": {
        "name": "Top 5 debiteurs",
        "description": "Classement des 5 plus gros clients debiteurs",
        "input": None,
        "phase": "batch",
    },
    "PJ19MOMT": {
        "name": "Mouvements par compte",
        "description": "Extraction et tri des mouvements d'un compte specifique",
        "input": "Numero de compte (001-020)",
        "phase": "batch",
    },
    "PJ20RLV": {
        "name": "Releve de compte",
        "description": "Edition d'un releve de compte client avec tri des mouvements par date",
        "input": "Numero de compte (001-020)",
        "phase": "batch",
    },
    "PJ21MERG": {
        "name": "Fusion trimestrielle",
        "description": "Fusion des mouvements de 3 mois (Janvier, Fevrier, Mars)",
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

    edition_file = os.path.join(DATA_DIR, "EDITION.txt")
    if os.path.isfile(edition_file):
        os.remove(edition_file)

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
        edition = ""
        if os.path.isfile(edition_file):
            with open(edition_file, "r") as f:
                edition = f.read()

        return jsonify({
            "program": pgm_info["name"],
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "edition": edition,
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout (10s)"}), 504


@app.route("/api/data/<filename>")
def get_data(filename):
    allowed = {"CLIENT.dat", "COMPTE.dat", "PROFES.dat", "REGION.dat",
                "MOUVEMENT.dat", "MOUVJANV.dat", "MOUVFEVR.dat",
                "MOUVMARS.dat"}
    if filename not in allowed:
        return jsonify({"error": "Fichier non autorise"}), 403
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(filepath):
        return jsonify({"error": "Fichier non trouve"}), 404
    with open(filepath, "r") as f:
        lines = f.readlines()
    return jsonify({"filename": filename, "lines": lines, "count": len(lines)})


@app.route("/api/db2/queries")
def list_queries():
    result = []
    for qid, q in QUERIES.items():
        result.append({
            "id": qid,
            "name": q["name"],
            "program": q["program"],
            "input": q.get("input"),
        })
    return jsonify(result)


@app.route("/api/db2/run/<query_id>", methods=["POST"])
def run_db2_query(query_id):
    params = None
    q = QUERIES.get(query_id, {})
    if q.get("input"):
        data = request.get_json(silent=True) or {}
        user_input = data.get("input", "").strip()
        if not user_input:
            return jsonify({"error": f"Entree requise : {q['input']}"}), 400
        params = (user_input,)
    return jsonify(run_query(query_id, params))


@app.route("/api/cics/screens")
def list_cics_screens():
    return jsonify(get_screens_list())


@app.route("/api/cics/screen/<screen_id>")
def show_cics_screen(screen_id):
    step = request.args.get("step", 0, type=int)
    return jsonify(get_screen(screen_id, step))


if __name__ == "__main__":
    os.system("bash /app/compile.sh")
    init_db()
    app.run(host="0.0.0.0", port=8080)
