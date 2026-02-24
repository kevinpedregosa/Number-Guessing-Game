const startForm = document.getElementById("start-form");
const guessForm = document.getElementById("guess-form");
const playAgainBtn = document.getElementById("play-again-btn");

const setupCard = document.getElementById("setup-card");
const gameCard = document.getElementById("game-card");

const statusUsername = document.getElementById("status-username");
const statusDifficulty = document.getElementById("status-difficulty");
const statusAttempts = document.getElementById("status-attempts");

const messagesEl = document.getElementById("messages");

const leaderboardEmpty = document.getElementById("leaderboard-empty");
const leaderboardTable = document.getElementById("leaderboard-table");
const leaderboardBody = document.getElementById("leaderboard-body");

function setGameVisible(visible) {
  if (visible) {
    gameCard.removeAttribute("aria-hidden");
    gameCard.classList.add("visible");
  } else {
    gameCard.setAttribute("aria-hidden", "true");
    gameCard.classList.remove("visible");
  }
}

function showMessage(text, style = "info") {
  if (!text) return;
  const msg = document.createElement("div");
  msg.className = `message ${style}`;
  msg.textContent = text;
  messagesEl.prepend(msg);
}

function clearMessages() {
  messagesEl.innerHTML = "";
}

function updateLeaderboard(leaderboard) {
  if (!leaderboard || leaderboard.length === 0) {
    leaderboardEmpty.hidden = false;
    leaderboardTable.hidden = true;
    leaderboardBody.innerHTML = "";
    return;
  }

  leaderboardEmpty.hidden = true;
  leaderboardTable.hidden = false;
  leaderboardBody.innerHTML = "";

  leaderboard.forEach((entry, index) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.username}</td>
      <td>${entry.attempts}</td>
      <td>${entry.difficulty}</td>
      <td>${entry.number}</td>
    `;
    leaderboardBody.appendChild(tr);
  });
}

async function fetchLeaderboard() {
  try {
    const res = await fetch("/api/leaderboard");
    if (!res.ok) return;
    const data = await res.json();
    updateLeaderboard(data.leaderboard || []);
  } catch (err) {
    // Silent failure for leaderboard fetch
  }
}

startForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearMessages();

  const formData = new FormData(startForm);
  const username = formData.get("username") || "Player";
  const difficulty = formData.get("difficulty") || "easy";

  try {
    const res = await fetch("/api/start-game", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, difficulty }),
    });

    if (!res.ok) {
      showMessage("Failed to start game. Please try again.", "error");
      return;
    }

    const data = await res.json();

    statusUsername.textContent = data.username;
    statusDifficulty.textContent = data.difficulty;
    statusAttempts.textContent = data.max_attempts;

    document.getElementById("guess").value = "";
    playAgainBtn.hidden = true;

    setGameVisible(true);
    showMessage(
      `New game started for ${data.username} on ${data.difficulty} difficulty.`,
      "success"
    );

    if (data.leaderboard) {
      updateLeaderboard(data.leaderboard);
    }
  } catch (err) {
    showMessage("An unexpected error occurred. Please try again.", "error");
  }
});

guessForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const input = document.getElementById("guess");
  const rawGuess = input.value;

  if (!rawGuess) {
    showMessage("Please enter a guess first.", "warning");
    return;
  }

  try {
    const res = await fetch("/api/guess", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ guess: rawGuess }),
    });

    const data = await res.json();

    if (!res.ok) {
      showMessage(data.error || "Invalid guess.", "error");
      return;
    }

    statusAttempts.textContent = data.attempts_left;

    const parts = [];
    if (data.distance_hint) parts.push(data.distance_hint);
    if (data.temp_feedback) parts.push(data.temp_feedback);
    if (parts.length) {
      showMessage(parts.join(" "), "info");
    }
    if (data.smart_hint) {
      showMessage(data.smart_hint, "hint");
    }

    if (data.game_over) {
      if (data.correct) {
        showMessage(
          `Correct! You guessed the number in ${data.attempt} attempts. Performance: ${data.performance}.`,
          "success"
        );
      } else {
        showMessage(
          `Game over. The number was ${data.secret}.`,
          "error"
        );
      }

      if (data.leaderboard) {
        updateLeaderboard(data.leaderboard);
      }

      playAgainBtn.hidden = false;
      input.value = "";
      input.disabled = true;
      guessForm.querySelector("button[type='submit']").disabled = true;
    } else {
      input.value = "";
      input.focus();
    }
  } catch (err) {
    showMessage("An unexpected error occurred while submitting your guess.", "error");
  }
});

playAgainBtn.addEventListener("click", () => {
  clearMessages();
  document.getElementById("guess").disabled = false;
  guessForm.querySelector("button[type='submit']").disabled = false;
  playAgainBtn.hidden = true;
  setGameVisible(false);
});

// Initial leaderboard load
fetchLeaderboard();

