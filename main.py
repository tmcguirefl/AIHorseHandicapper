# main.py - main flask program for the Handicapping webapp
# Copyright (c) 2025 tmcguirefl user on github
# This file is part of ProjectName released under the MIT License.
# See LICENSE file in the project root for licensing information.

import os
from flask import Flask, render_template_string
from dotenv import load_dotenv
load_dotenv('./.env')

from app.horsesite import horsesite_bp
from app.horsepdf import split_bp
from app.management import manage_bp


app = Flask(__name__)
app.secret_key = 'unified-horse-key'  # Shared across blueprints


# Register blueprints at desired paths
app.register_blueprint(horsesite_bp)
app.register_blueprint(split_bp)
app.register_blueprint(manage_bp)

@app.route('/')
def home():
    return render_template_string("""
    <h1>Welcome to the Horse Racing Portal 🏇</h1>
    <ul>
        <li><a href="/horsesite">🐴 Horse Data Processor</a></li>
        <li><a href="/pdfPP">📄 Upload & Split PDF</a></li>
        <li><a href="/manage">🗑️ Manage Files</a></li>
    </ul>
    """)

if __name__ == '__main__':
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    host = os.environ.get('FLASK_RUN_HOST','0.0.0.0')
    app.run(host=host, port=port)

