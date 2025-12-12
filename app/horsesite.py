# horsesite.py - updated with Extract button, new fields, and timestamp feature

import os
import json
import logging
import requests
from datetime import date
from flask import Blueprint, request, render_template, jsonify
from markupsafe import Markup
import markdown

horsesite_bp = Blueprint('horsesite_bp', __name__, url_prefix='/horsesite')

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.environ.get('BASE_DIR', os.getcwd())
PROMPT_FILE = os.path.join(BASE_DIR, os.environ.get('PROMPT_FILE', 'data/prompt_template.txt'))
JSON_PATH = os.path.join(BASE_DIR, os.environ.get('JSON_PATH', 'data/models.json'))

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
logging.info(f"API_KEY={OPENROUTER_API_KEY}")

DEFAULT_PROMPT_TEMPLATE = """# {timestamp}

Start your response with your model name then analyze the following race.

## Race Information
Date: {race_date}
Race Number: {race_number}

{race_info}

## Summary Data
{summary_data}

## Pace Data
{pace_data}

## User Insights
{user_insights}
"""

def build_timestamp(race_date, race_number, race_info):
    """Create 'YYYY-MM-DD • TRACK • Race X' timestamp."""
    track = ""

    if race_info.strip():
        first_line = race_info.strip().splitlines()[0]
        parts = first_line.split()
        if parts:
            track = parts[0]  # e.g., CD, GP, SA, AQU

    timestamp_parts = []
    if race_date:
        timestamp_parts.append(race_date)
    if track:
        timestamp_parts.append(track)
    if race_number:
        timestamp_parts.append(f"Race {race_number}")

    return " • ".join(timestamp_parts)


def load_prompt_from_file(race_info, summary_data, pace_data, race_date, race_number, user_insights):
    try:
        with open(PROMPT_FILE, 'r') as f:
            template = f.read()
    except Exception:
        template = DEFAULT_PROMPT_TEMPLATE

    timestamp = build_timestamp(race_date, race_number, race_info)

    return template.format(
        timestamp=timestamp,
        race_info=race_info,
        summary_data=summary_data,
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


def extract_race_info(summary_data):
    """Implements final Option 3:

    1. Find 'Help us improve Summary'
    2. Find first 'RACE STATS' after that
    3. Extract everything AFTER that → race info
    4. Summary becomes everything ABOVE the help line
    """

    if not summary_data:
        return "", summary_data

    lines = summary_data.splitlines()

    help_idx = None
    for i, line in enumerate(lines):
        if "help us improve summary" in line.lower():
            help_idx = i
            break

    if help_idx is None:
        return "", summary_data

    race_stats_idx = None
    for i in range(help_idx + 1, len(lines)):
        if "race stats" in lines[i].lower():
            race_stats_idx = i
            break

    if race_stats_idx is None:
        return "", summary_data

    extracted_lines = lines[race_stats_idx + 1:]
    race_info_block = "\n".join(extracted_lines).strip()

    cleaned_summary = "\n".join(lines[:help_idx]).strip()

    return race_info_block, cleaned_summary


@horsesite_bp.route('/extract', methods=['POST'])
def extract_route():
    summary_data = request.form.get('summary_data', '').strip()
    race_info = request.form.get('race_info', '').strip()

    if race_info:
        return jsonify({
            "race_info": race_info,
            "summary_data": summary_data,
            "message": "Race Info not empty; extraction skipped."
        })

    extracted, cleaned = extract_race_info(summary_data)

    return jsonify({
        "race_info": extracted,
        "summary_data": cleaned,
        "message": "Extraction completed."
    })


@horsesite_bp.route('/', methods=['GET', 'POST'])
def index():
    MODELS = load_models()
    DEFAULT_MODEL = MODELS[0][1]

    race_info = ''
    summary_data = ''
    pace_data = ''
    user_insights = ''
    race_date = date.today().isoformat()
    race_number = ''
    selected_model = DEFAULT_MODEL
    result_html = None
    error = None

    if request.method == 'POST':
        race_info = request.form.get('race_info', '').strip()
        summary_data = request.form.get('summary_data', '').strip()
        pace_data = request.form.get('pace_data', '').strip()
        user_insights = request.form.get('user_insights', '').strip()
        race_date = request.form.get('race_date', race_date)
        race_number = request.form.get('race_number', '')
        selected_model = request.form.get('model', DEFAULT_MODEL)

        if not (race_info or summary_data or pace_data or user_insights):
            error = "Please provide at least some data."
        elif not OPENROUTER_API_KEY:
            error = "API Key not set."
        else:
            timestamp = build_timestamp(race_date, race_number, race_info)
            prompt = load_prompt_from_file(
                race_info, summary_data, pace_data,
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

                # PREPEND TIMESTAMP TO MARKDOWN SHOWN IN horsesite.html
                final_markdown = f"# {timestamp}\n\n" + raw

                result_html = Markup(markdown.markdown(final_markdown))

            except Exception as e:
                error = f"Error: {str(e)}"

    return render_template(
        'horsesite.html',
        models=MODELS,
        race_info=race_info,
        summary_data=summary_data,
        pace_data=pace_data,
        user_insights=user_insights,
        race_date=race_date,
        race_number=race_number,
        selected_model=selected_model,
        result_html=result_html,
        error=error
    )

