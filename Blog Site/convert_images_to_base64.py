#!/usr/bin/env python3
"""Migration helper: convert existing image files referenced in DB to base64 data URIs.

Usage: python3 convert_images_to_base64.py

This script will:
 - load the Flask app and DB (via main.py)
 - find User.profile_pic and Post.image values that are filenames (not data URIs)
 - if corresponding file exists under app.config['UPLOAD_FOLDER'], read and convert to data URI and save back to DB
 - commit changes

Make a DB backup before running.
"""
import os
import base64
import mimetypes
from main import app, db
from model import User, Post

UPLOAD_FOLDER = app.config.get('UPLOAD_FOLDER', 'static')

def file_to_data_uri(path):
    mime = mimetypes.guess_type(path)[0] or 'image/png'
    with open(path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    return f"data:{mime};base64,{b64}"

with app.app_context():
    updated = 0
    # Users
    users = User.query.all()
    for u in users:
        val = (u.profile_pic or '')
        if val and not val.startswith('data:'):
            candidate = os.path.join(UPLOAD_FOLDER, val)
            if os.path.exists(candidate):
                try:
                    u.profile_pic = file_to_data_uri(candidate)
                    updated += 1
                except Exception as e:
                    print(f"Failed to convert user {u.id} file {candidate}: {e}")
            else:
                print(f"User {u.id} profile file not found: {candidate}")

    # Posts
    posts = Post.query.all()
    for p in posts:
        val = (p.image or '')
        if val and not val.startswith('data:'):
            candidate = os.path.join(UPLOAD_FOLDER, val)
            if os.path.exists(candidate):
                try:
                    p.image = file_to_data_uri(candidate)
                    updated += 1
                except Exception as e:
                    print(f"Failed to convert post {p.post_id} file {candidate}: {e}")
            else:
                print(f"Post {p.post_id} image file not found: {candidate}")

    if updated:
        db.session.commit()
        print(f"Updated {updated} image fields to data URIs.")
    else:
        print("No updates performed.")
