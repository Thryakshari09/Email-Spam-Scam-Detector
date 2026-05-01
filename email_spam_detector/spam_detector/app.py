"""
Email Spam & Scam Detector — Flask backend
Run: python app.py  -> http://127.0.0.1:5000
"""
from flask import Flask, render_template, request
import re
from model import predict_email, SUSPICIOUS_WORDS

app = Flask(__name__)

# Very small list of "known/legit" domains. Anything else is treated as
# slightly less trustworthy by the rule-based layer.
KNOWN_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
    "icloud.com", "protonmail.com", "company.com", "live.com",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def analyze_sender(sender: str):
    """Return a list of reasons why a sender looks suspicious."""
    reasons = []
    if not sender:
        return reasons

    sender = sender.strip().lower()
    if not EMAIL_RE.match(sender):
        reasons.append("Sender address is not a valid email format.")
        return reasons

    local, domain = sender.split("@", 1)

    # Random-looking local part: many digits or very long
    digits = sum(c.isdigit() for c in local)
    if len(local) >= 12 and digits / max(len(local), 1) > 0.4:
        reasons.append("Sender username looks random (many digits).")

    # Suspicious / free TLDs often abused by scammers
    bad_tlds = (".tk", ".ml", ".ga", ".cf", ".gq", ".win", ".click", ".zip")
    if domain.endswith(bad_tlds):
        reasons.append(f"Sender domain uses a suspicious TLD ({domain}).")

    if domain not in KNOWN_DOMAINS and "-" in domain and domain.count("-") >= 2:
        reasons.append("Sender domain contains many hyphens.")

    return reasons


def rule_based_check(content: str, sender: str):
    """Return (verdict, reasons). verdict in {'safe','suspicious','spam', None}.
    None means 'not decided — fall through to ML'."""
    reasons = []
    text = content.lower()

    hits = [w for w in SUSPICIOUS_WORDS if w in text]
    if hits:
        reasons.append("Contains suspicious phrases: " + ", ".join(hits))

    sender_reasons = analyze_sender(sender)
    reasons.extend(sender_reasons)

    # Strong spam signal: 3+ suspicious words OR suspicious words + bad sender
    if len(hits) >= 3 or (hits and sender_reasons):
        return "spam", reasons
    if hits or sender_reasons:
        return "suspicious", reasons
    return None, reasons


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        content = (request.form.get("content") or "").strip()
        sender = (request.form.get("sender") or "").strip()

        if not content:
            result = {
                "verdict": "error",
                "label": "Please enter the email content to analyze.",
                "reasons": [],
                "source": "validation",
            }
        else:
            verdict, reasons = rule_based_check(content, sender)
            if verdict is None:
                # Fall through to ML
                ml_label, confidence = predict_email(content)
                verdict = "spam" if ml_label == "spam" else "safe"
                reasons.append(
                    f"ML model classified this email as {ml_label.upper()} "
                    f"({confidence*100:.1f}% confidence)."
                )
                source = "ml"
            else:
                source = "rules"

            label_map = {
                "safe": "Safe Email",
                "suspicious": "Suspicious Email",
                "spam": "Spam / Scam Email",
            }
            result = {
                "verdict": verdict,
                "label": label_map[verdict],
                "reasons": reasons or ["No specific red flags found."],
                "source": source,
                "content": content,
                "sender": sender,
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
