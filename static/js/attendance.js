const scanBtn = document.getElementById("scanBtn");
const resultBox = document.getElementById("resultBox");

function showResult(text, type) {
  resultBox.textContent = text;
  resultBox.className = "result-box show" + (type ? " " + type : "");
}

scanBtn.addEventListener("click", async () => {
  scanBtn.disabled = true;
  showResult("Scanning…");

  const frame = captureFrame();

  try {
    const res = await fetch("/api/mark_attendance", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ frame }),
    });
    const data = await res.json();

    if (!data.ok) {
      showResult(data.error || "Something went wrong.", "err");
    } else if (!data.results || data.results.length === 0) {
      showResult("No face detected. Face the camera and try again.", "err");
    } else {
      const lines = data.results.map((r) => {
        if (r.status === "marked") return `✅ ${r.name} marked present at ${r.time}`;
        if (r.status === "already_marked") return `ℹ️ ${r.name} was already marked present today.`;
        return "⚠️ Face not recognized.";
      });
      const anyMarked = data.results.some((r) => r.status === "marked");
      const anyUnknown = data.results.some((r) => r.status === "unknown");
      showResult(lines.join("\n"), anyMarked ? "ok" : anyUnknown ? "warn" : "warn");
    }
  } catch (err) {
    console.error(err);
    showResult("Could not reach the server.", "err");
  } finally {
    scanBtn.disabled = false;
  }
});
