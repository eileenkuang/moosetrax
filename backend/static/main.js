let selectedExercise = "";
let videoFile = null;

const exerciseSelect = document.getElementById("exerciseSelect");
const videoInput = document.getElementById("videoInput");
const videoContainer = document.getElementById("videoContainer");
const output = document.getElementById("output");
const uploadBtn = document.getElementById("uploadBtn");
const dashboardBtn = document.getElementById("dashboardBtn");

// Dropdown selection
exerciseSelect.addEventListener("change", (e) => {
  selectedExercise = e.target.value;
});

// Dashboard button (placeholder)
dashboardBtn.addEventListener("click", () => {
  console.log("Dashboard clicked");
});

// Upload button click → open file picker
uploadBtn.addEventListener("click", () => {
  videoInput.click();
});

// Video selection → preview + upload to backend
videoInput.addEventListener("change", async (e) => {
  videoFile = e.target.files[0];
  if (!videoFile) return;

  // 1️⃣ Show preview in browser
  const videoUrl = URL.createObjectURL(videoFile);
  videoContainer.innerHTML = `<video src="${videoUrl}" controls></video>`;

  // 2️⃣ Send file to backend for saving
  const formData = new FormData();
  formData.append("file", videoFile);

  try {
    const res = await fetch("/api/save-video", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    output.textContent = `Video saved as: ${data.filename}`;
  } catch (err) {
    output.textContent = "Error saving video: " + err;
  }
});
