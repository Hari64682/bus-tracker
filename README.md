# 🚌 SNGCE Bus Tracker

Live GPS bus tracking system for SNGCE College.

## How It Works

| Who | What they do |
|-----|-------------|
| **Driver** | Opens `/driver` on phone → selects bus → taps "Start Sharing Location" → GPS sent every 5 s |
| **Student** | Opens `/` → selects bus → sees live map with bus moving in real time |

## Run Locally (same Wi-Fi)

```bash
pip install flask
python app.py
```

- Students open: `http://<your-ip>:5000`
- Driver opens: `http://<your-ip>:5000/driver`

Find your IP: run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

## Deploy Free on Railway.app (public URL)

1. Create account at https://railway.app
2. New Project → Deploy from GitHub repo
3. Push this folder to a GitHub repo
4. Railway auto-detects `Procfile` and deploys
5. Share the URL with drivers and students

## Deploy Free on Render.com

1. Push to GitHub
2. New Web Service at https://render.com
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## File Structure

```
bus_tracker/
├── app.py              ← Flask server + GPS API
├── requirements.txt    ← Dependencies
├── Procfile            ← For Railway/Render
└── templates/
    ├── index.html      ← Student home (bus selector)
    ├── driver.html     ← Driver GPS sharing page
    └── map.html        ← Live tracking map
```
