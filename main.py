from fastapi import FastAPI
from pydantic import BaseModel
from math import ceil

# --- BASE UNIT COMPONENTS (B8:G18) ---
BASE_UNIT_COMPONENTS = [
    {"name": "VM STANDARDS", "qty": 4, "rate": 2.38},
    {"name": "PFM7", "qty": 3, "rate": 9},
    {"name": "SL7", "qty": 4, "rate": 3.79},
    {"name": "SBB7", "qty": 0.5, "rate": 5.03},
    {"name": "GL", "qty": 1.32, "rate": 0.25},
    {"name": "SBB 1.15", "qty": 0.125, "rate": 1.25},
    {"name": "1.15 SL", "qty": 1, "rate": 3.01},
    {"name": "SBKTS 24", "qty": 0},
    {"name": "EPP7", "qty": 1, "rate": 7},
    {"name": "MONARFLEX", "qty": 0, "rate": 0.5},  # dynamic later
]
# --- CALCULATE BASE UNIT RENTAL (F15) ---
def calculate_base_unit_rental(components):
    total = 0

    for c in components:
        total += c["qty"] * c["rate"]

    return total

app = FastAPI()

class Input(BaseModel):
    length: float
    height: float
    base_outs: int
    ladder_bays: int
    guard_ends: int
    tarp: int

@app.post("/calculate")
def calculate(data: Input):

    square_units = ceil((data.length * data.height) / 45.5)
    vertical_units = ceil(data.height / 6.5)
    linear_units = ceil(data.length / 7)

    F15 = calculate_base_unit_rental(BASE_UNIT_COMPONENTS)

    return {
        "F15": F15,
        "square_units": square_units,
        "vertical_units": vertical_units,
        "linear_units": linear_units
    }
