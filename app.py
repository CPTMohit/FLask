"""
Catch the Star - a tiny web game
Run with:  python app.py
Then open: http://127.0.0.1:5000 in your browser
"""

from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Catch the Star</title>
<style>
  body {
    margin: 0;
    background: #111;
    color: #fff;
    font-family: Arial, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  h1 { margin-bottom: 5px; }
  #score { font-size: 20px; margin-bottom: 10px; }
  canvas {
    background: #222;
    border: 3px solid #555;
    border-radius: 8px;
  }
  #msg { margin-top: 10px; font-size: 16px; color: #aaa; }
</style>
</head>
<body>
  <h1>⭐ Catch the Star ⭐</h1>
  <div id="score">Score: 0 | Lives: 3</div>
  <canvas id="game" width="480" height="480"></canvas>
  <div id="msg">Use LEFT / RIGHT arrow keys to move the basket</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const msgEl = document.getElementById("msg");

const W = canvas.width, H = canvas.height;

let basket = { x: W / 2 - 40, y: H - 30, w: 80, h: 16, speed: 7 };
let star = spawnStar();
let score = 0;
let lives = 3;
let keys = {};
let gameOver = false;

function spawnStar() {
  return {
    x: Math.random() * (W - 20) + 10,
    y: -20,
    r: 10,
    speed: 2 + Math.random() * 2 + score * 0.05
  };
}

document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

function update() {
  if (gameOver) return;

  if (keys["ArrowLeft"]) basket.x -= basket.speed;
  if (keys["ArrowRight"]) basket.x += basket.speed;
  basket.x = Math.max(0, Math.min(W - basket.w, basket.x));

  star.y += star.speed;

  // Catch check
  if (
    star.y + star.r >= basket.y &&
    star.x >= basket.x &&
    star.x <= basket.x + basket.w
  ) {
    score += 1;
    star = spawnStar();
  } else if (star.y - star.r > H) {
    lives -= 1;
    star = spawnStar();
    if (lives <= 0) {
      gameOver = true;
      msgEl.textContent = "Game Over! Press R to restart.";
    }
  }

  scoreEl.textContent = `Score: ${score} | Lives: ${lives}`;
}

function draw() {
  ctx.clearRect(0, 0, W, H);

  // basket
  ctx.fillStyle = "#4caf50";
  ctx.fillRect(basket.x, basket.y, basket.w, basket.h);

  // star
  ctx.fillStyle = "#ffd700";
  ctx.beginPath();
  ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
  ctx.fill();

  if (gameOver) {
    ctx.fillStyle = "rgba(0,0,0,0.6)";
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#fff";
    ctx.font = "28px Arial";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", W / 2, H / 2 - 10);
    ctx.font = "16px Arial";
    ctx.fillText("Press R to restart", W / 2, H / 2 + 20);
  }
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

document.addEventListener("keydown", e => {
  if (e.key === "r" || e.key === "R") {
    if (gameOver) {
      score = 0;
      lives = 3;
      gameOver = false;
      star = spawnStar();
      msgEl.textContent = "Use LEFT / RIGHT arrow keys to move the basket";
    }
  }
});

loop();
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE)


if __name__ == "__main__":
    app.run(debug=True)
