const form = document.querySelector("#question-form");
const questionInput = document.querySelector("#question");
const submitButton = document.querySelector("#submit-button");
const characterCount = document.querySelector("#character-count");
const errorMessage = document.querySelector("#error-message");
const result = document.querySelector("#result");
const resultQuestion = document.querySelector("#result-question");

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
  result.hidden = true;
}

function showResult(question) {
  resultQuestion.textContent = question;
  result.hidden = false;
  errorMessage.hidden = true;
}

function setSubmitting(isSubmitting) {
  submitButton.disabled = isSubmitting;
  const buttonLabel = submitButton.querySelector(".button-label");
  buttonLabel.textContent = isSubmitting ? "会議をひらいています…" : "会議をはじめる";
}

function getApiErrorMessage(data) {
  if (typeof data.detail === "string") {
    return data.detail;
  }
  return "質問を入力してください。";
}

async function submitQuestion(question) {
  const response = await fetch("/api/questions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(getApiErrorMessage(data));
  }
  return data;
}

questionInput.addEventListener("input", () => {
  characterCount.textContent = `${questionInput.value.length} / 2000`;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();

  if (!question) {
    showError("質問を入力してください。");
    questionInput.focus();
    return;
  }

  setSubmitting(true);
  try {
    const data = await submitQuestion(question);
    showResult(data.question);
  } catch (error) {
    showError(error instanceof Error ? error.message : "通信に失敗しました。");
  } finally {
    setSubmitting(false);
  }
});
