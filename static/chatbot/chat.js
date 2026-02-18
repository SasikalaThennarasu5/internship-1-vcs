document.addEventListener("DOMContentLoaded", function () {

  const toggle = document.getElementById("chatbot-toggle");
  const box = document.getElementById("chatbot-box");
  const closeBtn = document.getElementById("chatbot-close");
  const input = document.getElementById("chat-input");
  const messages = document.getElementById("chatbot-messages");

  if (!toggle || !box || !messages) return;

  function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = sender;
    div.innerHTML = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
  }

  // Greeting (ONLY ONCE)
  if (window.USER_LOGGED_IN) {
    addMessage(`👋 Hi <b>${window.USER_NAME}</b>!<br>
      Enter your skill & location<br>
      <i>Example: python, chennai</i>`, "bot");
  } else {
    addMessage(`👋 Hi! Enter your skills and preferred location.<br>
      Example: django, chennai`, "bot");
  }

  // Send message
  window.sendMessage = async function () {
    const userText = input.value.trim();
    if (!userText) return;

    addMessage(userText, "user");
    input.value = "";

    try {
      const response = await fetch("/chatbot/api/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userText })
      });

      const data = await response.json();
      addMessage(data.reply, "bot");

    } catch (err) {
      console.error(err);
      addMessage("⚠ Something went wrong. Please try again.", "bot");
    }
  };

  input.addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
  });

  toggle.onclick = () => {
    box.style.display = "flex";
    toggle.style.display = "none";
  };

  closeBtn.onclick = () => {
    box.style.display = "none";
    toggle.style.display = "flex";
  };

});
