// ================= LOGIN =================
f/************************************************
 * AUTH (LOGIN / LOGOUT)
 ************************************************/
function login() {
  const email = document.getElementById("email")?.value;
  const password = document.getElementById("password")?.value;

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

// Protect all pages except login
if (!window.location.pathname.includes("login.html")) {
  if (!localStorage.getItem("loggedIn")) {
    window.location.href = "login.html";
  }
}

/************************************************
 * ANALYZE CANDIDATES (DASHBOARD)
 ************************************************/
async function analyze() {
  const jobTitle = document.getElementById("jobTitle")?.value;
  const skills = document.getElementById("skills")?.value;
  const experience = document.getElementById("experience")?.value;
  const jobDesc = document.getElementById("jobDesc")?.value;
  const fileInput = document.getElementById("resumes");
  const files = fileInput?.files;

  if (!files || files.length === 0) {
    alert("Please upload at least one resume");
    return;
  }

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

    // Save once, overwrite old results (correct behavior)
    localStorage.setItem("analysisResults", JSON.stringify(data));

    if (resultsDiv) {
      renderResults(data, resultsDiv);
    }

    alert("Analysis completed successfully!");

  } catch (error) {
    console.error(error);
    alert("Failed to analyze candidates. Is backend running?");
  }
}

/************************************************
 * RENDER RESULTS (REUSABLE)
 ************************************************/
function renderResults(results, container) {
  container.innerHTML = "";

  results.forEach(c => {
    const finalScore = c.final_score ?? 0;

    let badgeClass =
      finalScore >= 0.7 ? "strong" :
      finalScore >= 0.4 ? "moderate" : "weak";

    container.innerHTML += `
      <div class="candidate">
        <h3>${c.candidate_name}</h3>

        <div class="score">${(finalScore * 100).toFixed(1)}%</div>

        <div class="progress">
          <div class="progress-bar" style="width:${finalScore * 100}%"></div>
        </div>

        <span class="badge ${badgeClass}">
          ${c.remarks ?? "Evaluation complete"}
        </span>

        <p class="small"><b>Similarity:</b> ${(c.similarity_score ?? 0).toFixed(2)}</p>
        <p class="small"><b>Skill Score:</b> ${(c.skill_score ?? 0).toFixed(2)}</p>
        <p class="small"><b>Experience Score:</b> ${(c.experience_score ?? 0).toFixed(2)}</p>

        <p class="small"><b>Matched:</b> ${(c.matched_keywords ?? []).join(", ")}</p>
        <p class="small"><b>Missing:</b> ${(c.missing_keywords ?? []).join(", ")}</p>
      </div>
    `;
  });
}

/************************************************
 * CANDIDATES PAGE
 ************************************************/
document.addEventListener("DOMContentLoaded", () => {
  const candidateList = document.getElementById("candidateList");

  if (candidateList) {
    const stored = localStorage.getItem("analysisResults");

    if (!stored) {
      candidateList.innerHTML =
        "<p>No analysis data found. Please analyze candidates first.</p>";
      return;
    }

    const results = JSON.parse(stored);
    renderResults(results, candidateList);
  }
});

/************************************************
 * ANALYTICS PAGE
 ************************************************/
document.addEventListener("DOMContentLoaded", () => {
  const scoreChart = document.getElementById("scoreChart");

  if (scoreChart) {
    const stored = localStorage.getItem("analysisResults");
    if (!stored) return;

    const results = JSON.parse(stored);

    const names = results.map(r => r.candidate_name);
    const scores = results.map(r => Math.round((r.final_score ?? 0) * 100));

    new Chart(scoreChart, {
      type: "bar",
      data: {
        labels: names,
        datasets: [{
          label: "Final Score (%)",
          data: scores,
          backgroundColor: "#00f2fe"
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, max: 100 }
        }
      }
    });
  }
});
