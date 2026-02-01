// ================= LOGIN =================
function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (email === "hr@company.com" && password === "admin123") {
    localStorage.setItem("loggedIn", "true");
    window.location.href = "index.html";
  } else {
    alert("Invalid credentials");
  }
}

function logout() {
  localStorage.removeItem("loggedIn");
  window.location.href = "login.html";
}

// Protect pages
if (!window.location.pathname.includes("login.html")) {
  if (!localStorage.getItem("loggedIn")) {
    window.location.href = "login.html";
  }
}

// ================= ANALYZE =================
async function analyze() {
  const jobTitle = document.getElementById("jobTitle").value;
  const skills = document.getElementById("skills").value;
  const experience = document.getElementById("experience").value;
  const jobDesc = document.getElementById("jobDesc").value;
  const files = document.getElementById("resumes").files;

  if (!files.length) {
    alert("Please upload at least one resume");
    return;
  }

  // Build JD text (matches your NLP design)
  const jd_text = `
Role: ${jobTitle}
Required skills: ${skills}
Experience: ${experience} years
${jobDesc}
`;

  const formData = new FormData();
  formData.append("jd_text", jd_text);

  for (let i = 0; i < files.length; i++) {
    formData.append("resumes", files[i]);
  }

  // Loading state
  const resultsDiv = document.getElementById("results");
  if (resultsDiv) {
    resultsDiv.innerHTML = "<p>Analyzing candidates...</p>";
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    const data = await response.json();
    renderResults(data);

    // Save results for other pages (analytics, candidates)
    localStorage.setItem("analysisResults", JSON.stringify(data));

  } catch (error) {
    console.error(error);
    alert("Failed to analyze candidates");
  }
}

// ================= RENDER RESULTS =================
function renderResults(results) {
  const resultsDiv = document.getElementById("results");
  if (!resultsDiv) return;

  resultsDiv.innerHTML = "";

  results.forEach(c => {
    let badgeClass =
      c.final_score >= 0.7 ? "strong" :
      c.final_score >= 0.4 ? "moderate" : "weak";

    resultsDiv.innerHTML += `
      <div class="candidate">
        <h3>${c.candidate_name}</h3>

        <div class="score">${(c.final_score * 100).toFixed(1)}%</div>
        <div class="progress">
          <div class="progress-bar" style="width:${c.final_score * 100}%"></div>
        </div>

        <span class="badge ${badgeClass}">${c.remarks}</span>

        <p class="small"><b>Similarity:</b> ${c.similarity_score.toFixed(2)}</p>
        <p class="small"><b>Skill Score:</b> ${c.skill_score.toFixed(2)}</p>
        <p class="small"><b>Experience Score:</b> ${c.experience_score.toFixed(2)}</p>

        <p class="small"><b>Matched:</b> ${c.matched_keywords.join(", ")}</p>
        <p class="small"><b>Missing:</b> ${c.missing_keywords.join(", ")}</p>
      </div>
    `;
  });
}

// ================= CANDIDATES PAGE =================
const candidateList = document.getElementById("candidateList");
if (candidateList) {
  const stored = localStorage.getItem("analysisResults");
  if (stored) {
    const results = JSON.parse(stored);
    renderResults(results);
  } else {
    candidateList.innerHTML = "<p>No analysis data found.</p>";
  }
}

// ================= ANALYTICS PAGE =================
if (document.getElementById("scoreChart")) {
  const stored = localStorage.getItem("analysisResults");
  if (stored) {
    const results = JSON.parse(stored);

    const names = results.map(r => r.candidate_name);
    const scores = results.map(r => Math.round(r.final_score * 100));

    new Chart(scoreChart, {
      type: "bar",
      data: {
        labels: names,
        datasets: [{
          label: "Final Score",
          data: scores,
          backgroundColor: "#00f2fe"
        }]
      }
    });
  }
}
