# horsepdf.py - splits a large past performance pdf file into its races 
#               so they can be sent to an LLM via openrouter
#
## Copyright (c) 2025 tmcguirefl user on github
# This file is part of ProjectName released under the MIT License.
# See LICENSE file in the project root for licensing information.

import os, re, json, logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
import requests

split_bp = Blueprint('split_bp', __name__, url_prefix='/pdfPP')

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load paths from environment
BASE_DIR = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE_DIR, os.environ.get('UPLOAD_FOLDER', 'uploads'))
SPLIT_FOLDER = os.path.join(BASE_DIR, os.environ.get('SPLIT_FOLDER', 'split_races'))
MODELS_FILE = os.path.join(BASE_DIR, os.environ.get('MODELS_FILE', 'data/models.json'))
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SPLIT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def get_available_models():
    if os.path.exists(MODELS_FILE):
        try:
            with open(MODELS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load models.json: {e}")
            pass
    return [
        {"display_name": "GPT-4o", "model_id": "openai/gpt-4o-latest"}
    ]

def allowed_file(filename):
    return filename.lower().endswith('.pdf')

def extract_race_number(text):
    match = re.search(r"Race\s+(\d+)", text)
    return int(match.group(1)) if match else None

def split_pdf_by_race(filepath, subname):
    subdir_path = os.path.join(SPLIT_FOLDER, subname)
    os.makedirs(subdir_path, exist_ok=True)
    reader = PdfReader(filepath)
    writer = PdfWriter()
    race_num, output_files = None, []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        new_race = extract_race_number(text)
        if new_race and race_num != new_race and writer.pages:
            out_file = f'Race_{race_num}.pdf'
            with open(os.path.join(subdir_path, out_file), 'wb') as f:
                writer.write(f)
            output_files.append(out_file)
            writer = PdfWriter()
        race_num = new_race or race_num
        writer.add_page(page)

    if writer.pages:
        out_file = f'Race_{race_num}.pdf'
        with open(os.path.join(subdir_path, out_file), 'wb') as f:
            writer.write(f)
        output_files.append(out_file)

    return output_files

def query_openrouter(model, text_content):
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not set in environment variables."

    logger.info(f"Sending request to OpenRouter using model: {model}")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Horse Racing PP Analyzer",
        "Content-Type": "application/json"
    }

    prompt = f"Please identify yourself in the first line of your response.\n\nHere is the past performance data for a horse race. Please analyze it:\n\n{text_content}"

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"OpenRouter API Error: {e}")
        return f"API Error: {str(e)}"

@split_bp.route('/', methods=['GET'])
def index():
    subdirs = sorted([d for d in os.listdir(SPLIT_FOLDER) if os.path.isdir(os.path.join(SPLIT_FOLDER, d))])
    files = {d: sorted(os.listdir(os.path.join(SPLIT_FOLDER, d))) for d in subdirs}
    return render_template('horsepdf.html', models=[m['display_name'] for m in get_available_models()], directories=subdirs, files=files)

@split_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file or not allowed_file(file.filename):
        flash("Invalid file.")
        return redirect(url_for('split_bp.index'))

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    base = os.path.splitext(filename)[0]
    try:
        split_pdf_by_race(path, base)
        flash(f"Split into races successfully.")
    except Exception as e:
        flash(f"Error: {e}")
    return redirect(url_for('split_bp.index'))

@split_bp.route('/process', methods=['POST'])
def process():
    selected_files = request.form.getlist('race_files')
    selected_dir = request.form.get('directory')
    selected_display_name = request.form.get('model')
    user_instructions = request.form.get('instructions', '').strip()

    if not selected_files or not selected_dir or not selected_display_name:
        flash("Please select a directory, 1-3 files, and a model.")
        return redirect(url_for('split_bp.index'))

    if len(selected_files) > 3:
        flash("Please select no more than 3 race files.")
        return redirect(url_for('split_bp.index'))

    model_id = next((m['model_id'] for m in get_available_models() if m['display_name'] == selected_display_name), None)
    if not model_id:
        flash("Selected model not found.")
        return redirect(url_for('split_bp.index'))

    try:
        text_content = ""
        for filename in selected_files:
            file_path = os.path.join(SPLIT_FOLDER, selected_dir, filename)
            reader = PdfReader(file_path)
            text_content += f"\n\n--- {filename} ---\n"
            text_content += "\n".join([p.extract_text() for p in reader.pages])

        if user_instructions:
            text_content = f"User instructions: {user_instructions}\n\n{text_content}"

        llm_response = query_openrouter(model_id, text_content)

        return render_template(
            'result.html',
            response=llm_response,
            filename=", ".join(selected_files),
            model=selected_display_name
        )

    except Exception as e:
        logger.error(f"Processing Error: {e}")
        flash(f"Error processing races: {e}")
        return redirect(url_for('split_bp.index'))

