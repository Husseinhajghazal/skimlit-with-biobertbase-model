document.addEventListener("DOMContentLoaded", () => {
  const summaryDiv = document.getElementById("summary");
  const statusP = document.getElementById("status");
  const spinner = document.getElementById("spinner");

  chrome.storage.local.get(["selectedText"], (result) => {
    if (result.selectedText) {
      statusP.style.display = "none";
      spinner.style.display = "block";
      summarizeText(result.selectedText)
        .then((summary) => {
          spinner.style.display = "none";
          summaryDiv.style.display = "block";
          if (summary === "No objective or results found in the text.") {
            summaryDiv.textContent = summary;
            statusP.style.display = "block";
            statusP.textContent = "Summary unavailable";
          } else {
            typeWriter(summary, summaryDiv);
          }
          chrome.storage.local.remove("selectedText");
        })
        .catch((error) => {
          spinner.style.display = "none";
          statusP.style.display = "block";
          statusP.textContent = "Failed to summarize.";
          summaryDiv.textContent = "Error: " + error.message;
          summaryDiv.style.display = "block";
          chrome.storage.local.remove("selectedText");
        });
    } else {
      statusP.textContent = "No text selected.";
    }
  });
});

async function summarizeText(text) {
  const apiUrl = "http://localhost:8000/summarize";
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
      signal: AbortSignal.timeout(30000),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.summary;
  } catch (error) {
    throw new Error("Failed to fetch summary: " + error.message);
  }
}

function typeWriter(text, element) {
  element.textContent = "";
  element.classList.add("typing");
  let i = 0;
  const speed = 30;
  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    } else {
      element.classList.remove("typing");
    }
  }
  type();
}
