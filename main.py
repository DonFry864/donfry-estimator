from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


RENTAL_RATES = {
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
    "CTTRA": 2.00,
    "AC10": 20.00,
    "LBB42": 5.00,
    "TRAP DOOR": 10.00,
    "PFM 1.15": 5.00,
    "DL7": 14.50,
    "T8 TUBE": 4.00,
    "T2 TUBE": 1.00,
    "PK8 8'WOOD PLANK": 4.00,
}

CONSUMABLE_RATES = {
    "EYE BOLT": 7.00,
}

LABOUR_RATES = {
    "3M STANDARDS": 2.38,
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
    "CTTRA": 2.00,
    "EYE BOLT": 7.00,
    "AC10": 20.00,
    "LBB42": 5.00,
    "TRAP DOOR": 10.00,
    "PFM 1.15": 5.00,
    "DL7": 4.00,
    "T8 TUBE": 0.00,
    "T2 TUBE": 0.00,
    "PK8 8'WOOD PLANK": 0.00,
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
    "CTTRA",
    "EYE BOLT",
    "AC10",
    "LBB42",
    "TRAP DOOR",
    "PFM 1.15",
    "DL7",
    "T8 TUBE",
    "T2 TUBE",
    "PK8 8'WOOD PLANK",
]


class Input(BaseModel):
    length: float
    height: float
    g3: float = 1.10
    tarp: int = 0
    end_bay_leg_input: int = 0
    base_out_input: int = 0
    base_out_eb_input: int = 0
    access_ladder_input: int = 0
    ladder_bay_input: int = 0
    top_guard_rail_input: int = 0
    top_guard_rail_ends_input: int = 0
    tie_in_input: int = 0
    top_deck_level_input: int = 0


def resolved_access_ladder_input(data: Input) -> int:
    return data.access_ladder_input if data.access_ladder_input else data.ladder_bay_input


def height_engine_total(height: float, cost_per_vertical_ft: float) -> float:
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


def equipment_rental(equipment: dict[str, float]) -> float:
    return round(sum(qty * RENTAL_RATES.get(name, 0.0) for name, qty in equipment.items()), 2)


def equipment_consumables(equipment: dict[str, float]) -> float:
    return round(sum(qty * CONSUMABLE_RATES.get(name, 0.0) for name, qty in equipment.items()), 2)


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


def make_section(equipment: dict[str, float], labour: float) -> dict:
    return {
        "equipment": equipment,
        "rental": equipment_rental(equipment),
        "consumables": equipment_consumables(equipment),
        "labour": round(labour, 2),
    }


def apply_erect_minimum(erect_labour: float) -> float:
    return max(3040.0, erect_labour)


def apply_dismantle_minimum(dismantle_labour: float) -> float:
    return max(2120.0, dismantle_labour)


def engineering_fee(height: float) -> float:
    return 1650.0 if height > 49 else 0.0


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


def base_unit_labour(length: float, height: float, tarp: int, g3: float) -> float:
    f15 = (
        4 * LABOUR_RATES["3M STANDARDS"] +
        2 * LABOUR_RATES["PFM7"] +
        4 * LABOUR_RATES["SL7"] +
        0.5 * LABOUR_RATES["SBB7"] +
        1.32 * LABOUR_RATES["GL"] +
        1 * LABOUR_RATES["EPP7"] +
        1 * LABOUR_RATES["1.15 SL"] +
        (45.5 * LABOUR_RATES["MONARFLEX TARP"] * tarp)
    )
    g16 = 45.5 * 0.25 * tarp
    g15 = (f15 * g3) + g16

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
def end_bay_leg_units(height: float, end_bay_leg_input: int) -> float:
    return (height / 6.5) * end_bay_leg_input


def end_bay_leg_equipment(height: float, end_bay_leg_input: int, tarp: int) -> dict[str, float]:
    units = end_bay_leg_units(height, end_bay_leg_input)
    return {
        "3M STANDARDS": (4 / 3) * units,
        "SBB7": 1 * units,
        "GL": 1.32 * units,
        "EPP 1.15": 2 * units,
        "1.15 SL": 5 * units,
        "SBB 1.15": 5 * units,
        "MONARFLEX TARP": height * tarp * end_bay_leg_input,
    }


def end_bay_leg_labour(height: float, end_bay_leg_input: int, tarp: int, g3: float) -> float:
    # Sheet-locked labour recipe:
    # 4 VM STANDARDS, 1 SBB 1.15, 5 1.15 SL, 1.32 GL, 2 EPP 1.15, 1.32 GL, 45.5 tarp
    f84 = (
        4 * LABOUR_RATES["3M STANDARDS"] +
        1 * LABOUR_RATES["SBB 1.15"] +
        5 * LABOUR_RATES["1.15 SL"] +
        1.32 * LABOUR_RATES["GL"] +
        2 * LABOUR_RATES["EPP 1.15"] +
        1.32 * LABOUR_RATES["GL"] +
        45.5 * LABOUR_RATES["MONARFLEX TARP"] * tarp
    )
    g84 = f84 * g3
    units = end_bay_leg_units(height, end_bay_leg_input)
    cost_per_vertical_ft = (units * g84) / height
    return height_engine_total(height, cost_per_vertical_ft)


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
        1 * LABOUR_RATES["1.15 SL"] +
        1 * LABOUR_RATES["PK 5 SILL"] +
        2 * LABOUR_RATES["SBC"] +
        2 * LABOUR_RATES["SJ 18"]
    )
    return round(f144 * g3 * base_out_eb_input, 2)


# -------------------------
# Access Ladder
# -------------------------
def access_ladder_units(height: float, access_ladder_input: int) -> float:
    return (height / 6.5) * access_ladder_input


def access_ladder_equipment(height: float, access_ladder_input: int) -> dict[str, float]:
    units = access_ladder_units(height, access_ladder_input)

    return {
        "1.15 SL": 1 * units,
        "AC10": 1 * units,
        "CTTRA": 2 * units,
        "LBB42": 1 * units,
        "TRAP DOOR": 1 * units,
        "PFM 1.15": 1 * units,
    }


def access_ladder_labour(height: float, access_ladder_input: int, g3: float) -> float:
    # Sheet-locked base labour driver:
    # result in sheet is 39.05 at g3 = 1.10
    f153 = 35.5
    g155 = f153 * g3

    units = access_ladder_units(height, access_ladder_input)
    cost_per_vertical_ft = (units * g155) / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Tie In
# -------------------------
def tie_in_locations(length: float, height: float, tie_in_input: int) -> float:
    base_units = (length * height) / 45.5
    return ((base_units / 2) + (height / 13)) * tie_in_input


def tie_in_equipment(length: float, height: float, tie_in_input: int) -> dict[str, float]:
    locations = tie_in_locations(length, height, tie_in_input)
    return {
        "CTTRA": 2 * locations,
        "SL7": locations,
        "EYE BOLT": locations,
    }


def tie_in_labour(length: float, height: float, tie_in_input: int, g3: float) -> float:
    locations = tie_in_locations(length, height, tie_in_input)

    if height <= 0:
        return 0.0

    f_tie = 20.0
    g_tie = f_tie * g3
    cost_per_vertical_ft = (locations * g_tie) / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Top Guard Rail
# -------------------------
def top_guard_rail_equipment(length: float, top_guard_rail_input: int) -> dict[str, float]:
    runs = length / 7
    driver = runs * top_guard_rail_input

    return {
        "3M STANDARDS": driver / 3,
        "SL7": 2 * driver,
        "EPP7": 1 * driver,
        "GL": 0.33 * driver,
    }


def top_guard_rail_labour(length: float, height: float, top_guard_rail_input: int, g3: float) -> float:
    bays = (length / 7) * top_guard_rail_input

    f_top_gr = (
        1 * LABOUR_RATES["3M STANDARDS"] +
        2 * LABOUR_RATES["SL7"] +
        1 * LABOUR_RATES["EPP7"] +
        0.33 * LABOUR_RATES["GL"]
    )
    g_top_gr = f_top_gr * g3

    if height <= 0:
        return 0.0

    cost_per_vertical_ft = (bays * g_top_gr) / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Top Guard Rail Ends
# -------------------------
def top_guard_rail_ends_units(top_guard_rail_ends_input: int) -> float:
    return float(top_guard_rail_ends_input)


def top_guard_rail_ends_equipment(top_guard_rail_ends_input: int) -> dict[str, float]:
    units = top_guard_rail_ends_units(top_guard_rail_ends_input)

    return {
        "3M STANDARDS": 1 * units,
        "1.15 SL": 4 * units,
        "EPP 1.15": 2 * units,
        "GL": 1 * units,
    }


def top_guard_rail_ends_labour(height: float, top_guard_rail_ends_input: int, g3: float) -> float:
    units = top_guard_rail_ends_units(top_guard_rail_ends_input)

    f_top_gr_ends = (
        3 * LABOUR_RATES["3M STANDARDS"] +
        4 * LABOUR_RATES["1.15 SL"] +
        2 * LABOUR_RATES["EPP 1.15"] +
        1 * LABOUR_RATES["GL"]
    )
    g_top_gr_ends = f_top_gr_ends * g3

    if height <= 0:
        return 0.0

    cost_per_vertical_ft = (units * g_top_gr_ends) / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Tarp & Canopy
# -------------------------
def tarp_canopy_runs(length: float, tarp: int) -> float:
    return (length / 7) * tarp


def tarp_canopy_base_ties(length: float, height: float, tarp: int) -> float:
    return ((length * height) / 91) * tarp


def tarp_canopy_end_bay_ties(height: float, tarp: int) -> float:
    return (height / 13) * tarp


def tarp_canopy_equipment(length: float, height: float, tarp: int) -> dict[str, float]:
    runs = (length / 7) * tarp
    base_ties = ((length * height) / 91) * tarp
    end_bay_ties = (height / 13) * tarp

    return {
        "3M STANDARDS": (4 / 3) * runs,
        "PFM7": 4 * runs,
        "DL7": 1 * runs,
        "SL7": base_ties + (4 * runs) + end_bay_ties,
        "SBB7": 3 * runs,
        "T8 TUBE": 1 * runs,
        "CTTRA": (((length * height) / 91) + (height / 13)) * 2 * tarp + ((length / 7) * 2 * tarp),
        "SBC": 1.4 * runs,
        "SJ 18": 1 * runs,
        "MONARFLEX TARP": 150 * runs,
        "T2 TUBE": 1 * runs,
        "PK8 8'WOOD PLANK": 2 * runs,
        "EYE BOLT": base_ties + (4 * runs) + end_bay_ties,
    }
    return {
        "3M STANDARDS": (4 / 3) * runs,
        "PFM7": 4 * runs,
        "DL7": 1 * runs,
        "SL7": sl7_qty,
        "SBB7": 3 * runs,
        "T8 TUBE": 1 * runs,
        "CTTRA": cttra_qty,
        "SBC": 1.4 * runs,
        "SJ 18": 2 * runs,
        "MONARFLEX TARP": 150 * runs,
        "PK8 8'WOOD PLANK": 2 * runs,
        "EYE BOLT": eye_bolt_qty,
    }


def tarp_canopy_labour(length: float, height: float, tarp: int) -> float:
    if height <= 0 or tarp <= 0:
        return 0.0

    # Sheet logic:
    # =SUM(X2/7 * G232)
    top_driver = (length / 7) * (150 * tarp)
    cost_per_vertical_ft = top_driver / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Tarp & Canopy End Bay
# -------------------------
def tarp_canopy_end_bay_equipment(tarp: int) -> dict[str, float]:
    driver = float(tarp)

    return {
        "3M STANDARDS": (2 / 3) * driver,
        "DL7": 1 * driver,
        "SL7": 6 * driver,
        "SJ 18": 1 * driver,
        "SBC": 1 * driver,
        "CTTRA": 2 * driver,
        "MONARFLEX TARP": 300 * driver,
        "T8 TUBE": 1 * driver,
        "T2 TUBE": 2 * driver,
    }


def tarp_canopy_end_bay_labour(height: float, tarp: int, g3: float) -> float:
    f_tceb = (
        2 * LABOUR_RATES["3M STANDARDS"] +
        1 * LABOUR_RATES["DL7"] +
        6 * LABOUR_RATES["SL7"] +
        1 * LABOUR_RATES["SJ 18"] +
        1 * LABOUR_RATES["SBC"] +
        1 * LABOUR_RATES["T8 TUBE"] +
        2 * LABOUR_RATES["CTTRA"] +
        2 * LABOUR_RATES["T2 TUBE"] +
        300 * LABOUR_RATES["MONARFLEX TARP"]
    )

    g_tceb = f_tceb * g3

    if height <= 0:
        return 0.0

    cost_per_vertical_ft = (tarp * g_tceb) / height
    return height_engine_total(height, cost_per_vertical_ft)


# -------------------------
# Future Repeatable Units
# -------------------------
def vertical_repeatable_equipment() -> dict[str, float]:
    return {}


def vertical_repeatable_labour() -> float:
    return 0.0


def horizontal_repeatable_equipment() -> dict[str, float]:
    return {}


def horizontal_repeatable_labour() -> float:
    return 0.0


def build_estimate(data: Input) -> dict:
    sections = {}
    ladder_input = resolved_access_ladder_input(data)

    base_eq = base_unit_equipment(data.length, data.height, data.tarp)
    sections["base_unit"] = make_section(
        base_eq,
        base_unit_labour(data.length, data.height, data.tarp, data.g3),
    )

    ebl_eq = end_bay_leg_equipment(data.height, data.end_bay_leg_input, data.tarp)
    sections["end_bay_leg"] = make_section(
        ebl_eq,
        end_bay_leg_labour(data.height, data.end_bay_leg_input, data.tarp, data.g3),
    )

    bo_eq = base_out_equipment(data.base_out_input)
    sections["base_out"] = make_section(
        bo_eq,
        base_out_labour(data.length, data.base_out_input),
    )

    boeb_eq = base_out_eb_equipment(data.base_out_eb_input)
    sections["base_out_eb"] = make_section(
        boeb_eq,
        base_out_eb_labour(data.base_out_eb_input, data.g3),
    )

    al_eq = access_ladder_equipment(data.height, ladder_input)
    sections["access_ladder"] = make_section(
        al_eq,
        access_ladder_labour(data.height, ladder_input, data.g3),
    )

    tie_eq = tie_in_equipment(data.length, data.height, data.tie_in_input)
    sections["tie_in"] = make_section(
        tie_eq,
        tie_in_labour(data.length, data.height, data.tie_in_input, data.g3),
    )

    top_gr_eq = top_guard_rail_equipment(data.length, data.top_guard_rail_input)
    sections["top_guard_rail"] = make_section(
        top_gr_eq,
        top_guard_rail_labour(data.length, data.height, data.top_guard_rail_input, data.g3),
    )

    top_gr_ends_eq = top_guard_rail_ends_equipment(data.top_guard_rail_ends_input)
    sections["top_guard_rail_ends"] = make_section(
        top_gr_ends_eq,
        top_guard_rail_ends_labour(data.height, data.top_guard_rail_ends_input, data.g3),
    )

    tarp_ca_eq = tarp_canopy_equipment(data.length, data.height, data.tarp)
    sections["tarp_canopy"] = make_section(
        tarp_ca_eq,
        tarp_canopy_labour(data.length, data.height, data.tarp),
    )

    tceb_eq = tarp_canopy_end_bay_equipment(data.tarp)
    sections["tarp_canopy_end_bay"] = make_section(
        tceb_eq,
        tarp_canopy_end_bay_labour(data.height, data.tarp, data.g3),
    )

    vr_eq = vertical_repeatable_equipment()
    sections["vertical_repeatable"] = make_section(
        vr_eq,
        vertical_repeatable_labour(),
    )

    hr_eq = horizontal_repeatable_equipment()
    sections["horizontal_repeatable"] = make_section(
        hr_eq,
        horizontal_repeatable_labour(),
    )

    combined_eq = combine_equipment(*(section["equipment"] for section in sections.values()))

    total_rental = round(sum(section["rental"] for section in sections.values()), 2)
    total_consumables = round(sum(section["consumables"] for section in sections.values()), 2)
    total_labour = round(sum(section["labour"] for section in sections.values()), 2)

    erect_labour_min_applied = apply_erect_minimum(total_labour)
    dismantle_labour_raw = round(total_labour * 0.70, 2)
    dismantle_labour_min_applied = apply_dismantle_minimum(dismantle_labour_raw)
    engineering = engineering_fee(data.height)

    response_inputs = data.model_dump()
    response_inputs["access_ladder_input_resolved"] = ladder_input

    return {
        "inputs": response_inputs,
        "equipment_list": build_equipment_list(combined_eq),
        "sections": {
            name: {
                "rental": section["rental"],
                "consumables": section["consumables"],
                "labour": section["labour"],
            }
            for name, section in sections.items()
        },
        "totals": {
            "rental_28_day": total_rental,
            "consumables": total_consumables,
            "erect_labour_raw": total_labour,
            "erect_labour_min_applied": erect_labour_min_applied,
            "dismantle_labour_raw": dismantle_labour_raw,
            "dismantle_labour_min_applied": dismantle_labour_min_applied,
            "engineering_fee": engineering,
        },
    }


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/calculate")
def calculate(data: Input):
    return build_estimate(data)
