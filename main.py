from fastapi import FastAPI
from math import ceil

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/calculate")
def calculate(data: dict):
    
    # 🔹 INPUTS (match your Excel X row)
    length = data.get("length", 0)        # X2
    height = data.get("height", 0)        # X3
    base_outs = data.get("base_outs", 0)  # X7
    ladder_bays = data.get("ladder_bays", 0)  # X9
    guard_ends = data.get("guard_ends", 0)    # X11
    tarp = data.get("tarp", 0)                # X14

    # 🔹 DRIVERS
    square_units = ceil((length * height) / 45.5)
    vertical_units = ceil(height / 6.5)
    linear_units = ceil(length / 7)

    # 🔹 BASE UNIT (partial to start simple)
    base_units = square_units

    # 🔹 END BAY LEG
    end_bay_units = vertical_units * ladder_bays

    # 🔹 BASE OUTS
    base_out_units = linear_units * base_outs

    # 🔹 GUARD RAIL
    guard_units = linear_units

    # 🔹 OUTPUT (temporary — we build this later)
    return {
        "inputs": {
            "length": length,
            "height": height
        },
        "drivers": {
            "square_units": square_units,
            "vertical_units": vertical_units,
            "linear_units": linear_units
        },
        "units": {
            "base_units": base_units,
            "end_bay_units": end_bay_units,
            "base_out_units": base_out_units,
            "guard_units": guard_units
        }
    }
