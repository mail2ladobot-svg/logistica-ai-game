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


# ===================== RESET GAME =====================
def reset_game():
    global cash, service, co2, round_no, last_transport, last_warehouse
    cash = 750_000
    service = 78
    co2 = 6200
    round_no = 1
    last_transport = None
    last_warehouse = None


# ===================== ANIMATED UI STYLES =====================
STYLE = """
<style>

    /* --- Animated Gradient Background --- */
    body {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        background: linear-gradient(135deg, #0f172a, #1e293b, #0f172a);
        background-size: 300% 300%;
        animation: bgAnimation 12s ease infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        color: white;
        text-align: center;
        overflow-x: hidden;
    }

    @keyframes bgAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- Card Animation --- */
    .card {
        background: rgba(255,255,255,0.12);
        padding: 40px;
        border-radius: 20px;
        width: 90%;
        max-width: 550px;
        backdrop-filter: blur(18px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.45);
        animation: cardPop 0.7s ease;
        transform-origin: center;
    }

    @keyframes cardPop {
        0% { opacity: 0; transform: scale(0.85) translateY(30px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    /* --- Neon Glow Text --- */
    h1 {
        font-size: 38px;
        text-shadow: 0 0 12px #22c55e, 0 0 22px #22c55e;
        animation: glowPulse 3s infinite alternate;
    }

    @keyframes glowPulse {
        from { text-shadow: 0 0 8px #22c55e; }
        to { text-shadow: 0 0 22px #22c55e; }
    }

    h2 { font-size: 30px; }

    p, label {
        font-size: 20px;
        margin: 10px 0;
    }

    /* --- Select Animations --- */
    select {
        width: 90%;
        padding: 14px;
        margin-top: 10px;
        background: #1e293b;
        border: none;
        border-radius: 10px;
        color: white;
        font-size: 18px;
        transition: transform 0.2s ease;
    }
    select:hover {
        transform: scale(1.03);
    }

    /* --- Animated Buttons --- */
    button, a.button-link {
        width: 90%;
        padding: 14px;
        margin-top: 25px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: black;
        font-size: 22px;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        cursor: pointer;
        transition: 0.25s ease;
        position: relative;
        overflow: hidden;
    }

    button:hover, a.button-link:hover {
        transform: scale(1.07);
        box-shadow: 0 0 18px #22c55e;
    }

    /* --- Ripple Effect --- */
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
        100% { transform: translate(-50%, -50%) scale(25); opacity: 0; }
    }

</style>
"""


# ===================== HOME PAGE =====================
@app.get("/", response_class=HTMLResponse)
def home():
    reset_game()
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card">
            <h1>🚚 LOGISTICA.AI</h1>
            <p>Manage logistics decisions across 10 strategic rounds.</p>

            <h3 style="color:#facc15; font-size:24px; margin-top:20px;">🎯 Win Conditions</h3>
            <p>Cash ≥ ₹20L <br> Service ≥ 90% <br> CO₂ ≤ 4000</p>

            <form action="/dashboard">
                <button>▶ Start Game</button>
            </form>
        </div>

    </body></html>
    """


# ===================== DASHBOARD =====================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card">

            <h2>📊 Round {round_no}</h2>

            <p><b>💰 Cash:</b> ₹{cash}</p>
            <p><b>📦 Service Level:</b> {service}%</p>
            <p><b>🌿 CO₂ Index:</b> {co2}</p>

            <form action="/play">

                <label><b>Transport Mode</b></label>
                <select name="transport">
                    <option value="EV">EV Fleet</option>
                    <option value="Rail">Rail + Truck</option>
                    <option value="Truck">Standard Trucks</option>
                    <option value="Air">Express Air</option>
                </select>

                <label><b>Warehouse Type</b></label>
                <select name="warehouse">
                    <option value="Auto">Fully Automated</option>
                    <option value="Semi">Semi Automated</option>
                    <option value="Manual">Manual</option>
                </select>

                <label><b>Green Strategy</b></label>
                <select name="green">
                    <option value="Basic">Basic</option>
                    <option value="Aggressive">Aggressive</option>
                    <option value="None">None</option>
                </select>

                <button>▶ Run Round</button>

            </form>

            <p style="color:#facc15; font-size:18px; margin-top:15px;">
                🎯 Goal: ₹20L | 90% | CO₂ ≤ 4000 <br>
                Rounds left: {MAX_ROUNDS - round_no + 1}
            </p>
        </div>

    </body></html>
    """


# ===================== GAME LOGIC =====================
@app.get("/play", response_class=HTMLResponse)
def play(transport: str, warehouse: str, green: str):
    global cash, service, co2, round_no, last_transport, last_warehouse

    profit_map = {"Truck": 120000, "Rail": 160000, "EV": 150000, "Air": 210000}
    service_map = {"Manual": -2, "Semi": 4, "Auto": 6}
    co2_map = {"Truck": 250, "Rail": -120, "EV": -200, "Air": 450}
    green_map = {"None": 100, "Basic": -150, "Aggressive": -350}

    penalty = 1.0
    if transport == last_transport: penalty -= 0.1
    if warehouse == last_warehouse: penalty -= 0.08
    penalty = max(0.75, penalty)

    demand_factor = random.uniform(0.95, 1.1)
    profit = int(profit_map[transport] * demand_factor * penalty)

    if green == "Aggressive":
        profit -= 30000

    cash += profit
    service += service_map[warehouse]
    co2 += co2_map[transport] + green_map[green]
    service = min(100, max(60, service))
    co2 = max(2000, co2)

    last_transport = transport
    last_warehouse = warehouse
    round_no += 1

    # WIN SCREEN
    if cash >= TARGET_CASH and service >= TARGET_SERVICE and co2 <= TARGET_CO2:
        return f"""
        <html><head>{STYLE}</head><body>
            <div class="card">
                <h1 style="color:#22c55e; font-size:36px;">🏆 YOU WON!</h1>
                <p style="font-size:20px;">You balanced the entire logistics ecosystem!</p>
                <a class="button-link" href="/">🔄 Play Again</a>
            </div>
        </body></html>
        """

    # GAME OVER
    if round_no > MAX_ROUNDS:
        return f"""
        <html><head>{STYLE}</head><body>
            <div class="card">
                <h1 style="color:red; font-size:36px;">❌ GAME OVER</h1>
                <p style="font-size:20px;">You failed to meet all KPIs.</p>
                <a class="button-link" href="/">🔄 Try Again</a>
            </div>
        </body></html>
        """

    # CONTINUE
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card">
            <h2 style="font-size:28px;">Round {round_no - 1} Summary</h2>
            <p>Profit: ₹{profit}</p>
            <p>Cash: ₹{cash}</p>
            <p>Service: {service}%</p>
            <p>CO₂ Index: {co2}</p>

            <a class="button-link" href="/dashboard">▶ Continue</a>
        </div>

    </body></html>
    """


# ===================== END =====================

