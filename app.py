<<<<<<< HEAD
from pathlib import Path

from flask import Flask, send_from_directory
=======
from flask import Flask
>>>>>>> 73af21f54f9b402aae73349e99c9a52ea3c40b0b
from flask_cors import CORS

from api.routes import api_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)

<<<<<<< HEAD
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


@app.route("/", methods=["GET"])
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/frontend/<path:filename>", methods=["GET"])
def serve_frontend_file(filename):
    return send_from_directory(FRONTEND_DIR, filename)

=======
>>>>>>> 73af21f54f9b402aae73349e99c9a52ea3c40b0b

if __name__ == "__main__":
    app.run(debug=True)
