# 📰 NextWave Stories— Blog Website

A full-featured blog platform built with Python Flask, ready to deploy on Render.

## Features
- User Registration & Login (secure password hashing)
- Create, Read, Delete Blog Posts
- Category Filtering (Technology, Travel, Food, Lifestyle, Photography, Education)
- Search Posts
- Like / Unlike Posts (AJAX)
- Comment System
- User Profile with post stats
- 6 Sample Posts pre-loaded
- Stylish responsive design with Inter + Playfair Display fonts

## Project Structure
```
NextWave Stories/
├── app.py              # Flask application (routes, auth, API)
├── data.json           # Auto-created JSON database
├── requirements.txt
├── render.yaml         # Render deploy config
├── templates/
│   ├── base.html       # Navbar, flash messages, footer
│   ├── index.html      # Home feed
│   ├── post_detail.html
│   ├── create_post.html
│   ├── login.html
│   ├── register.html
│   └── profile.html
└── static/
    ├── css/style.css
    └── js/main.js
```

## Local Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
http://localhost:5000
```

## Deploy on Render (Free)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit — NextWave Stories "
git branch -M main
git remote add origin https://github.com/surya323-ma/NextWave Stories.git
git push -u origin main
```

### Step 2 — Create Render Web Service
1. Go to https://render.com and sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures everything
5. Click **Deploy** — your app goes live in ~2 minutes!

### Step 3 — Environment Variables (auto-set via render.yaml)
- `SECRET_KEY` — auto-generated secure key
- `PORT` — 5000

### Your live URL will be:
`https://inkwell-blog.onrender.com` (or your custom name)

## Notes
- Data is stored in `data.json` (file-based — resets on Render free tier restart)
- For persistent data, upgrade to PostgreSQL on Render
- Default admin account: register with username `admin`
