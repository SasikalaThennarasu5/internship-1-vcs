// ================= JOB FILTER (GLOBAL) =================
window.filterJobs = function (skill, location) {
  const jobs = document.querySelectorAll(".job-card");
  let found = 0;

  console.log("Filtering jobs:", skill, location);
  console.log("Jobs found:", jobs.length);

  jobs.forEach(job => {
    const jobSkill = job.dataset.skill || "";
    const jobLocation = job.dataset.location || "";

    if (
      jobSkill.includes(skill.toLowerCase()) &&
      jobLocation.includes(location.toLowerCase())
    ) {
      job.closest(".col-md-6").style.display = "block";
      found++;
    } else {
      job.closest(".col-md-6").style.display = "none";
    }
  });

  return found;
};

document.addEventListener("DOMContentLoaded", function () {

  const toggle = document.getElementById("chatbot-toggle");
  const box = document.getElementById("chatbot-box");
  const closeBtn = document.getElementById("chatbot-close");
  const input = document.getElementById("chat-input");
  const messages = document.getElementById("chatbot-messages");

  if (!toggle || !box || !messages) {
    console.error("Chatbot elements not found");
    return;
  }

  /* ---------- OPEN / CLOSE ---------- */

  toggle.onclick = () => {
    box.style.display = "flex";
    toggle.style.display = "none";
  };

  closeBtn.onclick = () => {
    box.style.display = "none";
    toggle.style.display = "flex";
  };

  // 👋 GREETING
  if (window.USER_LOGGED_IN) {
    addMessage(
      `👋 Hi <b>${window.USER_NAME}</b>!<br>
       Tell me your skill & location<br>
       <i>Example: python, chennai</i>`,
      "bot"
    );
  } else {
    addMessage(
      `👋 Hi! Please <b>login</b> for better matches.<br>
       Try: <i>python, bangalore</i>`,
      "bot"
    );
  }

  toggle.onclick = () => {
    box.style.display = "flex";
    toggle.style.display = "none";
  };

  closeBtn.onclick = () => {
    box.style.display = "none";
    toggle.style.display = "flex";
  };

  window.sendMessage = function () {
    const userText = input.value.trim();
    if (!userText) return;

    addMessage(userText, "user");
    input.value = "";

    setTimeout(() => {
      addMessage(botReply(userText), "bot");
    }, 400);
  };


  /* ---------- MESSAGE FUNCTIONS ---------- */

  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = sender;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  window.sendMessage = function () {
    const userText = input.value.trim();
    if (!userText) return;

    addMessage(userText, "user");
    input.value = "";

    setTimeout(() => {
      const reply = botReply(userText);
      addMessage(reply, "bot");
    }, 500);
  };

  /* ---------- BOT LOGIC ---------- */

  function botReply(text) {
  text = text.toLowerCase().trim();

  const match = text.match(/^([a-z\s]+),\s*([a-z\s]+)$/i);

  if (match) {
    const skill = match[1].trim();
    const location = match[2].trim();

    // 🔥 THIS WAS MISSING
    const found = filterJobs(skill, location);

    if (found > 0) {
      return `🔍 <b>Job Search Started</b><br>
              Skill: <b>${skill}</b><br>
              Location: <b>${location}</b><br><br>
              👉 <b>${found}</b> matching jobs found<br>
              👉 Scroll down to view them`;
    } else {
      return `😕 <b>No jobs found</b><br>
              Try a different skill or location<br>
              <i>Example: python, bangalore</i>`;
    }
  }

  return `🤖 I can help you find jobs.<br>
          Try: <b>python, chennai</b>`;
}

});







