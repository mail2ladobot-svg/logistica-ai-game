from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import random

app = FastAPI()

# ===================== GAME STATE =====================
cash = 750000
service = 78
co2 = 6200
round_no = 1

last_transport = None
last_warehouse = None

TARGET_CASH = 2000000
TARGET_SERVICE = 90
TARGET_CO2 = 4000
MAX_ROUNDS = 10


# ===================== RESET =====================
def reset_game():
    global cash, service, co2, round_no, last_transport, last_warehouse
    cash = 750000
    service = 78
    co2 = 6200
    round_no = 1
    last_transport = None
    last_warehouse = None


# ===================== GLOBAL STYLES =====================
STYLE = """
<style>

    body {
        margin: 0;
        background: linear-gradient(135deg, #0f172a, #1e293b, #0f172a);
        background-size: 300% 300%;
        animation: bgshift 15s ease-in-out infinite;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        height: 100vh;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    @keyframes bgshift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .card {
        width: 92%;
        max-width: 550px;
        padding: 40px;
        background: rgba(255,255,255,0.10);
        border-radius: 18px;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.45);
        text-align: center;
    }

    .home-card { animation: slidedown 0.7s cubic-bezier(.25,.46,.45,.94); }
    .dash-card { animation: rotatein 0.6s ease-out; }
    .bounce-card { animation: bounceIn 0.6s ease-out; }

    @keyframes slidedown {
        0% { opacity:0; transform: translateY(-40px) scale(0.92); }
        100% { opacity:1; transform: translateY(0px) scale(1); }
    }

    @keyframes rotatein {
        0% { opacity:0; transform: rotateX(-35deg) scale(0.9); }
        100% { opacity:1; transform: rotateX(0deg) scale(1); }
    }

    @keyframes bounceIn {
        0% { transform: scale(0.6); opacity:0; }
        60% { transform: scale(1.1); opacity:1; }
        100% { transform: scale(1); }
    }

    h1 {
        font-size: 38px;
        text-shadow: 0 0 15px #22c55e;
        animation: glowpulse 3s infinite alternate;
    }

    @keyframes glowpulse {
        0% { text-shadow: 0 0 6px #22c55e; }
        100% { text-shadow: 0 0 16px #22c55e; }
    }

    h2 { font-size: 30px; }
    p, label { font-size: 19px; }

    select {
        width: 92%;
        padding: 14px;
        background: #1e293b;
        border-radius: 10px;
        color: white;
        border: none;
        font-size: 18px;
        margin-top: 10px;
        transition: transform 0.15s ease;
    }
    select:hover { transform: scale(1.04); }

    button, a.button-link {
        width: 85%;
        margin: 25px auto 0 auto;
        padding: 14px 20px;
        background: linear-gradient(90deg, #22c55e, #16a34a);
        color: black;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        display: block;
        transition: 0.25s ease;
        text-decoration: none;
    }

    button:hover, a.button-link:hover {
        transform: scale(1.07);
        box-shadow: 0 0 20px #22c55e;
    }

    /* CONFETTI ANIMATION */
    .confetti {
        position: fixed;
        width: 8px;
        height: 14px;
        background: var(--color);
        top: -10px;
        left: var(--left);
        opacity: 0.9;
        transform: rotate(var(--angle));
        animation: fall var(--duration) linear infinite;
    }

    @keyframes fall {
        to { transform: translateY(120vh) rotate(360deg); }
    }

    /* Skull Shake Animation */
    .skull {
        font-size: 70px;
        display: inline-block;
        animation: skullshake 0.8s ease-in-out infinite;
        text-shadow: 0 0 20px red;
    }

    @keyframes skullshake {
        0% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        50% { transform: translateX(10px); }
        75% { transform: translateX(-6px); }
        100% { transform: translateX(0); }
    }

</style>
"""


# ===================== HOME =====================
@app.get("/", response_class=HTMLResponse)
def home():
    reset_game()
    return f"""
    <html><head>{STYLE}</head><body>
        <div class="card home-card">
            <h1>🚚 LOGISTICA.AI</h1>
            <p>Manage logistics across 10 strategic rounds.</p>

            <h3 style="color:#facc15;">🎯 Win Conditions</h3>
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
    global cash, service, co2, round_no

    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card dash-card">

            <h2>📊 Round {round_no}</h2>

            <p><b>💰 Cash:</b> ₹{cash}</p>
            <p><b>📦 Service:</b> {service}%</p>
            <p><b>🌿 CO₂:</b> {co2}</p>

            <form action="/play">

                <label>Transport Mode</label>
                <select name="transport">
                    <option value="EV">EV Fleet</option>
                    <option value="Rail">Rail + Truck</option>
                    <option value="Truck">Standard Trucks</option>
                    <option value="Air">Express Air</option>
                </select>

                <label>Warehouse Type</label>
                <select name="warehouse">
                    <option value="Auto">Automated</option>
                    <option value="Semi">Semi Automated</option>
                    <option value="Manual">Manual</option>
                </select>

                <label>Green Strategy</label>
                <select name="green">
                    <option value="Basic">Basic</option>
                    <option value="Aggressive">Aggressive</option>
                    <option value="None">None</option>
                </select>

                <button>Run Round</button>

            </form>

            <p style="color:#facc15; margin-top:15px;">
                Goal: ₹20L | 90% | CO₂ ≤ 4000 <br>
                Rounds Left: {MAX_ROUNDS - round_no + 1}
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
    if transport == last_transport:
        penalty -= 0.1
    if warehouse == last_warehouse:
        penalty -= 0.08
    penalty = max(0.75, penalty)

    demand_factor = random.uniform(0.95, 1.1)
    profit = int(profit_map[transport] * demand_factor *
                penalty)

    if green == "Aggressive":
        profit -= 30000

    cash += profit
    service += service_map[warehouse]
    co2 += co2_map[transport] + green_map[green]

    service = min(100, max(60, service))
    co2 = max(1000, co2)

    last_transport = transport
    last_warehouse = warehouse

    round_no += 1

    # ================= WIN SCREEN =====================
    if cash >= TARGET_CASH and service >= TARGET_SERVICE and co2 <= TARGET_CO2:
        confetti_html = "".join([
            f"<div class='confetti' style='--left:{random.randint(0,100)}vw; "
            f"--duration:{random.uniform(3,7)}s; --angle:{random.randint(0,360)}deg; "
            f"--color:hsl({random.randint(0,360)},80%,60%);'></div>"
            for _ in range(60)
        ])

        return f"""
        <html><head>{STYLE}</head><body>
            {confetti_html}
            <div class="card bounce-card">
                <h1 style="color:#22c55e;">🏆 YOU WON!</h1>
                <p>Excellent logistics management!</p>
                <a class="button-link" href="/">Play Again</a>
            </div>
        </body></html>
        """

    # ================= LOSE SCREEN =====================
    if round_no > MAX_ROUNDS:
        return f"""
        <html><head>{STYLE}</head><body>
            <div class="card bounce-card">
                <div class="skull">💀</div>
                <h1 style="color:red;">GAME OVER</h1>
                <p>You failed to meet all KPIs.</p>
                <a class="button-link" href="/">Try Again</a>
            </div>
        </body></html>
        """

    # ================= CONTINUE SUMMARY =====================
    return f"""
    <html><head>{STYLE}</head><body>

        <div class="card bounce-card">

            <h2>Round {round_no - 1} Summary</h2>

            <p>Profit: ₹{profit}</p>
            <p>Cash: ₹{cash}</p>
            <p>Service: {service}%</p>
            <p>CO₂: {co2}</p>

            <a class="button-link" href="/dashboard">Continue</a>
        </div>

    </body></html>
    """


# END
