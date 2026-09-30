const form = document.querySelector("#email-form");
const emailField = document.querySelector("#email-text");
const characterCount = document.querySelector("#character-count");
const clearButton = document.querySelector("#clear-button");
const checkButton = document.querySelector("#check-button");
const loadingMessage = document.querySelector("#loading-message");
const errorMessage = document.querySelector("#error-message");
const resultSection = document.querySelector("#result-section");

emailField.addEventListener("input", () => {
  characterCount.textContent = `${emailField.value.length.toLocaleString()} / 10,000 characters`;
});

clearButton.addEventListener("click", () => {
  emailField.value = "";
  emailField.dispatchEvent(new Event("input"));
  errorMessage.hidden = true;
  emailField.focus();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.hidden = true;
  resultSection.hidden = true;
  const email = emailField.value.trim();

  if (!email) {
    showError("Please enter an email message before checking.");
    emailField.focus();
    return;
  }

  setLoading(true);
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email })
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("The server returned an invalid response.");
    }

    if (!response.ok) {
      throw new Error(data.error || "The prediction request failed. Please try again.");
    }

    const prediction = String(data.prediction || "").trim().toLowerCase();
    const confidence = data.confidence == null ? null : Number(data.confidence);
    if (!["spam", "ham"].includes(prediction) ||
        (confidence !== null && (!Number.isFinite(confidence) || confidence < 0 || confidence > 1))) {
      throw new Error("The server response did not contain a valid prediction.");
    }
    showResult(prediction, confidence, email);
  } catch (error) {
    showError(error instanceof TypeError
      ? "Could not reach the Flask server. Make sure it is running and try again."
      : (error.message || "An unexpected prediction error occurred."));
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  checkButton.disabled = isLoading;
  clearButton.disabled = isLoading;
  emailField.disabled = isLoading;
  loadingMessage.hidden = !isLoading;
  checkButton.querySelector("span").textContent = isLoading ? "Analyzing..." : "Check Email";
  checkButton.querySelector("b").textContent = isLoading ? "" : "→";
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function showResult(prediction, confidence, email) {
  const isSpam = prediction === "spam";
  const percentage = confidence === null ? null : Math.round(confidence * 100);
  const card = document.querySelector("#result-card");
  card.className = `result-card ${isSpam ? "spam" : "ham"}`;
  document.querySelector("#result-icon").textContent = isSpam ? "!" : "✓";
  document.querySelector("#result-title").textContent = isSpam ? "⚠️ SPAM EMAIL" : "✓ HAM EMAIL";
  document.querySelector("#result-description").textContent = isSpam
    ? "This email has been classified as Spam."
    : "This email has been classified as a legitimate email.";
  document.querySelector("#result-status").textContent = isSpam ? "SUSPICIOUS" : "LEGITIMATE";
  document.querySelector("#confidence-value").textContent = percentage === null ? "Not available" : `${percentage}%`;
  document.querySelector("#confidence-bar").style.width = `${percentage ?? 0}%`;
  const progress = document.querySelector(".progress-track");
  progress.setAttribute("aria-valuenow", String(percentage ?? 0));
  document.querySelector("#analyzed-email").textContent = email;
  document.querySelector("#summary-prediction").textContent = isSpam ? "Spam" : "Ham";
  document.querySelector("#summary-confidence").textContent = percentage === null ? "Not available" : `${percentage}%`;
  const summaryStatus = document.querySelector("#summary-status");
  summaryStatus.textContent = isSpam ? "Suspicious" : "Legitimate";
  summaryStatus.className = isSpam ? "spam-text" : "ham-text";
  resultSection.hidden = false;
  resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

document.querySelector("#another-button").addEventListener("click", () => {
  resultSection.hidden = true;
  errorMessage.hidden = true;
  emailField.value = "";
  emailField.dispatchEvent(new Event("input"));
  emailField.focus();
  document.querySelector("#checker").scrollIntoView({ behavior: "smooth", block: "start" });
});
