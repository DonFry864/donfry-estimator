from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

RATES = {
    "3M STANDARDS": 7.14,
    "SL7": 3.79,
    "PFM7": 9.00,
    "SBB7": 5.03,
    "GL": 0.25,
    "EPP7": 7.00,
    "EPP 1.15": 3.50,
    "1.15 SL": 3.01,
    "SBB 1.15": 5.00,
    "PK 5 SILL": 4.00,
    "SBC": 1.40,
    "SJ 18": 3.00,
    "MONARFLEX TARP": 0.50,
}

EQUIPMENT_ORDER = [
    "3M STANDARDS",
    "SL7",
    "PFM7",
    "SBB7",
    "GL",
    "EPP7",
    "EPP 1.15",
    "1.15 SL",
    "SBB 1.15",
    "PK 5 SILL",
    "SBC",
    "SJ 18",
    "MONARFLEX TARP",
]


class Input(BaseModel):
    length: float
    height: float
    g3: float = 1.10
    tarp: int = 0
    end_bay_leg_input: int = 0   # X6
    base_out_input: int = 0      # X7
    base_out_eb_input: int = 0   # X8


def equipment_rental(equipment: dict[str, float]) -> float:
    return round(sum(qty * RATES.get(name, 0.0) for name, qty in equipment.items()), 2)


def combine_equipment(*sections: dict[str, float]) -> dict[str, float]:
    combined = defaultdict(float)
    for section in sections:
        for name, qty in section.items():
            combined[name] += qty
    return dict(combined)


def build_equipment_list(combined_eq: dict[str, float]) -> list[dict]:
    return [
        {"name": name, "qty": round(combined_eq.get(name, 0.0), 6)}
        for name in EQUIPMENT_ORDER
    ]


# -------------------------
# Base Unit
# -------------------------
def base_unit_equipment(length: float, height: float, tarp: int) -> dict[str, float]:
    base_units = (length * height) / 45.5

    return {
        "3M STANDARDS": 4 * base_units / 3,
        "PFM7": 2 * base_units,
        "SL7": 4 * base_units,
        "SBB7": 0.5 * base_units,
        "GL": 1.32 * base_units,
        "EPP7": 1 * base_units,
        "1.15 SL": 1 * base_units,
        "SBB 1.15": 1 * base_units,
        "MONARFLEX TARP": 45.5 * base_units * tarp,
    }


def base_unit_f15(tarp: int) -> float:
    return (
        (4 * 2.38) +
        (2 * 9.00) +
        (4 * 3.79) +
        (0.5 * 5.03) +
        (1.32 * 0.25) +
        (1 * 7.00) +
        (1 * 3.01) +
        ((45.5 * 0.50) * tarp)
    )


def base_unit_g15(tarp: int, g3: float) -> float:
    f15 = base_unit_f15(tarp)
    g16 = 45.5 * 0.25 * tarp
    return (f15 * g3) + g16


def base_unit_labour(length: float, height: float, tarp: int, g3: float) -> float:
    g15 = base_unit_g15(tarp, g3)

    total = 0.0
    remaining_height = height
    first = True

    while remaining_height >= -45.5:
        area = remaining_height * length
        factor = 1.0 if first else 0.7
        row_value = (area / 45.5) * g15 * factor

        if row_value > 0:
            total += row_value

        if first:
            remaining_height -= 19.5
            first = False
        else:
            remaining_height -= 6.5

    return round(total, 2)


# -------------------------
# End Bay Leg
# -------------------------
def end_bay_leg_equipment(height: float, end_bay_leg_input: int, tarp: int) -> dict[str, float]:
    driver = (height / 6.5) * end_bay_leg_input

    return {
        "3M STANDARDS": 4 * driver / 3,
        "SBB7": 1 * driver,
        "GL": 1.32 * driver,
        "EPP 1.15": 2 * driver,
        "1.15 SL": 5 * driver,
        "SBB 1.15": 5 * driver,
        "MONARFLEX TARP": 45.5 * tarp * end_bay_leg_input,
    }


def end_bay_leg_f84(tarp: int) -> float:
    return (
        (4 * 2.38) +             # VM STANDARDS
        (1 * 5.00) +             # SBB 1.15
        (5 * 3.01) +             # 1.15 SL
        (1.32 * 0.25) +          # GL
        (2 * 3.50) +             # EPP 1.15
        (1.32 * 0.25) +          # GL again
        ((45.5 * 0.50) * tarp)   # MONARFLEX TARP
    )


def end_bay_leg_g84(tarp: int, g3: float) -> float:
    f84 = end_bay_leg_f84(tarp)
    return f84 * g3


def end_bay_leg_labour(height: float, end_bay_leg_input: int, tarp: int, g3: float) -> float:
    g84 = end_bay_leg_g84(tarp, g3)
    cost_per_vertical_ft = (end_bay_leg_input * g84) / 6.5

    total = 0.0
    remaining_height = height
    first = True

    while remaining_height >= -45.5:
        factor = 1.0 if first else 0.7
        row_value = cost_per_vertical_ft * remaining_height * factor

        if row_value > 0:
            total += row_value

        if first:
            remaining_height -= 19.5
            first = False
        else:
            remaining_height -= 6.5

    return round(total, 2)


# -------------------------
# Base Out
# -------------------------
def base_out_equipment(base_out_input: int) -> dict[str, float]:
    return {
        "PFM7": 22 * base_out_input,
        "SL7": 22 * base_out_input,
        "1.15 SL": 11 * base_out_input,
        "PK 5 SILL": 11 * base_out_input,
        "SBC": 22 * base_out_input,
        "SJ 18": 22 * base_out_input,
    }


def base_out_labour(length: float, base_out_input: int) -> float:
    return round((length / 7) * 95 * base_out_input, 2)


# -------------------------
# Base Out EB
# -------------------------
def base_out_eb_equipment(base_out_eb_input: int) -> dict[str, float]:
    return {
        "1.15 SL": 1 * base_out_eb_input,
        "PK 5 SILL": 1 * base_out_eb_input,
        "SBC": 2 * base_out_eb_input,
        "SJ 18": 2 * base_out_eb_input,
    }


def base_out_eb_labour(base_out_eb_input: int, g3: float) -> float:
    f144 = (
        (1 * 3.01) +
        (1 * 4.00) +
        (2 * 1.40) +
        (2 * 3.00)
    )
    return round(f144 * g3 * base_out_eb_input, 2)


def build_estimate(data: Input) -> dict:
    base_eq = base_unit_equipment(data.length, data.height, data.tarp)
    ebl_eq = end_bay_leg_equipment(data.height, data.end_bay_leg_input, data.tarp)
    bo_eq = base_out_equipment(data.base_out_input)
    boeb_eq = base_out_eb_equipment(data.base_out_eb_input)

    combined_eq = combine_equipment(base_eq, ebl_eq, bo_eq, boeb_eq)

    base_rental = equipment_rental(base_eq)
    ebl_rental = equipment_rental(ebl_eq)
    bo_rental = equipment_rental(bo_eq)
    boeb_rental = equipment_rental(boeb_eq)

    base_lab = base_unit_labour(data.length, data.height, data.tarp, data.g3)
    ebl_lab = end_bay_leg_labour(data.height, data.end_bay_leg_input, data.tarp, data.g3)
    bo_lab = base_out_labour(data.length, data.base_out_input)
    boeb_lab = base_out_eb_labour(data.base_out_eb_input, data.g3)

    return {
        "inputs": data.model_dump(),
        "equipment_list": build_equipment_list(combined_eq),
        "sections": {
            "base_unit": {
                "rental": round(base_rental, 2),
                "labour": round(base_lab, 2),
            },
            "end_bay_leg": {
                "rental": round(ebl_rental, 2),
                "labour": round(ebl_lab, 2),
            },
            "base_out": {
                "rental": round(bo_rental, 2),
                "labour": round(bo_lab, 2),
            },
            "base_out_eb": {
                "rental": round(boeb_rental, 2),
                "labour": round(boeb_lab, 2),
            },
        },
        "totals": {
            "rental_28_day": round(base_rental + ebl_rental + bo_rental + boeb_rental, 2),
            "erect_labour": round(base_lab + ebl_lab + bo_lab + boeb_lab, 2),
        },
    }


@app.get("/")
def root():
    return {"message": "Estimator API is running"}


@app.post("/calculate")
def calculate(data: Input):
    return build_estimate(data)
