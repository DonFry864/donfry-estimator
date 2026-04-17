from collections import defaultdict
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


CONFIG_METADATA = {
    "A": {
        "code": "A",
        "name": "Stucco 4' No Setback Full Deck",
        "description": "Full deck scaffold configuration with 4' no setback layout.",
        "image": "/static/config-a.png",
    },
    "B": {
        "code": "B",
        "name": "Config B",
        "description": "Alternate scaffold configuration.",
        "image": "/static/config-b.png",
    },
    "C": {
        "code": "C",
        "name": "Config C",
        "description": "5-foot ledger variant with side brackets.",
        "image": "/static/config-c.png",
    },
    "D": {
        "code": "D",
        "name": "Config D",
        "description": "5-foot diagonal variant with side brackets.",
        "image": "/static/config-d.png",
    },
    "F": {
        "code": "F",
        "name": "Config F",
        "description": "Reduced base recipe using 1.15 family.",
        "image": "/static/config-f.png",
    },
    "G": {
        "code": "G",
        "name": "Config G",
        "description": "Reduced base recipe with paired deck level repeatable units.",
        "image": "/static/config-g.png",
    },
    "H": {
        "code": "H",
        "name": "Config H",
        "description": "5-foot ledger reduced recipe with paired deck level repeatable units.",
        "image": "/static/config-h.png",
    },
    "I": {
        "code": "I",
        "name": "Config I",
        "description": "5-foot diagonal reduced recipe with paired deck level repeatable units.",
        "image": "/static/config-i.png",
    },
}


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
    'sbkts 24"': 4.62,
    'SL 24"': 2.50,
    'EPP 24"': 3.50,
    "SL5": 3.36,
    "SBB5": 5.00,
    "DL5": 10.50,
    "EPP5": 3.50,
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
    'sbkts 24"': 4.62,
    'SL 24"': 2.50,
    'EPP 24"': 3.50,
    "SL5": 3.36,
    "SBB5": 5.00,
    "DL5": 10.50,
    "EPP5": 3.50,
    "PK 5 SILL": 4.00,
    "SBC": 1.40,
    "SJ 18": 3.00,
    "MONARFLEX TARP": 0.50,
    "EYE BOLT": 7.00,
    "CTTRA": 2.00,
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
    'sbkts 24"',
    'SL 24"',
    'EPP 24"',
    "SL5",
    "SBB5",
    "DL5",
    "EPP5",
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


STANDARD_CONFIGS = {"A", "B", "C", "D", "F", "G", "H", "I"}
DECK_LEVEL_CONFIGS = {"G", "H", "I"}


class Input(BaseModel):
    config: str = "A"
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
    deck_level_end_bay_input: int = 0


BASE_UNIT_RECIPES = {
    "A": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "2 * base_units"},
        {"name": "SL7", "expr": "4 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "EPP7", "expr": "1 * base_units"},
        {"name": "1.15 SL", "expr": "1 * base_units"},
        {"name": "SBB 1.15", "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "B": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "3 * base_units"},
        {"name": "SL7", "expr": "4 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.5 * base_units"},
        {"name": "1.15 SL", "expr": "1 * base_units"},
        {"name": 'sbkts 24"', "expr": "1 * base_units"},
        {"name": "EPP7", "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "C": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "4 * base_units"},
        {"name": "SL7", "expr": "4 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "SL5", "expr": "1 * base_units"},
        {"name": 'sbkts 24"', "expr": "1 * base_units"},
        {"name": "EPP7", "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "D": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "4 * base_units"},
        {"name": "SL7", "expr": "4 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "DL5", "expr": "1 * base_units"},
        {"name": "EPP7", "expr": "1 * base_units"},
        {"name": 'sbkts 24"', "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "F": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "1 * base_units"},
        {"name": "SL7", "expr": "2 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "1.15 SL", "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "G": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "1 * base_units"},
        {"name": "SL7", "expr": "2 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "1.15 SL", "expr": "1 * base_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * base_units * tarp"},
    ],
    "H": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "1 * base_units"},
        {"name": "SL7", "expr": "2 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "SL5", "expr": "1 * base_units"},
    ],
    "I": [
        {"name": "3M STANDARDS", "expr": "(4/3) * base_units"},
        {"name": "PFM7", "expr": "1 * base_units"},
        {"name": "SL7", "expr": "2 * base_units"},
        {"name": "SBB7", "expr": "0.5 * base_units"},
        {"name": "GL", "expr": "1.32 * base_units"},
        {"name": "SBB 1.15", "expr": "0.125 * base_units"},
        {"name": "DL5", "expr": "1 * base_units"},
    ],
}


BASE_UNIT_LABOUR_RECIPES = {
    "A": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 2},
        {"name": "SL7", "qty": 4},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "EPP7", "qty": 1},
        {"name": "1.15 SL", "qty": 1},
        {"name": "SBB 1.15", "qty": 1},
    ],
    "B": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 3},
        {"name": "SL7", "qty": 4},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "EPP7", "qty": 1},
        {"name": "1.15 SL", "qty": 1},
        {"name": "SBB 1.15", "qty": 0.5},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "C": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 4},
        {"name": "SL7", "qty": 4},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "SL5", "qty": 1},
        {"name": 'sbkts 24"', "qty": 1},
        {"name": "EPP7", "qty": 1},
    ],
    "D": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 4},
        {"name": "SL7", "qty": 4},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "DL5", "qty": 1},
        {"name": 'sbkts 24"', "qty": 1},
        {"name": "EPP7", "qty": 1},
    ],
    "F": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 1},
        {"name": "SL7", "qty": 2},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "1.15 SL", "qty": 1},
    ],
    "G": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 1},
        {"name": "SL7", "qty": 2},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "1.15 SL", "qty": 1},
    ],
    "H": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 1},
        {"name": "SL7", "qty": 2},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "SL5", "qty": 1},
    ],
    "I": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "PFM7", "qty": 1},
        {"name": "SL7", "qty": 2},
        {"name": "SBB7", "qty": 0.5},
        {"name": "GL", "qty": 1.32},
        {"name": "SBB 1.15", "qty": 0.125},
        {"name": "DL5", "qty": 1},
    ],
}

END_BAY_LEG_LABOUR_RECIPES = {
    "A": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB 1.15", "qty": 1},
        {"name": "1.15 SL", "qty": 5},
        {"name": "GL", "qty": 1.32},
        {"name": "EPP 1.15", "qty": 2},
    ],
    "B": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB 1.15", "qty": 1},
        {"name": "1.15 SL", "qty": 4},
        {"name": "GL", "qty": 1.32},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "C": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB5", "qty": 1},
        {"name": "SL5", "qty": 4},
        {"name": "GL", "qty": 1.32},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "D": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB5", "qty": 1},
        {"name": "SL5", "qty": 4},
        {"name": "GL", "qty": 1.32},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "F": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB 1.15", "qty": 1},
        {"name": "1.15 SL", "qty": 1},
        {"name": "GL", "qty": 1.32},
    ],
    "G": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB 1.15", "qty": 1},
        {"name": "1.15 SL", "qty": 1},
        {"name": "GL", "qty": 1.32},
    ],
    "H": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB5", "qty": 1},
        {"name": "SL5", "qty": 1},
        {"name": "GL", "qty": 1.32},
    ],
    "I": [
        {"name": "3M STANDARDS", "qty": 4},
        {"name": "SBB5", "qty": 1},
        {"name": "DL5", "qty": 1},
        {"name": "GL", "qty": 1.32},
    ],
}


END_BAY_LEG_RECIPES = {
    "A": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB 1.15", "expr": "1 * end_bay_units"},
        {"name": "1.15 SL", "expr": "5 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
        {"name": "EPP 1.15", "expr": "2 * end_bay_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * end_bay_units * tarp"},
    ],
    "B": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB 1.15", "expr": "1 * end_bay_units"},
        {"name": "1.15 SL", "expr": "4 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
        {"name": 'sbkts 24"', "expr": "1 * end_bay_units"},
        {"name": 'SL 24"', "expr": "4 * end_bay_units"},
        {"name": 'EPP 24"', "expr": "2 * end_bay_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * end_bay_units * tarp"},
    ],
    "C": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB5", "expr": "1 * end_bay_units"},
        {"name": "SL5", "expr": "4 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
        {"name": 'SL 24"', "expr": "4 * end_bay_units"},
        {"name": 'EPP 24"', "expr": "2 * end_bay_units"},
        {"name": 'sbkts 24"', "expr": "1 * end_bay_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * end_bay_units * tarp"},
    ],
    "D": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB5", "expr": "1 * end_bay_units"},
        {"name": "SL5", "expr": "4 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
        {"name": 'SL 24"', "expr": "4 * end_bay_units"},
        {"name": 'EPP 24"', "expr": "2 * end_bay_units"},
        {"name": 'sbkts 24"', "expr": "1 * end_bay_units"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * end_bay_units * tarp"},
    ],
    "F": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB 1.15", "expr": "1 * end_bay_units"},
        {"name": "1.15 SL", "expr": "1 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
    ],
    "G": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB 1.15", "expr": "1 * end_bay_units"},
        {"name": "1.15 SL", "expr": "1 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
    ],
    "H": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB5", "expr": "1 * end_bay_units"},
        {"name": "SL5", "expr": "1 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
    ],
    "I": [
        {"name": "3M STANDARDS", "expr": "(4/3) * end_bay_units"},
        {"name": "SBB5", "expr": "1 * end_bay_units"},
        {"name": "DL5", "expr": "1 * end_bay_units"},
        {"name": "GL", "expr": "1.32 * end_bay_units"},
    ],
}


DECK_LEVEL_RECIPES = {
    "G": [
        {"name": "PFM7", "expr": "3 * deck_level_runs"},
        {"name": "SL7", "expr": "2 * deck_level_runs"},
        {"name": "EPP7", "expr": "1 * deck_level_runs"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_runs"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_runs * tarp"},
    ],
    "H": [
        {"name": "PFM7", "expr": "4 * deck_level_runs"},
        {"name": "SL7", "expr": "2 * deck_level_runs"},
        {"name": "EPP7", "expr": "1 * deck_level_runs"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_runs"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_runs * tarp"},
    ],
    "I": [
        {"name": "PFM7", "expr": "4 * deck_level_runs"},
        {"name": "SL7", "expr": "2 * deck_level_runs"},
        {"name": "EPP7", "expr": "1 * deck_level_runs"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_runs"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_runs * tarp"},
    ],
}


DECK_LEVEL_END_BAY_RECIPES = {
    "G": [
        {"name": "1.15 SL", "expr": "4 * deck_level_end_bay_input"},
        {"name": "EPP 1.15", "expr": "2 * deck_level_end_bay_input"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_end_bay_input"},
        {"name": 'SL 24"', "expr": "4 * deck_level_end_bay_input"},
        {"name": 'EPP 24"', "expr": "2 * deck_level_end_bay_input"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_end_bay_input * tarp"},
    ],
    "H": [
        {"name": "SL5", "expr": "4 * deck_level_end_bay_input"},
        {"name": "EPP5", "expr": "2 * deck_level_end_bay_input"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_end_bay_input"},
        {"name": 'SL 24"', "expr": "4 * deck_level_end_bay_input"},
        {"name": 'EPP 24"', "expr": "2 * deck_level_end_bay_input"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_end_bay_input * tarp"},
    ],
    "I": [
        {"name": "DL5", "expr": "4 * deck_level_end_bay_input"},
        {"name": "EPP5", "expr": "2 * deck_level_end_bay_input"},
        {"name": 'sbkts 24"', "expr": "1 * deck_level_end_bay_input"},
        {"name": 'SL 24"', "expr": "4 * deck_level_end_bay_input"},
        {"name": 'EPP 24"', "expr": "2 * deck_level_end_bay_input"},
        {"name": "MONARFLEX TARP", "expr": "45.5 * deck_level_end_bay_input * tarp"},
    ],
}


DECK_LEVEL_LABOUR_RECIPES = {
    "G": [
        {"name": "PFM7", "qty": 3},
        {"name": "SL7", "qty": 2},
        {"name": "EPP7", "qty": 1},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "H": [
        {"name": "PFM7", "qty": 4},
        {"name": "SL7", "qty": 2},
        {"name": "EPP7", "qty": 1},
        {"name": 'sbkts 24"', "qty": 1},
    ],
    "I": [
        {"name": "PFM7", "qty": 4},
        {"name": "SL7", "qty": 2},
        {"name": "EPP7", "qty": 1},
        {"name": 'sbkts 24"', "qty": 1},
    ],
}

DECK_LEVEL_END_BAY_LABOUR_RECIPES = {
    "G": [
        {"name": "1.15 SL", "qty": 4},
        {"name": "EPP 1.15", "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
    ],
    "H": [
        {"name": "SL5", "qty": 4},
        {"name": "EPP5", "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
    ],
    "I": [
        {"name": "DL5", "qty": 4},
        {"name": "EPP5", "qty": 2},
        {"name": 'sbkts 24"', "qty": 1},
        {"name": 'SL 24"', "qty": 4},
        {"name": 'EPP 24"', "qty": 2},
    ],
}


SECTION_ORDER = [
    "base_unit",
    "end_bay_leg",
    "base_out",
    "base_out_eb",
    "access_ladder",
    "tie_in",
    "top_guard_rail",
    "top_guard_rail_ends",
    "deck_level",
    "deck_level_end_bay",
    "tarp_canopy",
    "tarp_canopy_end_bay",
]


def resolved_access_ladder_input(data: Input) -> int:
    return data.access_ladder_input if data.access_ladder_input else data.ladder_bay_input


def build_context(data: Input) -> dict:
    ladder_input = resolved_access_ladder_input(data)
    return {
        "length": data.length,
        "height": data.height,
        "g3": data.g3,
        "tarp": data.tarp,
        "end_bay_leg_input": data.end_bay_leg_input,
        "base_out_input": data.base_out_input,
        "base_out_eb_input": data.base_out_eb_input,
        "access_ladder_input": ladder_input,
        "tie_in_input": data.tie_in_input,
        "top_guard_rail_input": data.top_guard_rail_input,
        "top_guard_rail_ends_input": data.top_guard_rail_ends_input,
        "top_deck_level_input": data.top_deck_level_input,
        "deck_level_end_bay_input": data.deck_level_end_bay_input,
        "base_units": (data.length * data.height) / 45.5,
        "end_bay_units": (data.height / 6.5) * data.end_bay_leg_input,
        "deck_level_runs": (data.length / 7.0) * data.top_deck_level_input,
    }


def eval_expr(expr: str, context: dict) -> float:
    return float(eval(expr, {"__builtins__": {}}, context))


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


def run_equipment_recipe(recipe: list[dict], context: dict) -> dict[str, float]:
    equipment: dict[str, float] = {}
    for line in recipe:
        qty = eval_expr(line["expr"], context)
        if abs(qty) > 1e-12:
            equipment[line["name"]] = equipment.get(line["name"], 0.0) + qty
    return equipment


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


def recipe_qty_sum(recipe: list[dict]) -> float:
    total = 0.0
    for line in recipe:
        total += line["qty"] * LABOUR_RATES.get(line["name"], 0.0)
    return total


def labour_base_unit(config: str, context: dict) -> float:
    f15 = recipe_qty_sum(BASE_UNIT_LABOUR_RECIPES[config])
    g16 = 45.5 * LABOUR_RATES["MONARFLEX TARP"] * context["tarp"]
    g15 = (f15 * context["g3"]) + g16

    total = 0.0
    remaining_height = context["height"]
    first = True

    while remaining_height >= -45.5:
        area = remaining_height * context["length"]
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


def labour_end_bay_leg(config: str, context: dict) -> float:
    if context["height"] <= 0:
        return 0.0

    f84 = recipe_qty_sum(END_BAY_LEG_LABOUR_RECIPES[config])
    f84 += 45.5 * LABOUR_RATES["MONARFLEX TARP"] * context["tarp"]

    g84 = f84 * context["g3"]
    units = context["end_bay_units"]
    cost_per_vertical_ft = (units * g84) / context["height"]

    return height_engine_total(context["height"], cost_per_vertical_ft)


def labour_deck_level(config: str, context: dict) -> float:
    if config not in DECK_LEVEL_CONFIGS or context["top_deck_level_input"] <= 0 or context["height"] <= 0:
        return 0.0

    f_deck = recipe_qty_sum(DECK_LEVEL_LABOUR_RECIPES[config])
    f_deck += 45.5 * LABOUR_RATES["MONARFLEX TARP"] * context["tarp"]

    g_deck = f_deck * context["g3"]
    cost_per_vertical_ft = (context["deck_level_runs"] * g_deck) / context["height"]
    return height_engine_total(context["height"], cost_per_vertical_ft)


def labour_deck_level_end_bay(config: str, context: dict) -> float:
    if config not in DECK_LEVEL_CONFIGS or context["deck_level_end_bay_input"] <= 0 or context["height"] <= 0:
        return 0.0

    f_deck_eb = recipe_qty_sum(DECK_LEVEL_END_BAY_LABOUR_RECIPES[config])
    f_deck_eb += 45.5 * LABOUR_RATES["MONARFLEX TARP"] * context["tarp"]

    g_deck_eb = f_deck_eb * context["g3"]
    cost_per_vertical_ft = (context["deck_level_end_bay_input"] * g_deck_eb) / context["height"]
    return height_engine_total(context["height"], cost_per_vertical_ft)


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


def base_out_eb_equipment(base_out_eb_input: int) -> dict[str, float]:
    return {
        "1.15 SL": 1 * base_out_eb_input,
        "PK 5 SILL": 1 * base_out_eb_input,
        "SBC": 2 * base_out_eb_input,
        "SJ 18": 2 * base_out_eb_input,
    }


def base_out_eb_labour(base_out_eb_input: int, g3: float) -> float:
    f144 = (
        1 * LABOUR_RATES["1.15 SL"]
        + 1 * LABOUR_RATES["PK 5 SILL"]
        + 2 * LABOUR_RATES["SBC"]
        + 2 * LABOUR_RATES["SJ 18"]
    )
    return round(f144 * g3 * base_out_eb_input, 2)


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
    f153 = 35.5
    g155 = f153 * g3
    units = access_ladder_units(height, access_ladder_input)
    if height <= 0:
        return 0.0
    cost_per_vertical_ft = (units * g155) / height
    return height_engine_total(height, cost_per_vertical_ft)


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
        1 * LABOUR_RATES["3M STANDARDS"]
        + 2 * LABOUR_RATES["SL7"]
        + 1 * LABOUR_RATES["EPP7"]
        + 0.33 * LABOUR_RATES["GL"]
    )
    g_top_gr = f_top_gr * g3
    if height <= 0:
        return 0.0
    cost_per_vertical_ft = (bays * g_top_gr) / height
    return height_engine_total(height, cost_per_vertical_ft)


def top_guard_rail_ends_equipment(top_guard_rail_ends_input: int) -> dict[str, float]:
    units = float(top_guard_rail_ends_input)
    return {
        "3M STANDARDS": 1 * units,
        "1.15 SL": 4 * units,
        "EPP 1.15": 2 * units,
        "GL": 1 * units,
    }


def top_guard_rail_ends_labour(height: float, top_guard_rail_ends_input: int, g3: float) -> float:
    units = float(top_guard_rail_ends_input)
    f_top_gr_ends = (
        3 * LABOUR_RATES["3M STANDARDS"]
        + 4 * LABOUR_RATES["1.15 SL"]
        + 2 * LABOUR_RATES["EPP 1.15"]
        + 1 * LABOUR_RATES["GL"]
    )
    g_top_gr_ends = f_top_gr_ends * g3
    if height <= 0:
        return 0.0
    cost_per_vertical_ft = (units * g_top_gr_ends) / height
    return height_engine_total(height, cost_per_vertical_ft)


def tarp_canopy_runs(length: float, tarp: int) -> float:
    return (length / 7) * tarp


def tarp_canopy_base_ties(length: float, height: float, tarp: int) -> float:
    return ((length * height) / 91) * tarp


def tarp_canopy_end_bay_ties(height: float, tarp: int) -> float:
    return (height / 13) * tarp


def tarp_canopy_equipment(length: float, height: float, tarp: int) -> dict[str, float]:
    runs = tarp_canopy_runs(length, tarp)
    base_ties = tarp_canopy_base_ties(length, height, tarp)
    end_bay_ties = tarp_canopy_end_bay_ties(height, tarp)
    sl7_qty = base_ties + (4 * runs) + end_bay_ties
    cttra_qty = ((((length * height) / 91) + (height / 13)) * 2 * tarp) + ((length / 7) * 2 * tarp)
    eye_bolt_qty = sl7_qty
    return {
        "3M STANDARDS": (4 / 3) * runs,
        "PFM7": 4 * runs,
        "DL7": 1 * runs,
        "SL7": sl7_qty,
        "SBB7": 3 * runs,
        "T8 TUBE": 1 * runs,
        "CTTRA": cttra_qty,
        "SBC": 1.4 * runs,
        "SJ 18": 1 * runs,
        "MONARFLEX TARP": 150 * runs,
        "T2 TUBE": 1 * runs,
        "PK8 8'WOOD PLANK": 2 * runs,
        "EYE BOLT": eye_bolt_qty,
    }


def tarp_canopy_labour(length: float, height: float, tarp: int) -> float:
    if height <= 0 or tarp <= 0:
        return 0.0
    top_driver = (length / 7) * (150 * tarp)
    cost_per_vertical_ft = top_driver / height
    return height_engine_total(height, cost_per_vertical_ft)


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
        2 * LABOUR_RATES["3M STANDARDS"]
        + 1 * LABOUR_RATES["DL7"]
        + 6 * LABOUR_RATES["SL7"]
        + 1 * LABOUR_RATES["SJ 18"]
        + 1 * LABOUR_RATES["SBC"]
        + 1 * LABOUR_RATES["T8 TUBE"]
        + 2 * LABOUR_RATES["CTTRA"]
        + 2 * LABOUR_RATES["T2 TUBE"]
        + 300 * LABOUR_RATES["MONARFLEX TARP"]
    )
    g_tceb = f_tceb * g3
    if height <= 0:
        return 0.0
    cost_per_vertical_ft = (tarp * g_tceb) / height
    return height_engine_total(height, cost_per_vertical_ft)


def deck_level_equipment(config: str, context: dict) -> dict[str, float]:
    if config not in DECK_LEVEL_CONFIGS or context["top_deck_level_input"] <= 0:
        return {}
    return run_equipment_recipe(DECK_LEVEL_RECIPES[config], context)


def deck_level_labour(config: str, context: dict) -> float:
    return labour_deck_level(config, context)


def deck_level_end_bay_equipment(config: str, context: dict) -> dict[str, float]:
    if config not in DECK_LEVEL_CONFIGS or context["deck_level_end_bay_input"] <= 0:
        return {}
    return run_equipment_recipe(DECK_LEVEL_END_BAY_RECIPES[config], context)


def deck_level_end_bay_labour(config: str, context: dict) -> float:
    return labour_deck_level_end_bay(config, context)


def build_standard_estimate(data: Input) -> dict:
    config = data.config.upper()
    if config not in STANDARD_CONFIGS:
        raise ValueError(f"Unsupported config: {config}")

    ladder_input = resolved_access_ladder_input(data)
    context = build_context(data)
    sections: dict[str, dict] = {}

    sections["base_unit"] = make_section(
        run_equipment_recipe(BASE_UNIT_RECIPES[config], context),
        labour_base_unit(config, context),
    )

    sections["end_bay_leg"] = make_section(
        run_equipment_recipe(END_BAY_LEG_RECIPES[config], context),
        labour_end_bay_leg(config, context),
    )

    sections["base_out"] = make_section(
        base_out_equipment(data.base_out_input),
        base_out_labour(data.length, data.base_out_input),
    )

    sections["base_out_eb"] = make_section(
        base_out_eb_equipment(data.base_out_eb_input),
        base_out_eb_labour(data.base_out_eb_input, data.g3),
    )

    sections["access_ladder"] = make_section(
        access_ladder_equipment(data.height, ladder_input),
        access_ladder_labour(data.height, ladder_input, data.g3),
    )

    sections["tie_in"] = make_section(
        tie_in_equipment(data.length, data.height, data.tie_in_input),
        tie_in_labour(data.length, data.height, data.tie_in_input, data.g3),
    )

    sections["top_guard_rail"] = make_section(
        top_guard_rail_equipment(data.length, data.top_guard_rail_input),
        top_guard_rail_labour(data.length, data.height, data.top_guard_rail_input, data.g3),
    )

    sections["top_guard_rail_ends"] = make_section(
        top_guard_rail_ends_equipment(data.top_guard_rail_ends_input),
        top_guard_rail_ends_labour(data.height, data.top_guard_rail_ends_input, data.g3),
    )

    sections["deck_level"] = make_section(
        deck_level_equipment(config, context),
        deck_level_labour(config, context),
    )

    sections["deck_level_end_bay"] = make_section(
        deck_level_end_bay_equipment(config, context),
        deck_level_end_bay_labour(config, context),
    )

    sections["tarp_canopy"] = make_section(
        tarp_canopy_equipment(data.length, data.height, data.tarp),
        tarp_canopy_labour(data.length, data.height, data.tarp),
    )

    sections["tarp_canopy_end_bay"] = make_section(
        tarp_canopy_end_bay_equipment(data.tarp),
        tarp_canopy_end_bay_labour(data.height, data.tarp, data.g3),
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
        "config": {
            "selected": config,
            "metadata": CONFIG_METADATA[config],
        },
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


def build_estimate(data: Input) -> dict:
    config = data.config.upper()
    if config not in STANDARD_CONFIGS:
        raise ValueError(f"Unsupported config: {config}")
    return build_standard_estimate(data)


@app.get("/")
def root():
    return {
        "status": "ok",
        "supported_configs": list(CONFIG_METADATA.keys()),
    }


@app.get("/configs")
def get_configs():
    return {
        "configs": CONFIG_METADATA,
    }


@app.post("/calculate")
def calculate(data: Input):
    return build_estimate(data)
