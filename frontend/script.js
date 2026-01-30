const candidates = [
    { name: "Deepesh", score: 78, skill: 85, exp: 60 },
    { name: "Candidate B", score: 52, skill: 50, exp: 45 },
    { name: "Candidate C", score: 35, skill: 30, exp: 25 }
  ];
  
  // Populate Candidates page
  const list = document.getElementById("candidateList");
  if (list) {
    candidates.forEach(c => {
      list.innerHTML += `
        <div class="card">
          <h3>${c.name}</h3>
          <p>Final Score: ${c.score}%</p>
          <p>Skill Match: ${c.skill}%</p>
          <p>Experience: ${c.exp}%</p>
        </div>
      `;
    });
  }
  
  // Charts
  if (document.getElementById("scoreChart")) {
    new Chart(scoreChart, {
      type: 'bar',
      data: {
        labels: candidates.map(c => c.name),
        datasets: [{
          label: "Final Score",
          data: candidates.map(c => c.score),
          backgroundColor: "#00f2fe"
        }]
      }
    });
  
    new Chart(skillChart, {
      type: 'pie',
      data: {
        labels: candidates.map(c => c.name),
        datasets: [{
          data: candidates.map(c => c.skill),
          backgroundColor: ["#2ecc71","#f1c40f","#e74c3c"]
        }]
      }
    });
  }
  
  function analyze() {
    alert("Connected to backend next 🔥");
  }
  function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    // Demo credentials
    if (email === "hr@company.com" && password === "admin123") {
      localStorage.setItem("loggedIn", "true");
      window.location.href = "index.html";
    } else {
      alert("Invalid credentials");
    }
  }
  
  // Protect pages (run on every page)
  if (!window.location.pathname.includes("login.html")) {
    const loggedIn = localStorage.getItem("loggedIn");
    if (!loggedIn) {
      window.location.href = "login.html";
    }
  }
  
  function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "login.html";
  }
  