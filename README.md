# 📈 Real-Time Data Quality Monitoring Dashboard 🛡️

A **Streamlit** and **Watchdog** based project that monitors a folder for incoming CSV files, checks for **data quality issues** like missing columns, duplicates, missing values, and sends **automatic email alerts** if problems are found.

## 🚀 Features

- Real-time monitoring of a `watch_folder/`
- Detects:
  - Missing expected columns
  - Duplicate entries
  - Missing values
  - Invalid formats
- Logs issues to Streamlit dashboard
- Sends email alerts automatically for detected issues

## 🛠️ Setup Instructions

### Install Requirements

```bash
pip install pandas streamlit watchdog
```

### Set Up Email

Update your email, password, and receiver in `app/main.py`:

```python
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
TO_EMAIL = "receiver_email@example.com"
```

*(Use App Passwords for Gmail, Outlook, etc.)*

## 🎯 How to Run

```bash
streamlit run app/main.py
```

Then drop new CSV files into the `watch_folder/` and monitor the dashboard live.

## 📁 Project Structure

- `app/main.py` – Main Streamlit + Watchdog app
- `watch_folder/` – Folder being watched for new files
- `README.md` – Project documentation

---

⚡ Built with Pandas, Streamlit, Watchdog, and a bit of Email Magic ✉️
