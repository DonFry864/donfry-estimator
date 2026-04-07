from fastapi import FastAPI
from pydantic import BaseModel
from math import ceil

# --- BASE UNIT COMPONENTS (B8:G18) ---
BASE_UNIT_COMPONENTS = [
    {"name": "VM STANDARDS", "qty": 4, "rate": 2.38, "labour": 0},
    {"name": "PFM7", "qty": 3, "rate": 9, "labour": 0},
    {"name": "SL7", "qty": 4, "rate": 3.79, "labour": 0},
    {"name": "SBB7", "qty": 0.5, "rate": 5.03, "labour": 0},
    {"name": "GL", "qty": 1.32, "rate": 0.25, "labour": 0},
    {"name": "SBB 1.15", "qty": 0.125, "rate": 1.25, "labour": 0},
    {"name": "1.15 SL", "qty": 1, "rate": 3.01, "labour": 0},
    {"name": "SBKTS 24", "qty": 0, "rate": 0, "labour": 0},
    {"name": "EPP7", "qty": 1, "rate": 7, "labour": 0},
    {"name": "MONARFLEX", "qty": 0, "rate": 0.5, "labour": 0},
]
# --- CALCULATE BASE UNIT RENTAL (F15) ---
def calculate_base_unit_labour(components, g3):
    total = 0

    for c in components:
        labour_rate = c.get("labour", 0)
        qty = c.get("qty", 0)

        total += qty * labour_rate

    return round(total * g3, 2)  # currency
    
app = FastAPI()

class Input(BaseModel):
    length: float
    height: float
    g3: float = 1.10
    base_outs: int
    ladder_bays: int
    guard_ends: int
    tarp: int

@app.post("/calculate")
def calculate(data: Input):

    square_units = ceil((data.length * data.height) / 45.5)
    vertical_units = ceil(data.height / 6.5)
    linear_units = ceil(data.length / 7)

    F15 = calculate_base_unit_labour(BASE_UNIT_COMPONENTS. data.g3)

    return {
        "base_unit_value": F15
        "square_units": square_units,
        "vertical_units": vertical_units,
        "linear_units": linear_units
    }
