from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import math

app = FastAPI()

# =========================
# CORE CALCULATION ENGINE
# =========================

def ceil(x):
    return math.ceil(x)

def calculate_config_a(data):
    X2 = data["length"]
    X3 = data["height"]
    X7 = data.get("base_outs", 0)
    X9 = data.get("ladder_bays", 0)
    X11 = data.get("guard_rail_ends", 0)
    X14 = data.get("tarp", 0)

    equipment = {i: 0 for i in range(24, 50)}
    consumables = 0
    labour_total = 0

    # =========================
    # ACCESS LADDER (AG)
    # =========================
    units_ag = ceil(X3 / 6.5) * X9

    equipment[36] += ceil(units_ag * 1)
    equipment[37] += ceil(units_ag * 1)
    equipment[38] += ceil(units_ag * 1)
    equipment[39] += ceil(units_ag * 1)
    equipment[26] += ceil(units_ag * -1)
    equipment[44] += ceil(units_ag * 1)
    equipment[31] += ceil(units_ag * 1)

    # =========================
    # TIE-INS (AI)
    # =========================
    area_units = (X2 * X3) / 45.5
    vertical_units = X3 / 6.5
    total_units = area_units + vertical_units

    equipment[25] += ceil(total_units * 1)
    equipment[37] += ceil(total_units * 2)

    consumables += ceil(total_units * 1)

    # =========================
    # TARP (AS)
    # =========================
    units_as = (X2 / 7) * X14

    equipment[24] += ceil(units_as / 3)
    equipment[26] += ceil(units_as * 1)
    equipment[25] += ceil(units_as * 1)
    equipment[27] += ceil(units_as * 1)

    # =========================
    # AU BLOCK
    # =========================
    units_au = X14

    equipment[24] += ceil(units_au / 3)
    equipment[46] += ceil(units_au * 1)
    equipment[25] += ceil(units_au * 1)
    equipment[35] += ceil(units_au * 1)

    return {
        "equipment": equipment,
        "consumables": consumables,
        "labour": labour_total
    }

# =========================
# ROUTES
# =========================

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.post("/calculate")
async def calculate(request: Request):
    data = await request.json()
    result = calculate_config_a(data)
    return result
