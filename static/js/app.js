const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");
const preview = document.getElementById("preview");
const loading = document.getElementById("loading");
const resultsBox = document.getElementById("results");
const resultsTable = document.querySelector("#resultsTable tbody");
const errorBox = document.getElementById("errorBox");
const copyBtn = document.getElementById("copyBtn");

let selectedFile = null;
let lastResult = null;

dropZone.addEventListener("click", () => fileInput.click());

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length) {
    handleFile(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length) {
    handleFile(fileInput.files[0]);
  }
});

function handleFile(file) {
  selectedFile = file;
  uploadBtn.disabled = false;
  preview.innerHTML = "";
  errorBox.classList.add("hidden");

  if (file.type.startsWith("image/")) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    preview.appendChild(img);
  } else {
    preview.innerHTML = `<p>Selected file: ${file.name}</p>`;
  }
}

uploadBtn.addEventListener("click", async () => {
  if (!selectedFile) return;

  resultsBox.classList.add("hidden");
  errorBox.classList.add("hidden");
  loading.classList.remove("hidden");
  uploadBtn.disabled = true;

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/extract", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Extraction failed.");
    }

    const data = await response.json();
    lastResult = data;
    renderResults(data);
  } catch (err) {
    errorBox.textContent = err.message;
    errorBox.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
    uploadBtn.disabled = false;
  }
});

function renderResults(data) {
  resultsTable.innerHTML = "";
  const fieldLabels = {
    candidate_name: "Candidate Name",
    certificate_title: "Certificate Title",
    organization_name: "Organization",
    issue_date: "Issue Date",
    certificate_number: "Certificate Number",
    grade_score: "Grade / Score",
  };

  for (const [key, label] of Object.entries(fieldLabels)) {
    const row = document.createElement("tr");
    row.innerHTML = `<td class="field-name">${label}</td><td>${data[key] || "—"}</td>`;
    resultsTable.appendChild(row);
  }

  resultsBox.classList.remove("hidden");
}

copyBtn.addEventListener("click", () => {
  if (!lastResult) return;
  navigator.clipboard.writeText(JSON.stringify(lastResult, null, 2));
  copyBtn.textContent = "Copied!";
  setTimeout(() => (copyBtn.textContent = "Copy JSON to clipboard"), 1500);
});
