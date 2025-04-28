import streamlit as st
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import smtplib
from email.message import EmailMessage
import os

# Email alert settings (configure your own details)
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
TO_EMAIL = "receiver_email@example.com"

# Function to send email alerts
def send_email_alert(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Email sending failed: {e}")

# Data Quality Check Function
def data_quality_check(file_path):
    issues = []
    try:
        df = pd.read_csv(file_path)
        if df.isnull().sum().sum() > 0:
            issues.append("Missing values detected.")
        if df.duplicated().any():
            issues.append("Duplicate rows detected.")
        expected_columns = ['id', 'timestamp', 'value']
        for col in expected_columns:
            if col not in df.columns:
                issues.append(f"Missing expected column: {col}")
    except Exception as e:
        issues.append(f"Invalid file format or parsing error: {str(e)}")
    return issues

# File system event handler
class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            issues = data_quality_check(event.src_path)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            if issues:
                for issue in issues:
                    st.error(f"[{timestamp}] {os.path.basename(event.src_path)}: {issue}")
                    send_email_alert("⚠️ Data Quality Issue Detected", f"{os.path.basename(event.src_path)}: {issue}")
            else:
                st.success(f"[{timestamp}] {os.path.basename(event.src_path)}: No issues found.")

# Streamlit Dashboard
st.title("🛡️ Real-Time Data Quality Monitoring Dashboard")
st.info("Monitoring 'watch_folder/' for new incoming files...")

watch_path = "watch_folder"
event_handler = WatcherHandler()
observer = Observer()
observer.schedule(event_handler, path=watch_path, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
