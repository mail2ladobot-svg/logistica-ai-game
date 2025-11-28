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


# ===================== SHARED CSS =====================
STYLE = """
<style>
    body {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 20px;
        margin: 0;
        text-align: center;
    }

    h1, h2 { margin-bottom: 10px; }

    .card {
        background: rgba(255,255,255,0.08);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        max-width: 480px;
        margin: auto;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
    }

    select, button {
        width: 85%;
        padding: 12px;
        margin-top: 10px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
    }

    select {
        background: #1e293b;
        color: white;
    }

    button {
        background: #22c55e;
        color: black;
        margin-top: 20px;
        font-weight: bold;
        transition: 0.2s;
    }

    button:hover {
        transform: scale(1.05);
        background: #16a34a;
        cursor: pointer;
    }

    a.button-link {
        display: inline-block;
        margin-top: 20px;
        padding: 12px 25px;
        background: #22c55e;
        border-radius: 8px;
        text-decoration: none;
        color: black;
        font-size: 18px;
        transition: 0.2s;
        font-weight: bold;
    }

    a.button-link:hover {
        transform: scale(1.05);
        background: #16a34a;
    }

    @media (max-width: 480px) {
        .card { width: 90%; }
        button, select { width: 95%; }
    }
</style>
"""


# ===================== HOME PAGE =====================
@app.get("/", response_class=HTMLResponse)
def home():
    reset_game()

    return f"""
    <html>
    <head>{STYLE}</head>
    <body>

        <div class="card">
            <h1>🚚 LOGISTICA.AI</h1>
            <p>Manage logistics decisions across 10 strategic rounds.</p>

            <h3 style="color:#facc15">🎯 Win Conditions</h3>
            <p>Cash ≥ ₹20L<br>Service ≥ 90%<br>CO₂ ≤ 4000</p>

            <form action="/dashboard">
                <button>▶ Start Game</button>
            </form>
        </div>

    </body>
    </html>
    """


# ===================== DASHBOARD =====================
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    global cash, service, co2, round_no

    return f"""
    <html>
    <head>{STYLE}</head>
    <body>

        <div class="card">
            <h2>📊 Round {round_no}</h2>

            <p>💰 <b>Cash:</b> ₹{cash}</p>
            <p>📦 <b>Service:</b> {service}%</p>
            <p>🌿 <b>CO₂ Index:</b> {co2}</p>

            <form action="/play">
                <label><b>Transport Mode</b></label><br>
                <select name="transport">
                    <option value="EV">EV Fleet</option>
                    <option value="Rail">Rail + Truck</option>
                    <option value="Truck">Standard Trucks</option>
                    <option value="Air">Express Air</option>
                </select><br>

                <label><b>Warehouse Type</b></label><br>
                <select name="warehouse">
                    <option value="Auto">Fully Automated</option>
                    <option value="Semi">Semi Automated</option>
                    <option value="Manual">Manual</option>
                </select><br>

                <label><b>Green Strategy</b></label><br>
                <select name="green">
                    <option value="Basic">Basic</option>
                    <option value="Aggressive">Aggressive</option>
                    <option value="None">None</option>
                </select><br>

                <button>▶ Run Round</button>
            </form>

            <p style="color:#facc15;margin-top:15px;">
                🎯 Goal: ₹20L | 90% | CO₂ ≤ 4000<br>
                Rounds left: {MAX_ROUNDS - round_no + 1}
            </p>
        </div>

    </body>
    </html>
    """


# ===================== GAME LOGIC =====================
@app.get("/play", response_class=HTMLResponse)
def play(transport: str, warehouse: str, green: str):
    global cash, service, co2, round_no
    global last_transport, last_warehouse

    # Profit, service, CO₂ impacts
    profit_map = {"Truck": 120000, "Rail": 160000, "EV": 150000, "Air": 210000}
    service_map = {"Manual": -2, "Semi": 4, "Auto": 6}
    co2_map = {"Truck": 250, "Rail": -120, "EV": -200, "Air": 450}
    green_map = {"None": 100, "Basic": -150, "Aggressive": -350}

    # Mild repetition penalty
    penalty = 1.0
    if transport == last_transport: penalty -= 0.1
    if warehouse == last_warehouse: penalty -= 0.08
    penalty = max(0.75, penalty)

    # Random demand effect
    demand_factor = random.uniform(0.95, 1.1)

    # Profit calculation
    profit = int(profit_map[transport] * demand_factor * penalty)
    if green == "Aggressive": profit -= 30000

    # Update game state
    cash += profit
    service += service_map[warehouse]
    co2 += co2_map[transport] + green_map[green]
    service = min(100, max(60, service))
    co2 = max(2000, co2)

    last_transport = transport
    last_warehouse = warehouse
    round_no += 1

    # Winning screen
    if cash >= TARGET_CASH and service >= TARGET_SERVICE and co2 <= TARGET_CO2:
        return f"""
        <html><head>{STYLE}</head><body>
            <div class="card">
                <h1 style="color:#22c55e">🏆 YOU WON!</h1>
                <p>Excellent logistics management!</p>
                <a class="button-link" href="/">🔄 Play Again</a>
            </div>
        </body></html>
        """

    # Game Over
    if round_no > MAX_ROUNDS:
        return f"""
        <html><head>{STYLE}</head><body>
            <div class="card">
                <h1 style="color:red">❌ GAME OVER</h1>
                <p>You could not hit all targets.</p>
                <a class="button-link" href="/">🔄 Try Again</a>
            </div>
        </body></html>
        """

    # Mid-game summary
    return f"""
    <html><head>{STYLE}</head><body>
        <div class="card">
            <h2>Round {round_no - 1} Completed</h2>
            <p>Profit: ₹{profit}</p>
            <p>Cash: ₹{cash}</p>
            <p>Service: {service}%</p>
            <p>CO₂ Index: {co2}</p>
            <a class="button-link" href="/dashboard">▶ Continue</a>
        </div>
    </body></html>
    """


# ===================== END =====================

