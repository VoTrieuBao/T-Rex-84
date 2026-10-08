import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="T-Rex Chrome Runner Pro", page_icon="🦖", layout="centered")

st.title("🦖 T-Rex Runner Arcade Pro")
st.caption("🎮 **Điều khiển:** Phím cách / Mũi tên Lên (Nhảy) | Mũi tên Xuống (Cúi người)")

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
    #gameCanvas {
      border: 2px solid #333;
      border-radius: 8px;
      box-shadow: 0 6px 14px rgba(0,0,0,0.15);
      cursor: pointer;
      transition: background-color 0.8s ease;
    }
    .hud {
      margin-top: 10px;
      display: flex;
      gap: 15px;
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
    button:hover { background: #1b5e20; }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="640" height="220"></canvas>
  <div class="hud">
    <button id="soundBtn">🔊 Bật / Tắt Nhạc</button>
    <span style="font-size: 13px; color: #555;">Bấm Space/↑ để Nhảy, Giữ ↓ để Cúi</span>
  </div>

  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const soundBtn = document.getElementById("soundBtn");

    // ==========================================
    // ÂM THANH & NHẠC NỀN
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

    function playTone(freq, dur, type="square", vol=0.07) {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(vol, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + dur);
      } catch(e) {}
    }

    function playJumpSound() {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(160, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(500, audioCtx.currentTime + 0.14);
        gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.14);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.14);
      } catch(e) {}
    }

    function playHitSound() {
      if (isMuted || !audioCtx) return;
      try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = "sawtooth";
        osc.frequency.setValueAtTime(140, audioCtx.currentTime);
        osc.frequency.linearRampToValueAtTime(30, audioCtx.currentTime + 0.35);
        gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
        gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.35);
      } catch(e) {}
    }

    const bgmNotes = [261.6, 293.6, 329.6, 392.0, 329.6, 293.6];
    let noteIdx = 0;
    function startBgm() {
      if (bgmInterval) clearInterval(bgmInterval);
      bgmInterval = setInterval(() => {
        if (!gameOver && !isMuted && audioCtx) {
          playTone(bgmNotes[noteIdx], 0.16, "triangle", 0.05);
          noteIdx = (noteIdx + 1) % bgmNotes.length;
        }
      }, 240);
    }

    soundBtn.addEventListener("click", () => {
      initAudio();
      isMuted = !isMuted;
      soundBtn.innerText = isMuted ? "🔇 Đã Tắt Nhạc" : "🔊 Bật / Tắt Nhạc";
    });

    // ==========================================
    // SPRITES VECTOR NÉT CHUẨN ARCADE
    // ==========================================
    function createSvgImg(svgXml) {
      const img = new Image();
      img.src = "data:image/svg+xml;utf8," + encodeURIComponent(svgXml);
      return img;
    }

    // Khủng long chạy chân 1
    const dinoRun1 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 47" width="44" height="47">
        <path fill="#4b5563" d="M22 0h14v2h-14zm14 2h8v12h-2v2h-6v2h-4v2h-2v2h-2v4h-2v2h-4v2H6v2H4v2H2v4H0v7h2v-5h2v-2h2v-2h2v-2h2v2h2v7h2v-6h4v6h2v-6h2v-2h2v-2h2v-2h2v-4h2v-2h2v-2h4v-2h2V12h-8V8h6V6h-8V2z"/>
        <rect x="36" y="4" width="3" height="3" fill="#ffffff"/>
      </svg>
    `);

    // Khủng long chạy chân 2
    const dinoRun2 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 44 47" width="44" height="47">
        <path fill="#4b5563" d="M22 0h14v2h-14zm14 2h8v12h-2v2h-6v2h-4v2h-2v2h-2v4h-2v2h-4v2H6v2H4v2H2v4H0v7h2v-5h2v-2h2v-2h2v-2h2v6h2v-4h4v6h2v-6h2v-2h2v-2h2v-2h2v-4h2v-2h2v-2h4v-2h2V12h-8V8h6V6h-8V2z"/>
        <rect x="36" y="4" width="3" height="3" fill="#ffffff"/>
      </svg>
    `);

    // Khủng long Cúi (Ducking)
    const dinoDuck1 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 59 30" width="59" height="30">
        <path fill="#4b5563" d="M0 16h4v-2h8v-2h6v-2h12v-2h18v2h-2v2h8v10h-2v2h-8v-2h-4v4h-2v2h-4v-4h-2v4h-2v-4h-8v-2H16v-2H6v2H0z"/>
        <rect x="49" y="10" width="3" height="3" fill="#ffffff"/>
      </svg>
    `);

    const dinoDuck2 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 59 30" width="59" height="30">
        <path fill="#4b5563" d="M0 16h4v-2h8v-2h6v-2h12v-2h18v2h-2v2h8v10h-2v2h-8v-2h-4v4h-2v-4h-4v4h-2v-4h-8v-2H16v-2H6v2H0z"/>
        <rect x="49" y="10" width="3" height="3" fill="#ffffff"/>
      </svg>
    `);

    // Chim bay (Vỗ cánh lên / xuống)
    const bird1 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 46 36" width="46" height="36">
        <path fill="#374151" d="M22 0h6v8h-6zm0 8h16v6H22zm0 6h24v6H22zm-8 6h32v6H14zm-8 6h40v6H6zM0 32h34v4H0z"/>
      </svg>
    `);
    const bird2 = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 46 36" width="46" height="36">
        <path fill="#374151" d="M14 6h16v6H14zm-8 6h30v6H6zm-6 6h46v6H0zm8 6h28v6H8zm12 6h8v6h-8z"/>
      </svg>
    `);

    // Xương rồng lớn & nhỏ
    const cactusSingle = createSvgImg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 45" width="24" height="45">
        <path fill="#15803d" d="M8 0h8v45H8zM2 14h6v6H2zm0 6h4v14H2zM16 18h6v6h-6zm4 6h4v10h-4z"/>
      </svg>
    `);

    // ==========================================
    // BIẾN KHỞI TẠO TRÒ CHƠI
    // ==========================================
    const GROUND_Y = 175;
    let dino = {
      x: 50,
      y: GROUND_Y - 42,
      w: 42,
      h: 44,
      vy: 0,
      jumping: false,
      ducking: false
    };

    let obstacles = [];
    let clouds = [{ x: 150, y: 40 }, { x: 380, y: 70 }, { x: 550, y: 30 }];
    let stars = [];
    for(let i=0; i<25; i++) {
      stars.push({ x: Math.random() * 640, y: Math.random() * 120, r: Math.random() * 1.5 + 0.5 });
    }

    let score = 0;
    let highScore = 0;
    let gameOver = false;
    let speed = 5.5;
    let frame = 0;
    let isNight = false;

    // Phím điều khiển
    const keys = {};
    window.addEventListener("keydown", (e) => {
      keys[e.code] = true;
      if (e.code === "Space" || e.code === "ArrowUp") {
        e.preventDefault();
        jump();
      }
      if (e.code === "ArrowDown") {
        e.preventDefault();
      }
    });

    window.addEventListener("keyup", (e) => {
      keys[e.code] = false;
    });

    canvas.addEventListener("touchstart", (e) => {
      e.preventDefault();
      jump();
    });
    canvas.addEventListener("mousedown", jump);

    function jump() {
      initAudio();
      if (!dino.jumping && !dino.ducking && !gameOver) {
        dino.vy = -11.5;
        dino.jumping = true;
        playJumpSound();
      } else if (gameOver) {
        resetGame();
      }
    }

    function resetGame() {
      dino.y = GROUND_Y - 42;
      dino.vy = 0;
      dino.jumping = false;
      dino.ducking = false;
      obstacles = [];
      score = 0;
      speed = 5.5;
      gameOver = false;
      isNight = false;
      loop();
    }

    // ==========================================
    // VÒNG LẶP CHÍNH
    // ==========================================
    function loop() {
      if (gameOver) {
        ctx.fillStyle = isNight ? "#f3f4f6" : "#1f2937";
        ctx.font = "bold 22px monospace";
        ctx.fillText("G A M E   O V E R", 220, 95);
        ctx.font = "14px monospace";
        ctx.fillText("Nhan Space hoac cham de choi lai", 185, 125);
        return;
      }

      frame++;
      
      // Tăng điểm
      if (frame % 5 === 0) {
        score++;
        // Cứ mỗi 100 điểm: Đổi Ngày / Đêm và Tăng Tốc Độ
        if (score % 100 === 0) {
          isNight = (Math.floor(score / 100) % 2 === 1);
          speed += 0.45; // Tăng độ khó
          playTone(600, 0.2, "sine", 0.1); // Tiếng ting báo hiệu qua 100 điểm
        }
      }

      // Xử lý Cúi (Duck)
      if (keys["ArrowDown"] && !dino.jumping) {
        dino.ducking = true;
        dino.w = 56;
        dino.h = 28;
        dino.y = GROUND_Y - 28;
      } else if (!dino.jumping) {
        dino.ducking = false;
        dino.w = 42;
        dino.h = 44;
        dino.y = GROUND_Y - 44;
      }

      // Vật lý nhảy
      if (dino.jumping) {
        dino.y += dino.vy;
        dino.vy += 0.65; // Trọng lực
        if (dino.y >= GROUND_Y - 44) {
          dino.y = GROUND_Y - 44;
          dino.jumping = false;
          dino.vy = 0;
        }
      }

      // Xoá màn hình theo màu Ngày/Đêm
      ctx.fillStyle = isNight ? "#111827" : "#f9fafb";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Vẽ Trăng Sao (Đêm) hoặc Mây (Ngày)
      if (isNight) {
        ctx.fillStyle = "#fbbf24";
        ctx.beginPath();
        ctx.arc(560, 45, 16, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#ffffff";
        stars.forEach(s => {
          ctx.beginPath();
          ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
          ctx.fill();
        });
      } else {
        ctx.fillStyle = "#e5e7eb";
        clouds.forEach(c => {
          c.x -= speed * 0.25;
          if (c.x < -60) c.x = canvas.width + Math.random() * 80;
          ctx.beginPath();
          ctx.arc(c.x, c.y, 14, 0, Math.PI*2);
          ctx.arc(c.x + 15, c.y - 6, 18, 0, Math.PI*2);
          ctx.arc(c.x + 32, c.y, 14, 0, Math.PI*2);
          ctx.fill();
        });
      }

      // Vẽ Đường Đất
      ctx.strokeStyle = isNight ? "#4b5563" : "#9ca3af";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(0, GROUND_Y);
      ctx.lineTo(canvas.width, GROUND_Y);
      ctx.stroke();

      // Vẽ Khủng Long (Chọn Frame Chạy hoặc Cúi)
      let currentDinoImg;
      const legToggle = Math.floor(frame / 6) % 2 === 0;
      if (dino.ducking) {
        currentDinoImg = legToggle ? dinoDuck1 : dinoDuck2;
      } else if (dino.jumping) {
        currentDinoImg = dinoRun1;
      } else {
        currentDinoImg = legToggle ? dinoRun1 : dinoRun2;
      }
      ctx.drawImage(currentDinoImg, dino.x, dino.y, dino.w, dino.h);

      // Sinh chướng ngại vật (Cây xương rồng hoặc Chim)
      const minDistance = Math.max(55, 95 - Math.floor(score / 50));
      if (frame % minDistance === 0 && Math.random() > 0.28) {
        // Sau 100 điểm bắt đầu xuất hiện Chim
        const canSpawnBird = score >= 100 && Math.random() > 0.45;

        if (canSpawnBird) {
          // Chim: 2 độ cao (Bay thấp buộc cúi: 130px; Bay tầm trung: 105px)
          const birdY = Math.random() > 0.5 ? (GROUND_Y - 32) : (GROUND_Y - 55);
          obstacles.push({
            type: "bird",
            x: canvas.width,
            y: birdY,
            w: 42,
            h: 30
          });
        } else {
          // Xương rồng mặt đất
          obstacles.push({
            type: "cactus",
            x: canvas.width,
            y: GROUND_Y - 42,
            w: 24,
            h: 42
          });
        }
      }

      // Xử lý di chuyển & va chạm
      for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.x -= speed;

        // Vẽ chướng ngại vật
        if (obs.type === "cactus") {
          ctx.drawImage(cactusSingle, obs.x, obs.y, obs.w, obs.h);
        } else {
          const wingToggle = Math.floor(frame / 10) % 2 === 0;
          ctx.drawImage(wingToggle ? bird1 : bird2, obs.x, obs.y, obs.w, obs.h);
        }

        // Hitbox chính xác (thu nhỏ lề 4px để công bằng)
        const padX = 5, padY = 4;
        if (
          dino.x + padX < obs.x + obs.w - padX &&
          dino.x + dino.w - padX > obs.x + padX &&
          dino.y + padY < obs.y + obs.h - padY &&
          dino.y + dino.h - padY > obs.y + padY
        ) {
          gameOver = true;
          playHitSound();
          if (score > highScore) highScore = score;
        }

        if (obs.x + obs.w < 0) {
          obstacles.splice(i, 1);
        }
      }

      // Hiển thị Điểm số & Chế độ ngày đêm
      ctx.fillStyle = isNight ? "#e5e7eb" : "#374151";
      ctx.font = "bold 15px monospace";
      const scoreStr = score.toString().padStart(5, '0');
      const highStr = highScore.toString().padStart(5, '0');
      ctx.fillText(`HI ${highStr}  ${scoreStr}`, 470, 26);

      requestAnimationFrame(loop);
    }

    loop();
  </script>
</body>
</html>
"""

components.html(game_code, height=280)
