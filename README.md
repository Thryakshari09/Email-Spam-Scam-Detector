# Email-Spam-Scam-Detector
A simple college-level cybersecurity web app that classifies an email as Safe, Suspicious, or Spam/Scam using:

1. User Input (Frontend)
The user enters:
📩 Email content
📧 Sender address (optional)
Clicks Submit
This data is sent to the backend (app.py) using a form
2. Rule-Based Detection (First Check)
   The system first runs a function like rule_based_check()
It looks for:
   🚨 Suspicious words like:
   “urgent”
   “lottery”
   “verify”
   “win money”
⚠️ Suspicious sender patterns:
   Random emails (e.g. abc123@xyz.ru)
   Unknown or fake domains

👉 If something suspicious is found:

It immediately classifies:
   Suspicious OR Spam/Scam
   No need for ML in this case
3. Machine Learning Check (If rules don’t trigger)
   If the email looks normal, then ML is used
How ML works:
   The email text is converted into numbers using:
   CountVectorizer
Then classified using:
   Multinomial Naive Bayes

👉 The model was trained earlier on:

Spam emails
Safe emails

👉 It predicts:

Safe
Spam
4. Final Decision
   Combine results:
   Rule-based result (if triggered)
   OR ML prediction
5. Output Display (Frontend)
   The result is shown with color:
   Result	Color	Meaning
     🟢 Safe	Green	Normal email
     🟡 Suspicious	Orange	Be careful
     🔴 Spam/Scam	Red	Dangerous
🧠 Simple Flow (Easy to remember)
User Input
   ↓
Rule-Based Check
   ↓ (if suspicious found)
Show Result
   ↓ (if no issue)
ML Model Prediction
   ↓
Show Final Result
url :http://127.0.0.1:5000
