// Biến toàn cục
let ws = null;
let playerName = "";
let playerScore = 0,
  opponentScore = 0;
let canPlay = false;
let searchTimerInterval = null;
let searchStartTime = null;

// Hàm fade ẩn màn hình cũ, hiện màn hình mới (opacity animation)
function fadeToggle(showEl, hideEl, duration = 500) {
  if (hideEl) {
    hideEl.style.transition = `opacity ${duration}ms`;
    hideEl.style.opacity = 1;
    // Ẩn dần
    hideEl.style.opacity = 0;
    setTimeout(() => {
      hideEl.classList.add("hidden");
      if (showEl) {
        showEl.classList.remove("hidden");
        showEl.style.transition = `opacity ${duration}ms`;
        showEl.style.opacity = 0;
        setTimeout(() => {
          showEl.style.opacity = 1;
        }, 10);
      }
    }, duration);
  } else if (showEl) {
    // Chỉ hiện
    showEl.classList.remove("hidden");
    showEl.style.transition = `opacity ${duration}ms`;
    showEl.style.opacity = 0;
    setTimeout(() => {
      showEl.style.opacity = 1;
    }, 10);
  }
}

// Bắt đầu đếm thời gian tìm đối thủ (dùng Date.now để chính xác hơn)
function startSearchTimer() {
  searchStartTime = Date.now();
  updateSearchTimer(); // cập nhật ngay lần đầu

  if (searchTimerInterval) clearInterval(searchTimerInterval);

  // Cập nhật mỗi 300ms cho mượt
  searchTimerInterval = setInterval(() => {
    updateSearchTimer();
  }, 300);
}

// Cập nhật số giây tìm đối thủ
function updateSearchTimer() {
  const elapsedMs = Date.now() - searchStartTime;
  const elapsedSec = Math.floor(elapsedMs / 1000);
  document.getElementById("search-timer").innerText = `Time: ${elapsedSec}s`;
}

// Dừng đếm và ẩn đồng hồ
function stopSearchTimer() {
  if (searchTimerInterval) clearInterval(searchTimerInterval);
  searchTimerInterval = null;
  document.getElementById("search-timer").innerText = "";
}

// Cập nhật text kết quả với animation phóng to thu nhỏ
function setResultText(text) {
  const resultEl = document.getElementById("result");
  resultEl.innerText = text;
  resultEl.style.transform = "scale(1.5)";
  resultEl.style.transition = "transform 0.3s ease";

  setTimeout(() => {
    resultEl.style.transform = "scale(1)";
  }, 300);
}

// Hiệu ứng tăng điểm số dần dần
function animateScoreUpdate(el, start, end) {
  const duration = 500;
  const stepTime = 30;
  const steps = duration / stepTime;
  let currentStep = 0;
  let increment = (end - start) / steps;
  let currentValue = start;

  const interval = setInterval(() => {
    currentStep++;
    currentValue += increment;
    el.innerText = `${el.id === "player-score" ? "You: " : "Opponent: "}${Math.round(currentValue)}`;
    if (currentStep >= steps) {
      el.innerText = `${el.id === "player-score" ? "You: " : "Opponent: "}${end}`;
      clearInterval(interval);
    }
  }, stepTime);
}

function joinGame() {
  playerName = document.getElementById("name").value.trim();
  if (!playerName) return alert("Enter your name first!");

  if (ws) {
    ws.close();
    ws = null;
  }

  ws = new WebSocket("ws://127.0.0.1:8765");

  ws.onopen = () => {
    ws.send(JSON.stringify({ action: "join", name: playerName }));
    document.getElementById("loading").classList.remove("hidden");
    startSearchTimer();
    canPlay = false;
    disableChoices(true);
    setResultText("");
  };

  ws.onmessage = (event) => {
    let data = JSON.parse(event.data);

    if (data.action === "waiting") {
      document.getElementById("loading").querySelector("p").innerText =
        "Waiting for opponent...";
    } else if (data.action === "start_game") {
      stopSearchTimer();
      fadeToggle(
        document.getElementById("game-screen"),
        document.getElementById("login-screen")
      );

      document.getElementById("loading").classList.add("hidden");
      document.getElementById("opponent-name").innerText = data.opponent;
      canPlay = true;
      disableChoices(false);
      setResultText("Game started! Make your move.");
    } else if (data.action === "round_result") {
      setResultText(data.message);
      updateScoreFromMessage(data.message);
      canPlay = true;
      disableChoices(false);
    } else if (data.action === "opponent_quit") {
      setResultText(data.message);
      canPlay = false;
      disableChoices(true);

      setTimeout(() => {
        quitGame();
        alert("Opponent has left the game. Returning to main screen.");
      }, 3000);
    }
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
    alert("Connection error. Please refresh and try again.");
    stopSearchTimer();
  };

  ws.onclose = (event) => {
    console.log("WebSocket closed", event);
    alert("Connection closed. Please refresh to reconnect.");
    stopSearchTimer();
  };
}

function makeMove(move) {
  if (!canPlay) {
    alert("Please wait for your turn or connection.");
    return;
  }
  if (!ws || ws.readyState !== WebSocket.OPEN) {
    alert("Connection lost. Please refresh to reconnect.");
    return;
  }

  ws.send(JSON.stringify({ action: "move", move: move }));
  canPlay = false;
  disableChoices(true);
}

function updateScoreFromMessage(message) {
  let playerScoreEl = document.getElementById("player-score");
  let opponentScoreEl = document.getElementById("opponent-score");

  let oldPlayerScore = playerScore;
  let oldOpponentScore = opponentScore;

  if (message.toLowerCase().includes("win")) {
    playerScore++;
  } else if (message.toLowerCase().includes("lose")) {
    opponentScore++;
  }

  animateScoreUpdate(playerScoreEl, oldPlayerScore, playerScore);
  animateScoreUpdate(opponentScoreEl, oldOpponentScore, opponentScore);
}

function disableChoices(disable) {
  const choices = document.querySelectorAll(".choice");
  choices.forEach(
    (ch) => (ch.style.pointerEvents = disable ? "none" : "auto")
  );
}

function quitGame() {
  if (ws) {
    ws.close();
    ws = null;
  }
  // Reset UI
  fadeToggle(
    document.getElementById("login-screen"),
    document.getElementById("game-screen")
  );
  document.getElementById("loading").classList.add("hidden");

  // Reset scores
  playerScore = 0;
  opponentScore = 0;
  document.getElementById("player-score").innerText = "You: 0";
  document.getElementById("opponent-score").innerText = "Opponent: 0";

  // Clear inputs and messages
  document.getElementById("name").value = "";
  setResultText("");

  stopSearchTimer();

  canPlay = false;
  disableChoices(true);
}
