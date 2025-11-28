from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# ===================== GAME STATE =====================
cash = 750_000
service = 78
co2 = 6200
round_no = 1

last_transport = None
last_warehouse = None

TARGET_CASH = 2_000_000
TARGET_SERVICE = 90
TARGET_CO2 = 4000
MAX_ROUNDS = 10


# ===================== RESET =====================
def reset_game():
    global cash, service, co2, round_no, last_transport, last_warehouse
    cash = 750_000
    service = 78
    co2 = 6200
    last_transport = None
    last_warehouse = None
    round_no = 1


# ===================== GLOBAL STYLES =====================
STYLE = """
<style>

    /* Animated Background */
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b, #0f172a);
        background-size: 300% 300%;
        animation: bgshift 15s ease-in-out infinite;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        margin: 0;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        color: white;
    }

    @keyframes bgshift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Main Card */
    .card {
        width: 92%;
        max-width: 550px;
        padding: 40px;
        background: rgba(255,255,255,0.10);
        border-radius: 18px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.45);
        animation: popin 0.7s ease-out;
    }

    /* Home Page Animation */
    .home-card {
        animation: slidedown 0.7s cubic-bezier(.25,.46,.45,.94);
    }

    @keyframes slidedown {
        0% { opacity:0; transform: translateY(-40px) scale(0.92); }
        100% { opacity:1; transform: translateY(0px) scale(1); }
    }

    /* Dashboard Animation */
    .dash-card {
        animation: rotatein 0.6s ease-out;
    }

    @keyframes rotatein {
        0% { opacity:0; transform: rotateX(-35deg) scale(0.9); }
        100% { opacity:1; transform: rotateX(0deg) scale(1); }
    }

    /* Summary / Game Over Card */
    .bounce-card {
        animation: bounceIn 0.6s ease-out;
    }

    @keyframes bounceIn {
        0% { transform: scale(0.6); opacity:0; }
        60% { transform: scale(1.08); opacity:1; }
        100% { transform: scale(1); }
    }

    /* Title Glow */
    h1 {
        font-size: 38px;
        text-shadow: 0 0 15px #22c55e;
        animation: glowslow 3s infinite alternate;
    }

    @keyframes glowslow {
        0% { text-shadow: 0 0 6px #22c55e; }
        100% { text-shadow: 0 0 16px #22c55e; }
    }

    h2 { font-size: 30px; }

    p, label {
        font-size: 19px;
    }

    /* Select Inputs */
    select {
        width: 92%;
        padding: 14px;
        background: #1e293b;
        border: none;
        border-radius: 10px;
        color: #fff;
        font-size: 18px;
        margin-top: 10px;
        transition: transform 0.15s ease;
    }

    select:hover {
        transform: scale(1.04);
    }

    /* Buttons (bug-free, centered, consistent) */
    button, a.button-link {
        width: 85%;
        display: block;
        margin: 25px auto 0 auto;
        padding: 14px 20px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: black;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        text-decoration: none;
        transition: 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    button:hover, a.button-link:hover {
        transform: scale(1.07);
        box-shadow: 0 0 20px #22c55e;
    }

    /* Ripple Effect */
    button:active::after, a.button-link:active::after {
        content: "";
        position: absolute;
        left: 50%;
        top: 50%;
        width: 5px;
        height: 5px;
        background: white;
        opacity: 0.8;
        border-radius: 50%;
        transform: translate(-50%, -50%) scale(1);
        animation: ripple 0.6s ease-out;
    }

    @keyframes ripple {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 0.9; }
        100% { transform: translate(-50%, -50%) scale(26); opacity: 0; }
    }

</style>
"""


# ===================== HOME PAGE =====================
@app.get("/", response_class=HTMLResponse)
def home():
    reset_game()
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card home-card">

            <h1>🚚 LOGISTICA.AI</h1>
            <p>Manage logistics across 10 strategic rounds.</p>

            <h3 style="color:#facc15; font-size:24px;">🎯 Win Conditions</h3>
            <p>Cash ≥ ₹20L <br> Service ≥ 90% <br> CO₂ ≤ 4000</p>

            <form action="/dashboard">
                <button>Start Game</button>
            </form>

        </div>

    </body></html>
    """


# ===================== DASHBOARD =====================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card dash-card">

            <h2>📊 Round {round_no}</h2>

            <p><b>💰 Cash:</b> ₹{cash}</p>
            <p><b>📦 Service Level:</b> {service}%</p
