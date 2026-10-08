import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="T-Rex Runner", page_icon="🦖", layout="centered")

st.title("🦖 T-Rex Runner trên Streamlit")
st.write("Nhấn **Phím cách (Space)** hoặc **chạm vào khung game** để nhảy qua chướng ngại vật!")

game_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: transparent;
      font-family: monospace;
      user-select: none;
    }
    #gameCanvas {
      background: #fafafa;
      border: 2px solid #555;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <canvas id="gameCanvas" width="600" height="200"></canvas>
  <script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");

    let dino = { x: 50, y: 150, width: 24, height: 30, vy: 0, jumping: false };
    let obstacles = [];
    let score = 0;
    let gameOver = false;
    let gameSpeed = 5;
    let frame = 0;

    function jump() {
      if (!dino.jumping && !gameOver) {
        dino.vy = -10;
        dino.jumping = true;
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
      dino = { x: 50, y: 150, width: 24, height: 30, vy: 0, jumping: false };
      obstacles = [];
      score = 0;
      gameSpeed = 5;
      gameOver = false;
      loop();
    }

    function loop() {
      if (gameOver) {
        ctx.fillStyle = "#333";
        ctx.font = "20px monospace";
        ctx.fillText("GAME OVER - Nhan Space de choi lai", 110, 100);
        return;
      }

      frame++;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.strokeStyle = "#888";
      ctx.beginPath();
      ctx.moveTo(0, 180);
      ctx.lineTo(canvas.width, 180);
      ctx.stroke();

      dino.y += dino.vy;
      dino.vy += 0.55;
      if (dino.y >= 150) {
        dino.y = 150;
        dino.jumping = false;
      }

      ctx.fillStyle = "#2e7d32";
      ctx.fillRect(dino.x, dino.y, dino.width, dino.height);

      if (frame % 80 === 0 && Math.random() > 0.3) {
        obstacles.push({ x: canvas.width, y: 152, width: 14, height: 28 });
      }

      for (let i = obstacles.length - 1; i >= 0; i--) {
        let obs = obstacles[i];
        obs.x -= gameSpeed;

        ctx.fillStyle = "#d32f2f";
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);

        if (
          dino.x < obs.x + obs.width &&
          dino.x + dino.width > obs.x &&
          dino.y < obs.y + obs.height &&
          dino.y + dino.height > obs.y
        ) {
          gameOver = true;
        }

        if (obs.x + obs.width < 0) {
          obstacles.splice(i, 1);
          score += 10;
          if (score % 50 === 0) gameSpeed += 0.3;
        }
      }

      ctx.fillStyle = "#333";
      ctx.font = "16px monospace";
      ctx.fillText("Score: " + score, 480, 30);

      requestAnimationFrame(loop);
    }

    loop();
  </script>
</body>
</html>
"""

components.html(game_code, height=220)
