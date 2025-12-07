# management.py - application to help delete files to save space and keep the 
#                 app manageable in a single screen
#
# Copyright (c) 2025 tmcguirefl user on github
# This file is part of ProjectName released under the MIT License.
# See LICENSE file in the project root for licensing information.

from flask import Blueprint, render_template, flash, redirect, url_for
import os, shutil

manage_bp = Blueprint('manage_bp', __name__, url_prefix='/manage')

UPLOAD_FOLDER = 'uploads'
SPLIT_FOLDER = 'split_races'

@manage_bp.route('/', methods=['GET'])
def index():
    subdirs = sorted([d for d in os.listdir(SPLIT_FOLDER) if os.path.isdir(os.path.join(SPLIT_FOLDER, d))])
    return render_template('manage.html', subdirs=subdirs)

@manage_bp.route('/delete/<subdir>', methods=['POST'])
def delete(subdir):
    split_dir = os.path.join(SPLIT_FOLDER, subdir)
    upload_pdf = os.path.join(UPLOAD_FOLDER, f"{subdir}.pdf")
    if os.path.exists(split_dir):
        shutil.rmtree(split_dir)
        flash(f"Deleted {split_dir}")
    if os.path.exists(upload_pdf):
        os.remove(upload_pdf)
        flash(f"Deleted {upload_pdf}")
    return redirect(url_for('manage_bp.index'))
