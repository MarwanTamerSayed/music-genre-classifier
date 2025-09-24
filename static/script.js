const fileInput = document.getElementById("fileInput");
const audioWrapper = document.getElementById("audioWrapper");
const audioPlayer = document.getElementById("audioPlayer");
const loader = document.getElementById("loader");
const resultDiv = document.getElementById("result");

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    audioPlayer.src = URL.createObjectURL(file);
    audioWrapper.classList.remove("hidden");  // keep visible
  } else {
    audioWrapper.classList.add("hidden");
  }
});

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) return;

  const formData = new FormData();
  formData.append("file", file);

  // Show loader, hide result (keep audio visible)
  loader.classList.remove("hidden");
  resultDiv.classList.add("hidden");

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    // Hide loader and show result
    loader.classList.add("hidden");
    resultDiv.classList.remove("hidden");
    resultDiv.innerHTML = `🎧 Predicted Genre: <span style="color:#ffd369">${data.genre}</span>`;
  } catch (err) {
    console.error(err);
    loader.classList.add("hidden");
    alert("Error during prediction!");
  }
});
