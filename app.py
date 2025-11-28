from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# ---------- GAME STATE ----------
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

# ---------- HOME ----------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <body style="background:#0f172a;color:white;font-family:Arial;padding:40px">

        <h1>🚚 LOGISTICA.AI</h1>
        <p>You are managing a national logistics network. Optimize cost, service & sustainability.</p>

        <div style="color:#facc15;font-size:18px">
            🎯 Goal: Cash ≥ ₹20L | Service ≥ 90 | CO₂ ≤ 4000<br>
            Total Rounds: 10
        </div>

        <form action="/dashboard">
            <button style="margin-top:20px;padding:14px 30px;
                           font-size:18px;background:#22c55e;border:none;border-radius:5px;">
                ▶ Start Game
            </button>
        </form>

    </body>
    </html>
    """

# ---------- DASHBOARD ----------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    global cash, service, co2, round_no

    return f"""
    <html>
    <body style="background:#111;color:white;font-family:Arial;padding:30px">

        <h2>📊 Round {round_no}</h2>
        <p>💰 Cash: ₹{cash}</p>
        <p>📦 Service Level: {service}%</p>
        <p>🌿 CO₂ Index: {co2}</p>

        <form action="/play">
            <label>Transport:</label>
            <select name="transport">
                <option value="EV">EV Fleet</option>
                <option value="Rail">Rail + Truck</option>
                <option value="Truck">Standard Trucks</option>
                <option value="Air">Express Air</option>
            </select><br><br>

            <label>Warehouse:</label>
            <select name="warehouse">
                <option value="Auto">Fully Automated</option>
                <option value="Semi">Semi Automated</option>
                <option value="Manual">Manual</option>
            </select><br><br>

            <label>Green Strategy:</label>
            <select name="green">
                <option value="Basic">Basic</option>
                <option value="Aggressive">Aggressive</option>
                <option value="None">None</option>
            </select><br><br>

            <button type="submit">▶ Run Round</button>
        </form>

    </body>
    </html>
    """

# ---------- GAME LOGIC ----------
@app.get("/play", response_class=HTMLResponse)
def play(transport: str, warehouse: str, green: str):
    global cash, service, co2, round_no
    global last_transport, last_warehouse

    profit_map = {
        "Truck": 120000,
        "Rail": 160000,
        "EV": 150000,
        "Air": 210000
    }

    service_map = {
        "Manual": -2,
        "Semi": 4,
        "Auto": 6
    }

    co2_map = {
        "Truck": 250,
        "Rail": -120,
        "EV": -200,
        "Air": 450
    }

    green_map = {
        "None": 100,
        "Basic": -150,
        "Aggressive": -350
    }

    penalty = 1.0
    if transport == last_transport:
        penalty -= 0.1
    if warehouse == last_warehouse:
        penalty -= 0.08
    penalty = max(0.75, penalty)

    demand_factor = random.uniform(0.95, 1.1)
    profit = int(profit_map[transport] * demand_factor * penalty)

    if green == "Aggressive":
        profit -= 30000

    cash += profit
    service += service_map[warehouse]
    co2 += co2_map[transport] + green_map[green]

    last_transport = transport
    last_warehouse = warehouse

    service = min(100, max(60, service))
    co2 = max(2000, co2)
    round_no += 1

    # WIN
    if cash >= TARGET_CASH and service >= TARGET_SERVICE and co2 <= TARGET_CO2:
        return """
        <html>
        <body style="background:#0f172a;color:white;font-family:Arial;padding:40px">
            <h1 style='color:#22c55e'>🏆 YOU WON!</h1>
            <p>You successfully optimized cost, service and sustainability.</p>
        </body>
        </html>
        """

    # LOSE
    if round_no > MAX_ROUNDS:
        return """
        <html>
        <body style="background:#0f172a;color:white;font-family:Arial;padding:40px">
            <h1 style='color:red'>❌ GAME OVER</h1>
            <p>You couldn't reach the targets in 10 rounds.</p>
        </body>
        </html>
        """

    # CONTINUE
    return f"""
    <html>
    <body style="background:#111;color:white;font-family:Arial;padding:30px">
        <h2>✅ Round {round_no - 1} Result</h2>
        <p>Profit: ₹{profit}</p>
        <p>Cash: ₹{cash}</p>
        <p>Service: {service}%</p>
        <p>CO₂ Index: {co2}</p>
        <br>
        <a href="/dashboard" style="color:#22c55e;font-size:18px;">▶ Next Round</a>
    </body>
    </html>
    """
