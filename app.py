import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request
from datetime import datetime
import threading, time

app = Flask(__name__)

# ---------- Email Configuration ----------
SENDER_EMAIL = "mounikajagarapu17@gmail.com"
SENDER_PASSWORD = "hwnnpiwrzdpqncnm"  

# ---------- Function to Send Email ----------
def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f" Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# ---------- Reminder Thread ----------
def reminder_thread(message, remind_time, user_email):
    while True:
        if datetime.now() >= remind_time:
            send_email(user_email, "Reminder Alert", message)
            break
        time.sleep(10)

# ---------- Flask Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    message = request.form['message']
    remind_time = datetime.fromisoformat(request.form['datetime'])
    user_email = request.form['email']

    threading.Thread(target=reminder_thread, args=(message, remind_time, user_email)).start()

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)