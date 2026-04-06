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

    base_unit_table = {
        "standards": 4,
        "ledgers": 6,
        "transoms": 3,
        "boards": 5
    }

    base_units_result = {}

    for item, qty in base_unit_table.items():
        base_units_result[item] = qty * square_units

    return {
        "drivers": {
            "square_units": square_units,
            "vertical_units": vertical_units,
            "linear_units": linear_units
        },
        "base_units": base_units_result
    }
