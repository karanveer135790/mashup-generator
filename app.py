from flask import Flask, render_template, request
import subprocess
import yagmail
import zipfile
import os
import sys

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    singer = request.form["singer"]
    number = request.form["number"]
    duration = request.form["duration"]
    email = request.form["email"]

    output_file = "result.mp3"

    # ensure outputs folder exists
    os.makedirs("outputs", exist_ok=True)

    # run mashup script safely
    subprocess.run([
        "python",          # safer than "python"
        "102303670.py",
        singer,
        number,
        duration,
        output_file
    ])

    # zip output
    zip_name = "result.zip"
    with zipfile.ZipFile(zip_name, "w") as z:
        z.write(f"outputs/{output_file}")

    # send email (USE ENV VARIABLES FOR PASSWORD)
    yag = yagmail.SMTP(
        os.getenv("EMAIL_USER"),
        os.getenv("EMAIL_PASS")
    )

    yag.send(
        to=email,
        subject="Your Mashup is Ready!",
        contents="Attached is your mashup file.",
        attachments=zip_name
    )

    return "Mashup sent to your email!"


# Works BOTH locally and on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
