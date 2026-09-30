"""Flask interface for the existing Spam/Ham classifier."""
from __future__ import annotations

import pickle
from pathlib import Path
from threading import Lock
from typing import Any

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"

# The supplied notebook stores both fitted objects in spam_classifier.pkl.
BUNDLE_PATHS = (
    MODEL_DIR / "spam_classifier.pkl",
    BASE_DIR / "spam_classifier.pkl",
)
SEPARATE_MODEL_PATHS = (
    MODEL_DIR / "model.pkl",
    MODEL_DIR / "spam_model.pkl",
    BASE_DIR / "model.pkl",
    BASE_DIR / "spam_model.pkl",
)
VECTORIZER_PATHS = (
    MODEL_DIR / "vectorizer.pkl",
    MODEL_DIR / "tfidf_vectorizer.pkl",
    BASE_DIR / "vectorizer.pkl",
    BASE_DIR / "tfidf_vectorizer.pkl",
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
_artifact_lock = Lock()
_artifacts: tuple[Any, Any | None] | None = None


def _load_serialized(path: Path) -> Any:
    """Load a trusted local pickle/joblib artifact."""
    if path.suffix.lower() == ".joblib":
        import joblib

        return joblib.load(path)
    with path.open("rb") as artifact_file:
        return pickle.load(artifact_file)


def load_artifacts() -> tuple[Any, Any | None]:
    """Load the existing model and, if separate, its fitted vectorizer."""
    global _artifacts
    if _artifacts is not None:
        return _artifacts

    with _artifact_lock:
        if _artifacts is not None:
            return _artifacts

        for path in BUNDLE_PATHS:
            if path.is_file():
                bundle = _load_serialized(path)
                if isinstance(bundle, dict) and "model" in bundle:
                    _artifacts = (bundle["model"], bundle.get("vectorizer"))
                    return _artifacts
                # sklearn Pipeline objects own their preprocessing steps.
                if hasattr(bundle, "named_steps"):
                    _artifacts = (bundle, None)
                    return _artifacts

        model_path = next((path for path in SEPARATE_MODEL_PATHS if path.is_file()), None)
        vectorizer_path = next((path for path in VECTORIZER_PATHS if path.is_file()), None)
        if model_path and vectorizer_path:
            _artifacts = (_load_serialized(model_path), _load_serialized(vectorizer_path))
            return _artifacts

        if model_path and hasattr(_load_serialized(model_path), "named_steps"):
            _artifacts = (_load_serialized(model_path), None)
            return _artifacts

        raise FileNotFoundError(
            "No usable trained model was found. Expected the existing combined "
            "spam_classifier.pkl, or a model file plus its fitted vectorizer."
        )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send a valid JSON object containing an email field."), 400

    email_text = payload.get("email")
    if not isinstance(email_text, str):
        return jsonify(error="Email must be text."), 400
    if not email_text.strip():
        return jsonify(error="Please enter an email message to classify."), 400
    if len(email_text) > 10000:
        return jsonify(error="Email text must be 10,000 characters or fewer."), 400

    try:
        model, vectorizer = load_artifacts()
        # The fitted CountVectorizer from the notebook reproduces training-time
        # text preprocessing. A Pipeline handles its own transformation.
        features = vectorizer.transform([email_text]) if vectorizer is not None else [email_text]
        prediction = str(model.predict(features)[0]).strip().lower()
        if prediction not in {"spam", "ham"}:
            app.logger.error("Unsupported classifier label: %r", prediction)
            return jsonify(error="The model returned an unsupported class."), 500

        confidence = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(features)[0]
            classes = [str(label).strip().lower() for label in model.classes_]
            if prediction in classes:
                confidence = float(probabilities[classes.index(prediction)])

        return jsonify(prediction=prediction, confidence=confidence)
    except FileNotFoundError as exc:
        app.logger.warning("Model artifact unavailable: %s", exc)
        return jsonify(error="The trained model or vectorizer file is missing."), 503
    except Exception:
        app.logger.exception("Email classification failed")
        return jsonify(error="The model could not classify this email. Please try again."), 500


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(error="The request is too large. Please shorten the email text."), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
