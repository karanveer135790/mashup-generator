import os
import sys
import subprocess
import zipfile
from flask import Flask, render_template, request, jsonify
import yagmail  # still required if you want email sending; it's safe because we check credentials

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    singer = request.form.get("singer", "").strip()
    number = request.form.get("number", "1").strip()
    duration = request.form.get("duration", "10").strip()
    email = request.form.get("email", "").strip()

    output_file = "result.mp3"
    zip_name = "result.zip"

    # 1) ensure folders exist
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)

    # 2) run mashup script using same python interpreter as running Gunicorn
    cmd = [
        sys.executable,             # ensures correct interpreter inside the Render venv
        "102303670.py",
        singer,
        number,
        duration,
        output_file
    ]

    try:
        # run and capture logs for debugging
        proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=1800)
        run_stdout = proc.stdout
        run_stderr = proc.stderr
    except subprocess.CalledProcessError as e:
        # return error and log in Render logs
        err_msg = f"Subprocess failed: returncode={e.returncode}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}"
        app.logger.error(err_msg)
        return f"Error creating mashup:\n{err_msg}", 500
    except subprocess.TimeoutExpired as e:
        app.logger.error("Mashup script timed out")
        return "Mashup script timed out", 500
    except Exception as e:
        app.logger.exception("Unexpected error running mashup script")
        return f"Unexpected error: {e}", 500

    # 3) make sure output exists
    output_path = os.path.join("outputs", output_file)
    if not os.path.exists(output_path):
        app.logger.error(f"Expected output missing: {output_path}\nstdout:\n{run_stdout}\nstderr:\n{run_stderr}")
        return "Mashup failed: output file not found. See server logs.", 500

    # 4) zip the result
    try:
        with zipfile.ZipFile(zip_name, "w") as z:
            # write as just the file name inside zip
            z.write(output_path, arcname=output_file)
    except Exception as e:
        app.logger.exception("Failed to create zip")
        return f"Failed to create zip: {e}", 500

    # 5) send email only if environment variables are set (safer than hardcoding)
    email_user = os.environ.get("EMAIL_USER")   # set these as Render environment vars if you want email
    email_pass = os.environ.get("EMAIL_PASS")
    if email_user and email_pass and email:
        try:
            yag = yagmail.SMTP(email_user, email_pass)
            yag.send(
                to=email,
                subject="Your Mashup is Ready!",
                contents="Attached is your mashup file.",
                attachments=zip_name
            )
        except Exception as e:
            # don't crash the response — log and return a useful message
            app.logger.exception("Failed to send email")
            return "Mashup created but failed to send email. Check server logs for details.", 200

    # 6) success
    return "Mashup created successfully. If you provided an email and configured EMAIL_USER/EMAIL_PASS in environment, it was emailed. Otherwise download the zip from the app server.", 200


if __name__ == "__main__":
    app.run(debug=True)
