const empIdInput = document.getElementById("empId");
const empNameInput = document.getElementById("empName");
const captureBtn = document.getElementById("captureBtn");
const resetBtn = document.getElementById("resetBtn");
const submitBtn = document.getElementById("submitBtn");
const frameCountEl = document.getElementById("frameCount");
const thumbRow = document.getElementById("thumbRow");
const statusMsg = document.getElementById("statusMsg");

let frames = [];

function setStatus(text, type) {
  statusMsg.textContent = text || "";
  statusMsg.className = "status-msg" + (type ? " " + type : "");
}

function refreshUi() {
  frameCountEl.textContent = frames.length;
  submitBtn.disabled = frames.length < 3;
}

captureBtn.addEventListener("click", () => {
  const dataUrl = captureFrame();
  frames.push(dataUrl);

  const img = document.createElement("img");
  img.src = dataUrl;
  thumbRow.appendChild(img);

  refreshUi();
});

resetBtn.addEventListener("click", () => {
  frames = [];
  thumbRow.innerHTML = "";
  setStatus("");
  refreshUi();
});

submitBtn.addEventListener("click", async () => {
  const emp_id = empIdInput.value.trim();
  const name = empNameInput.value.trim();

  if (!emp_id || !name) {
    setStatus("Please enter an employee ID and name.", "err");
    return;
  }
  if (frames.length < 3) {
    setStatus("Please capture at least 3 photos.", "err");
    return;
  }

  submitBtn.disabled = true;
  setStatus("Enrolling…");

  try {
    const res = await fetch("/api/enroll", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emp_id, name, frames }),
    });
    const data = await res.json();

    if (data.ok) {
      setStatus(`Enrolled ${name} using ${data.captured} photo(s).`, "ok");
      frames = [];
      thumbRow.innerHTML = "";
      empIdInput.value = "";
      empNameInput.value = "";
      refreshUi();
    } else {
      setStatus(data.error || "Enrollment failed.", "err");
      submitBtn.disabled = frames.length < 3;
    }
  } catch (err) {
    console.error(err);
    setStatus("Could not reach the server.", "err");
    submitBtn.disabled = frames.length < 3;
  }
});

refreshUi();
