import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="T-Rex Runner", page_icon="🦖", layout="centered")

st.title("🦖 T-Rex Runner Arcade")
st.write("Nhấn **Phím cách (Space)**, **Mũi tên lên (↑)** hoặc **chạm vào màn hình** để nhảy!")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {
      margin: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      background-color: transparent;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
      user-select: none;
    }
    #game-container {
      position: relative;
    }
    #gameCanvas {
      background: #f7f7f7;
      border: 2px solid #444;
      border-radius: 8px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
      cursor: pointer;
    }
    .controls {
      margin-top: 8px;
      display: flex;
      gap: 12px;
      align-items: center;
    }
    button {
      padding: 6px 14px;
      background: #2e7d32;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-weight: bold;
      font-size: 13px;
    }
    button:hover {
      background: #1b5e20;
    }
  </style>
</head>
<body>
  <div id="game-container">
    <canvas id="gameCanvas" width="600" height="200"></canvas>
  </div>
  <div class="controls">
    <button id="soundToggleBtn">🔊 Bật / Tắt Nhạc</button>
    <span style="font-size: 13px; color: #555;">Chạm hoặc bấm Space để nhảy & khởi động âm thanh</span>
  </div>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const soundToggleBtn = document.getElementById("soundToggleBtn");

    // ==========================================
    // ÂM THANH & NHẠC NỀN 8-BIT (WEB AUDIO API)
    // ==========================================
    let audioCtx = null;
    let isMuted = false;
    let bgmInterval = null;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        startBgm();
      }
    }

    function playTone(freq, duration, type="square") {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch(e) {}
    }

    function playJumpSound() {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(150, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(450, audioCtx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
      } catch(e) {}
    }

    function playHitSound() {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(120, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(40, audioCtx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.3);
      } catch(e) {}
    }

    // Giai điệu nhạc nền 8-bit lặp lại
    const bgmNotes = [261.63, 293.66, 329.63, 392.00, 329.63, 293.66];
    let noteIdx = 0;
    function startBgm() {
      if (bgmInterval) clearInterval(bgmInterval);
      bgmInterval = setInterval(() => {
        if (!gameOver && !isMuted && audioCtx) {
          playTone(bgmNotes[noteIdx], 0.16, "triangle");
          noteIdx = (noteIdx + 1) % bgmNotes.length;
        }
      }, 250);
    }

    soundToggleBtn.addEventListener("click", () => {
      initAudio();
      isMuted = !isMuted;
      soundToggleBtn.innerText = isMuted ? "🔇 Đã Tắt Nhạc" : "🔊 Bật / Tắt Nhạc";
    });

    // ==========================================
    // TẢI HÌNH ẢNH SPRITE (KHỦNG LONG & XƯƠNG RỒNG)
    // ==========================================
    const dinoImg = new Image();
    dinoImg.src = "data:image/svg+xml;utf8," + encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 47" width="44" height="47">
        <path fill="#535353" d="M22 0h14v2h-14zm14 2h8v12h-2v2h-6v2h-4v2h-2v2h-2v4h-2v2h-4v2H6v2H4v2H2v4H0v7h2v-5h2v-2h2v-2h2v-2h2v2h2v7h2v-6h4v6h2v-6h2v-2h2v-2h2v-2h2v-4h2v-2h2v-2h4v-2h2V12h-8V8h6V6h-8V2z"/>
        <circle cx="36" cy="5" r="1.5" fill="#ffffff" />
      </svg>
    `);

    const cactusImg = new Image();
    cactusImg.src = "data:image/svg+xml;utf8," + encodeURIComponent(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 45" width="24" height="45">
        <path fill="#2e7d32" d="M8 0h6v45H8zM2 14h6v6H2zm0 6h4v14H2zM14 18h6v6h-6zm4 6h4v10h-4z"/>
      </svg>
    `);

    // ==========================================
    // LOGIC TRÒ CHƠI
    // ==========================================
    let dino = { x: 50, y: 135, width: 36, height: 40, vy: 0, jumping: false };
    let obstacles = [];
    let score = 0;
    let highScore = 0;
    let gameOver = false;
    let gameSpeed = 5.2;
    let frame = 0;

    function jump() {
      initAudio();
      if (!dino.jumping && !gameOver) {
        dino.vy = -10.5;
        dino.jumping = true;
        playJumpSound();
      } else if (gameOver) {
        resetGame();
      }
    }

    window.addEventListener("keydown", (e) => {
      if (e.code === "Space" || e.code === "ArrowUp") {
        e.preventDefault();
        jump();
      }
    });

    canvas.addEventListener("touchstart", (e) => {
      e.preventDefault();
      jump();
    });
    canvas.addEventListener("mousedown", jump);

    function resetGame() {
      dino = { x: 50, y: 135, width: 36, height: 40, vy: 0, jumping: false };
      obstacles = [];
      score = 0;
      gameSpeed = 5.2;
      gameOver = false;
      loop();
    }

    function loop() {
      if (gameOver) {
        ctx.fillStyle = "#333";
        ctx.font = "bold 20px monospace";
        ctx.fillText("G A M E   O V E R", 200, 90);
        ctx.font = "14px monospace";
        ctx.fillText("Nhan Phim Cach hoac cham de choi lai", 150, 120);
        return;
      }

      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Mặt đất
      ctx.strokeStyle = "#9e9e9e";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, 175);
      ctx.lineTo(canvas.width, 175);
      ctx.stroke();

      // Cập nhật vị trí khủng long
      dino.y += dino.vy;
      dino.vy += 0.58; // Trọng lực
      if (dino.y >= 135) {
        dino.y = 135;
        dino.jumping = false;
      }

      // Vẽ khủng long T-Rex
      ctx.drawImage(dinoImg, dino.x, dino.y, dino.width, dino.height);

      // Sinh chướng ngại vật
      if (frame % 85 === 0 && Math.random() > 0.25) {
        obstacles.push({ x: canvas.width, y: 138, width: 22, height: 38 });
      }

      // Di chuyển chướng ngại vật & kiểm tra va chạm
      for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.x -= gameSpeed;

        // Vẽ cây xương rồng
        ctx.drawImage(cactusImg, obs.x, obs.y, obs.width, obs.height);

        // Hộp va chạm (Hitbox tinh chỉnh nhỏ hơn 4px để công bằng hơn)
        if (
          dino.x + 4 < obs.x + obs.width &&
          dino.x + dino.width - 4 > obs.x &&
          dino.y + 4 < obs.y + obs.height &&
          dino.y + dino.height > obs.y
        ) {
          gameOver = true;
          playHitSound();
          if (score > highScore) highScore = score;
        }

        if (obs.x + obs.width < 0) {
          obstacles.splice(i, 1);
          score += 10;
          if (score % 60 === 0) gameSpeed += 0.35; // Tăng dần tốc độ
        }
      }

      // Bảng điểm
      ctx.fillStyle = "#444";
      ctx.font = "bold 15px monospace";
      ctx.fillText(`HI ${highScore.toString().padStart(5, '0')}  ${score.toString().padStart(5, '0')}`, 430, 25);

      requestAnimationFrame(loop);
    }

    loop();
  </script>
</body>
</html>
"""

components.html(game_code, height=270)
