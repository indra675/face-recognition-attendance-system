// Shared webcam helper. Starts the camera into #video as soon as the page loads.
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: false });
    video.srcObject = stream;
  } catch (err) {
    alert("Could not access the webcam. Please allow camera permission and reload the page.");
    console.error(err);
  }
}

// Captures the current video frame and returns a base64 data URL (image/jpeg).
function captureFrame() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/jpeg", 0.9);
}

startCamera();
