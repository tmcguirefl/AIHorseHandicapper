# horseinput.py - Flask blueprint for manual horse racing data input and LLM analysis
# Copyright (c) 2025 tmcguirefl user on github
# This file is part of AIHorseHandicapper project released under the MIT License.
# See LICENSE file in the project root for licensing information.

import os
import json
import logging
import requests
from datetime import date
from flask import Blueprint, request, render_template, jsonify
from markupsafe import Markup
import markdown

horseinput_bp = Blueprint('horseinput_bp', __name__, url_prefix='/horseinput')

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.environ.get('BASE_DIR', os.getcwd())
PROMPT_FILE = os.path.join(BASE_DIR, os.environ.get('PROMPT_FILE2', 'data/prompt_template2.txt'))
JSON_PATH = os.path.join(BASE_DIR, os.environ.get('JSON_PATH', 'data/models.json'))

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
logging.info(f"API_KEY={OPENROUTER_API_KEY}")

DEFAULT_PROMPT_TEMPLATE = """# {timestamp}

Start your response with your model name then analyze the following race.

## Race Information
Date: {race_date}
Track: {track}
Race Number: {race_number}

## Speed Data
{speed_data}

## Class Data
{class_data}

## Pace Data
{pace_data}

## User Insights
{user_insights}
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


def load_prompt_from_file(track, speed_data, class_data, pace_data, race_date, race_number, user_insights):
    try:
        with open(PROMPT_FILE, 'r') as f:
            template = f.read()
    except Exception:
        template = DEFAULT_PROMPT_TEMPLATE

    timestamp = build_timestamp(track, race_date, race_number)

    return template.format(
        timestamp=timestamp,
        track=track,
        speed_data=speed_data,
        class_data=class_data,
        pace_data=pace_data,
        race_date=race_date,
        race_number=race_number,
        user_insights=user_insights
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


@horseinput_bp.route('/', methods=['GET', 'POST'])
def index():
    MODELS = load_models()
    DEFAULT_MODEL = MODELS[0][1]

    track = ''
    speed_data = ''
    class_data = ''
    pace_data = ''
    user_insights = ''
    race_date = date.today().isoformat()
    race_number = '1'  # Default for select
    selected_model = DEFAULT_MODEL
    result_html = None
    error = None

    if request.method == 'POST':
        track = request.form.get('track', '').strip()
        speed_data = request.form.get('speed_data', '').strip()
        class_data = request.form.get('class_data', '').strip()
        pace_data = request.form.get('pace_data', '').strip()
        user_insights = request.form.get('user_insights', '').strip()
        race_date = request.form.get('race_date', race_date)
        race_number = request.form.get('race_number', race_number)
        selected_model = request.form.get('model', DEFAULT_MODEL)

        if not (track or speed_data or class_data or pace_data or user_insights):
            error = "Please provide at least some data."
        elif not OPENROUTER_API_KEY:
            error = "API Key not set."
        else:
            timestamp = build_timestamp(track, race_date, race_number)
            prompt = load_prompt_from_file(
                track, speed_data, class_data, pace_data,
                race_date, race_number, user_insights
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

                # PREPEND TIMESTAMP TO MARKDOWN SHOWN IN horseinput.html
                final_markdown = f"# {timestamp}\n\n" + raw

                result_html = Markup(markdown.markdown(final_markdown))

            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template(
        'horseinput.html',
        models=MODELS,
        track=track,
        speed_data=speed_data,
        class_data=class_data,
        pace_data=pace_data,
        user_insights=user_insights,
        race_date=race_date,
        race_number=race_number,
        selected_model=selected_model,
        result_html=result_html,
        error=error
    )
