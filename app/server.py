# app/server.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from app.api.routes import rotas



app = Flask(__name__)
app.register_blueprint(rotas)

if __name__ == "__main__":
    app.run(debug=True)
