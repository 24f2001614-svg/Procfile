# Analytics API – Deployment Guide

Files: `app.py`, `requirements.txt`, `Procfile`, `test.sh`

## 1. Set your email
Either set an `EMAIL` environment variable on the host (recommended), or edit the default in `app.py`.
Use the exact email you are logged in with on the exam page.

## 2. (Optional) Test locally
    pip install -r requirements.txt
    EMAIL=you@example.com python app.py
    ./test.sh http://localhost:8000/analytics

## 3. Push to GitHub
1. Create a new GitHub repo (public or private).
2. Upload all files from this folder to the repo root.

## 4. Deploy on Render (free)
1. Sign in at https://render.com with GitHub.
2. New -> Web Service -> pick your repo.
3. Runtime: Python 3
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Environment -> Add variable: `EMAIL` = your logged-in email
7. Create Web Service and wait for "Live".

Your URL: `https://<service-name>.onrender.com/analytics`

## 5. Verify
    ./test.sh https://<service-name>.onrender.com/analytics
Expected: 401, 401, then JSON with total_events 3, unique_users 2, revenue 12.5, top_user "a".

## 6. Submit
Paste the full URL ending in `/analytics`.
Free tier sleeps when idle: open the URL / run test.sh right before the grader checks.

Alternatives: Railway, Fly.io, or PythonAnywhere work too (same code; start command `gunicorn app:app`).
