from flask import Flask
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/flask', methods=['GET'])
def index():
    return "Flask server"

if __name__ == "__main__":
    app.run(port=5000, debug=True)