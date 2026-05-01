# Email-Spam-Scam-Detector
A simple college-level cybersecurity web app that classifies an email as Safe, Suspicious, or Spam/Scam using:

Rule-based detection — flags suspicious keywords (e.g. "urgent", "lottery", "verify"), and inspects the sender address.
Machine learning — CountVectorizer + MultinomialNB (scikit-learn) trained on a small built-in dataset of spam vs. safe emails.
Project structure
app.py                 # Flask backend (routes, rule-based layer)
model.py               # ML model (CountVectorizer + Naive Bayes)
templates/index.html   # Frontend
static/style.css       # Soft beige styling
requirements.txt
Setup & run
# 1. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate           # on Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
Then open: http://127.0.0.1:5000

How it works
The form posts the email content (and optional sender) to /.
rule_based_check() looks for suspicious phrases and bad sender patterns.
If rules don't trigger, predict_email() runs the Naive Bayes model.
The verdict is rendered with color coding:
🟢 Green = Safe
🟡 Orange = Suspicious
🔴 Red = Spam / Scam

url :http://127.0.0.1:5000
