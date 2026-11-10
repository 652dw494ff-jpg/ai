const body = document.body;
const chatArea = document.getElementById("chatArea");
const welcome = document.getElementById("welcome");
const input = document.getElementById("messageInput");
const form = document.getElementById("chatForm");
const statusText = document.getElementById("statusText");
const engineLabel = document.getElementById("engineLabel");

function setTheme(theme) {
  body.dataset.theme = theme;
  document.querySelectorAll("[data-theme-choice]").forEach(b =>
    b.classList.toggle("selected", b.dataset.themeChoice === theme));
  try { localStorage.setItem("aura-theme", theme); } catch {}
}
try { setTheme(localStorage.getItem("aura-theme") || "dark"); } catch { setTheme("dark"); }
document.querySelectorAll("[data-theme-choice]").forEach(b => b.addEventListener("click", () => setTheme(b.dataset.themeChoice)));
document.getElementById("themeToggle").addEventListener("click", () => setTheme(body.dataset.theme === "dark" ? "light" : "dark"));

function addMessage(text, who) {
  welcome.style.display = "none";
  const row = document.createElement("div");
  row.className = "message " + who;
  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = who === "user" ? "TY" : "A";
  const content = document.createElement("div");
  content.className = "message-content";
  content.textContent = text;
  row.append(avatar, content);
  chatArea.appendChild(row);
  chatArea.scrollTop = chatArea.scrollHeight;
  return content;
}

async function sendMessage(text) {
  const clean = text.trim();
  if (!clean) return;
  addMessage(clean, "user");
  input.value = "";
  const answerNode = addMessage("Aura přemýšlí…", "assistant");
  answerNode.classList.add("typing");
  try {
    const response = await fetch("/api/chat", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message: clean})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Server vrátil chybu.");
    answerNode.textContent = data.reply;
    engineLabel.textContent = data.engine || "Aura Core 0.1";
  } catch (err) {
    answerNode.textContent = "Nepodařilo se spojit se serverem: " + err.message;
  }
  answerNode.classList.remove("typing");
  chatArea.scrollTop = chatArea.scrollHeight;
}
form.addEventListener("submit", e => { e.preventDefault(); sendMessage(input.value); });
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
});
document.querySelectorAll(".suggestion").forEach(b => b.addEventListener("click", () => sendMessage(b.textContent)));
document.getElementById("newChat").addEventListener("click", () => {
  chatArea.replaceChildren(); welcome.style.display = "block"; input.focus();
});
fetch("/api/status").then(r => r.json()).then(s => {
  statusText.textContent = s.trained ? "Aura Core 0.1 · připraveno" : "Aura Core 0.1 · čeká na trénink";
  engineLabel.textContent = s.engine;
}).catch(() => statusText.textContent = "Server není dostupný");
