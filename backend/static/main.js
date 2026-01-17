// ===== STATE =====
let selectedExercise = "";
let videoFile = null;

// ===== ELEMENTS =====
const exerciseSelect = document.getElementById("exerciseSelect");
const uploadBtn = document.getElementById("uploadBtn");
const videoInput = document.getElementById("videoInput");
const videoContainer = document.getElementById("videoContainer");
const analyzeBtn = document.getElementById("analyzeBtn");
const output = document.getElementById("output");

// ===== EVENTS =====

// Dropdown change
exerciseSelect.addEventListener("change", (e) => {
  selectedExercise = e.target.value;
});

// Upload button click
uploadBtn.addEventListener("click", () => {
  videoInput.click();
});

// File selected
videoInput.addEventListener("change", (e) => {
  videoFile = e.target.files[0];

  if (videoFile) {
    const videoUrl = URL.createObjectURL(videoFile);
    videoContainer.innerHTML = `
      <video src="${videoUrl}" controls></video>
    `;
  }
});

// Analyze button
analyzeBtn.addEventListener("click", async () => {
  if (!videoFile || !selectedExercise) {
    alert("Please select an exercise and upload a video first");
    return;
  }

  const formData = new FormData();
  formData.append("file", videoFile);
  formData.append("exercise", selectedExercise);

  try {
    const res = await fetch("/api/analyze-video", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    output.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    output.textContent = "Error contacting backend";
    console.error(err);
  }
});
