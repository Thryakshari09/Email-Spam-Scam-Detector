"""
ML model: CountVectorizer + Multinomial Naive Bayes
Trained once at import time on a small built-in dataset.
"""
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Words/phrases the rule-based layer flags as suspicious
SUSPICIOUS_WORDS = [
    "urgent", "win money", "free", "click now", "verify",
    "lottery", "congratulations", "prize", "claim now",
    "act now", "limited time", "bank account", "password",
    "wire transfer", "bitcoin", "gift card",
]

# Tiny built-in training dataset (label: 'spam' or 'safe')
TRAIN_DATA = [
    # --- Spam ---
    ("Congratulations! You have won a free lottery prize. Click now to claim.", "spam"),
    ("URGENT: Verify your bank account immediately or it will be closed.", "spam"),
    ("You have won money in our exclusive lottery, act now!", "spam"),
    ("Free gift card waiting for you. Click the link to claim now.", "spam"),
    ("Limited time offer: send bitcoin to double your money.", "spam"),
    ("Your password has expired. Verify your account here urgently.", "spam"),
    ("Claim your prize now before it expires. This is urgent!", "spam"),
    ("Wire transfer required to release your inheritance funds.", "spam"),
    ("You are the lucky winner of our promotion. Click now to receive.", "spam"),
    ("Get rich quick with this amazing free investment opportunity.", "spam"),
    # --- Safe ---
    ("Hi team, please find attached the meeting notes from today.", "safe"),
    ("Reminder: your dentist appointment is tomorrow at 10 AM.", "safe"),
    ("The quarterly report is ready for your review. Let me know your thoughts.", "safe"),
    ("Thanks for your email. I'll get back to you by Friday.", "safe"),
    ("Please review the project proposal and share your feedback.", "safe"),
    ("Lunch at 1pm? Let me know if that works for you.", "safe"),
    ("Your order has been shipped and will arrive on Monday.", "safe"),
    ("Welcome to the course! Here is the syllabus for this semester.", "safe"),
    ("The server maintenance is scheduled for Saturday night.", "safe"),
    ("Happy birthday! Hope you have a wonderful day with family.", "safe"),
]

texts = [t for t, _ in TRAIN_DATA]
labels = [l for _, l in TRAIN_DATA]

# Build pipeline manually so we can re-use the vectorizer
_vectorizer = CountVectorizer(lowercase=True, stop_words="english")
_X = _vectorizer.fit_transform(texts)
_clf = MultinomialNB()
_clf.fit(_X, labels)


def predict_email(text: str):
    """Return (label, confidence) where label is 'spam' or 'safe'."""
    X = _vectorizer.transform([text])
    proba = _clf.predict_proba(X)[0]
    classes = list(_clf.classes_)
    idx = proba.argmax()
    return classes[idx], float(proba[idx])
