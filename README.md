# 🎵 Mashup Generator Web App

A Flask-based web application that automatically downloads songs of a singer, trims them, merges them into a mashup, and emails the final MP3 to the user.

🚀 **Live Demo:** https://mashup-generator-5.onrender.com/

---

# 📌 Features

✅ Download songs automatically using yt-dlp  
✅ Trim audio using MoviePy  
✅ Merge multiple clips into one mashup  
✅ Generate MP3 output  
✅ Zip file automatically  
✅ Send mashup to user via email  
✅ Simple web interface (Flask + HTML)  
✅ Cloud deployed on Render  

---

# 🛠 Tech Stack

- Python 3
- Flask
- MoviePy
- yt-dlp
- yagmail (Gmail email sender)
- Gunicorn
- Render (deployment)

---

# 📂 Project Structure

```
MashupProject/
│
├── app.py                # Flask web app
├── 102303670.py          # Mashup generation script
├── requirements.txt      # Dependencies
├── templates/
│     └── index.html      # Frontend form
├── outputs/              # Generated mashups
├── README.md
└── .gitignore
```

---

# ⚙️ How It Works

1. User enters:
   - Singer name
   - Number of videos
   - Duration
   - Email

2. Backend:
   - Downloads YouTube videos
   - Extracts audio
   - Trims clips
   - Merges clips
   - Creates result.mp3
   - Zips file
   - Sends email

3. User receives mashup automatically 🎧

---

# 💻 Run Locally

## Step 1 — Clone repo
```
git clone https://github.com/<your-username>/mashup-generator.git
cd mashup-generator
```

## Step 2 — Install dependencies
```
pip install -r requirements.txt
```

## Step 3 — Run server
```
python app.py
```

## Step 4 — Open browser
```
http://127.0.0.1:5000
```

---

# 🔐 Gmail Setup (IMPORTANT)

To send emails using yagmail:

### Enable 2-Step Verification
Google Account → Security → Turn ON 2FA

### Create App Password
Google → App Passwords → Generate password

### Add to app.py
```python
yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")
```

⚠️ Never upload real passwords to GitHub. Use environment variables in production.

---

# ☁️ Deploy on Render

Create a new **Web Service** and use:

## Build Command
```
pip install -r requirements.txt
```

## Start Command
```
gunicorn app:app
```

---

# 📦 requirements.txt

```
flask
gunicorn
moviepy
imageio-ffmpeg
yt-dlp
yagmail
```

---

# 🚫 .gitignore (recommended)

```
outputs/
videos/
audios/
*.mp3
*.zip
__pycache__/
.env
```

---

# 🧠 Common Errors & Fixes

## moviepy.editor not found
✔ Add moviepy inside requirements.txt

## outputs/result.mp3 not found
✔ Add this before subprocess:
```python
os.makedirs("outputs", exist_ok=True)
```

## flask not recognized
✔ Use:
```
python -m flask run
```

## Gmail Authentication Error
✔ Use Gmail App Password (NOT your real password)

---

# 🎯 Future Improvements

- Progress bar
- Multiple formats
- Download button instead of email
- Background task queue
- Cloud storage
- Better UI/UX

---

# 👨‍💻 Author

Karan Veer  
Computer Science Student  
Mashup Generator Project  

---

# ⭐ If you like this project

Give it a ⭐ on GitHub!
