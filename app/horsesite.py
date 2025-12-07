# horsesite.py - cut and paste data twinspires provides in there betting application
#                the summary table and it's race info line; the pace data table
#
# Copyright (c) 2025 tmcguirefl user on github
# This file is part of ProjectName released under the MIT License.
# See LICENSE file in the project root for licensing information.

import os
import json
import logging
import requests
from flask import Blueprint, request, render_template

# Create the blueprint
horsesite_bp = Blueprint('horsesite_bp', __name__, url_prefix='/horsesite')

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Load paths from environment or set default
BASE_DIR = os.environ.get('BASE_DIR', os.getcwd())
PROMPT_FILE = os.path.join(BASE_DIR, os.environ.get('PROMPT_FILE', 'data/prompt_template.txt'))
JSON_PATH = os.path.join(BASE_DIR, os.environ.get('JSON_PATH', 'data/models.json'))

# Default prompt template fallback
DEFAULT_PROMPT_TEMPLATE = """You are an expert horse racing analyst.

Start your response with your model name then
Analyze the following horse racing data and provide:
- Key insights from each section
- Top horse picks with reasoning
- Predicted winner(s) and placers
- Value bets or risks
- Any other relevant advice

Structure your response clearly.

## Race Information
{race_info}

## Summary Data
{summary_data}

## Pace Data
{pace_data}
"""

def load_prompt_from_file(race_info, summary_data, pace_data):
    """Reads the prompt template from a file, or fallbacks to default if error occurs."""
    try:
        with open(PROMPT_FILE, 'r') as f:
            template = f.read()
        logging.info(f"Loaded prompt template from {PROMPT_FILE}")
    except Exception as e:
        logging.warning(f"Error loading prompt file: {e}")
        template = DEFAULT_PROMPT_TEMPLATE
    return template.format(
        race_info=race_info,
        summary_data=summary_data,
        pace_data=pace_data
    )

def load_models():
    """Reads the list of models from a JSON file."""
    try:
        with open(JSON_PATH, 'r') as f:
            models_data = json.load(f)
        return [(m['display_name'], m['model_id']) for m in models_data]
    except Exception as e:
        logging.warning(f"Error loading models from {JSON_PATH}: {e}")
        return [
            ("GPT-4o", "openai/gpt-4o"),
            ("Claude 3.5 Sonnet", "anthropic/claude-3.5-sonnet")
        ]

@horsesite_bp.route('/', methods=['GET', 'POST'])
def index():
    MODELS = load_models()
    DEFAULT_MODEL = MODELS[0][1] if MODELS else "anthropic/claude-3.5-sonnet"
    race_info, summary_data, pace_data = '', '', ''
    selected_model, result, error = DEFAULT_MODEL, None, None

    if request.method == 'POST':
        race_info = request.form.get('race_info', '').strip()
        summary_data = request.form.get('summary_data', '').strip()
        pace_data = request.form.get('pace_data', '').strip()
        selected_model = request.form.get('model', DEFAULT_MODEL)

        if not (race_info or summary_data or pace_data):
            error = "Please provide at least some data."
        else:
            prompt = load_prompt_from_file(race_info, summary_data, pace_data)

            try:
                from app.config import API_KEY  # Assumes you have centralized API key config
                response = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers={
                        'Authorization': f'Bearer {API_KEY}',
                        'Content-Type': 'application/json',
                        'HTTP-Referer': 'http://localhost:5000/',
                        'X-Title': 'Horse Racing Analyzer',
                    },
                    json={
                        'model': selected_model,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'temperature': 0.7,
                        'max_tokens': 4000,
                    },
                )
                response.raise_for_status()
                result = response.json()['choices'][0]['message']['content']
            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template(
        'horsesite.html',
        models=MODELS,
        race_info=race_info,
        summary_data=summary_data,
        pace_data=pace_data,
        selected_model=selected_model,
        result=result,
        error=error
    )

