from fastapi import FastAPI
from math import ceil

app = FastAPI()

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
