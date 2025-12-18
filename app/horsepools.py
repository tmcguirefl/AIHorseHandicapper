# horsepools.py - Flask blueprint for manual pool data input and LLM analysis
# Copyright (c) 2025 tmcguirefl user on github
# This file is part of ProjectName released under the MIT License.
# See LICENSE file in the project root for licensing information.

import os
import json
import logging
import requests
from datetime import date
from flask import Blueprint, request, render_template, jsonify
from markupsafe import Markup
import markdown

horsepools_bp = Blueprint('horsepools_bp', __name__, url_prefix='/horsepools')

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.environ.get('BASE_DIR', os.getcwd())
PROMPT_FILE = os.path.join(BASE_DIR, os.environ.get('PROMPT_FILE3', 'data/prompt_template3.txt'))
JSON_PATH = os.path.join(BASE_DIR, os.environ.get('JSON_PATH', 'data/models.json'))

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
logging.info(f"API_KEY={OPENROUTER_API_KEY}")

DEFAULT_PROMPT_TEMPLATE = """# {timestamp}

Start your response with your model name then analyze the following pools data for handicapping the race.

## Race Information
Date: {race_date}
Track: {track}
Race Number: {race_number}

## Pools Data
{pools_data}
"""

def build_timestamp(track, race_date, race_number):
    """Create 'YYYY-MM-DD • TRACK • Race X' timestamp."""
    timestamp_parts = []
    if race_date:
        timestamp_parts.append(race_date)
    if track:
        timestamp_parts.append(track.upper())
    if race_number:
        timestamp_parts.append(f"Race {race_number}")

    return " • ".join(timestamp_parts)


def load_prompt_from_file(track, pools_data, race_date, race_number):
    try:
        with open(PROMPT_FILE, 'r') as f:
            template = f.read()
    except Exception:
        template = DEFAULT_PROMPT_TEMPLATE

    timestamp = build_timestamp(track, race_date, race_number)

    return template.format(
        timestamp=timestamp,
        track=track,
        pools_data=pools_data,
        race_date=race_date,
        race_number=race_number
    )


def load_models():
    try:
        with open(JSON_PATH, 'r') as f:
            models_data = json.load(f)
        return [(m['display_name'], m['model_id']) for m in models_data]
    except Exception:
        return [
            ("GPT-4o", "openai/gpt-4o"),
            ("Claude 3.5 Sonnet", "anthropic/claude-3.5-sonnet")
        ]


@horsepools_bp.route('/', methods=['GET', 'POST'])
def index():
    MODELS = load_models()
    DEFAULT_MODEL = MODELS[0][1]

    track = ''
    pools_data = ''
    race_date = date.today().isoformat()
    race_number = '1'  # Default for select
    selected_model = DEFAULT_MODEL
    result_html = None
    error = None

    if request.method == 'POST':
        track = request.form.get('track', '').strip()
        pools_data = request.form.get('pools_data', '').strip()
        race_date = request.form.get('race_date', race_date)
        race_number = request.form.get('race_number', race_number)
        selected_model = request.form.get('model', DEFAULT_MODEL)

        if not (track or pools_data):
            error = "Please provide at least some data."
        elif not OPENROUTER_API_KEY:
            error = "API Key not set."
        else:
            timestamp = build_timestamp(track, race_date, race_number)
            prompt = load_prompt_from_file(
                track, pools_data, race_date, race_number
            )

            headers = {
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:5500/',
                'X-Title': 'Horse Racing Analyzer'
            }

            data = {
                'model': selected_model,
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.7,
                'max_tokens': 4000
            }

            try:
                response = requests.post(
                    'https://openrouter.ai/api/v1/chat/completions',
                    headers=headers,
                    json=data
                )
                response.raise_for_status()

                raw = response.json()['choices'][0]['message']['content']

                # PREPEND TIMESTAMP TO MARKDOWN SHOWN IN horsepools.html
                final_markdown = f"# {timestamp}\n\n" + raw

                result_html = Markup(markdown.markdown(final_markdown))

            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template(
        'horsepools.html',
        models=MODELS,
        track=track,
        pools_data=pools_data,
        race_date=race_date,
        race_number=race_number,
        selected_model=selected_model,
        result_html=result_html,
        error=error
    )

