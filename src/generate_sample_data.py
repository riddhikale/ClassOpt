"""Generate a larger, reproducible SIMULATED dataset for ClassOpt (Member 1).

Examples (run from the repo root):
    python -m src.generate_sample_data
    python -m src.generate_sample_data --out data_stress --instructors 6 --fixed-fraction 0.4 --oversized 2

The same --seed always gives the same files, so the whole team tests on identical data.
"""
import argparse
import math
import random
from pathlib import Path

import pandas as pd

from .data_manager import DataManager
from .validation import CLASS_COLS, ROOM_COLS, SLOT_COLS

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
DEPTS = ["IT", "CS", "EXTC", "MECH", "CIVIL", "ELEC"]
SUBJECTS = ["DM", "DS", "OS", "CN", "DBMS", "AI", "MATH", "PHY"]
SURNAMES = ["Rao", "Shah", "Iyer", "Mehta", "Patil", "Kulkarni", "Joshi", "Nair",
            "Desai", "Verma", "Gupta", "Kale", "Pawar", "Sen", "Bose", "Menon"]
CAPACITIES = [30, 40, 50, 60, 80, 100, 120]
FACILITIES = ["Projector", "Projector", "Smart board", ""]


def make_rooms(n_rooms, rng):
    caps = sorted(rng.choice(CAPACITIES) for _ in range(n_rooms))
    return pd.DataFrame(
        [{"room_id": f"R{101 + i}", "capacity": c, "facilities": rng.choice(FACILITIES)}
         for i, c in enumerate(caps)],
        columns=ROOM_COLS,
    )


def make_slots(days, slots_per_day):
    rows = []
    for d in range(days):
        for k in range(slots_per_day):
            hour = 9 + k
            rows.append({"slot_id": f"T{len(rows) + 1}", "day": DAYS[d % len(DAYS)],
                         "time": f"{hour:02d}:00-{hour + 1:02d}:00"})
    return pd.DataFrame(rows, columns=SLOT_COLS)


def _instructor_pool(n):
    return [f"Prof. {SURNAMES[k % len(SURNAMES)]}{k // len(SURNAMES) or ''}" for k in range(n)]


def make_classes(n_classes, max_cap, slots, n_rooms, n_instructors, fixed_fraction, oversized, rng):
    # Every student group has several subjects, so classes of one group conflict with each other.
    n_groups = max(1, round(n_classes / 3))
    groups = [f"{DEPTS[i % len(DEPTS)]}-{chr(65 + i // len(DEPTS))}" for i in range(n_groups)]
    low, high = min(20, max_cap), min(100, max_cap)
    group_size = {g: rng.randint(low, high) for g in groups}
    pool = _instructor_pool(n_instructors)

    rows = []
    for i in range(n_classes):
        g = groups[i % n_groups]
        rows.append({
            "class_id": f"C{101 + i}",
            "class_name": f"{g}-{SUBJECTS[(i // n_groups) % len(SUBJECTS)]}",
            "students": group_size[g],
            "instructor": rng.choice(pool),
            "student_group": g,
            "fixed_slot": "",
        })

    # Stress option: classes that fit in no room (they must end up unallocated).
    for row in rows[n_classes - oversized:] if oversized else []:
        row["students"] = max_cap + rng.randint(10, 40)

    # Fixed times, never two fixed classes of the same instructor/group in one slot.
    candidates = [r for r in rows if r["students"] <= max_cap]
    rng.shuffle(candidates)
    used = {}  # slot_id -> {"people": set, "count": int}
    for row in candidates[: round(n_classes * fixed_fraction)]:
        for _ in range(30):
            slot = rng.choice(slots["slot_id"].tolist())
            info = used.setdefault(slot, {"people": set(), "count": 0})
            who = {row["instructor"], row["student_group"]}
            if not (info["people"] & who) and info["count"] < max(1, n_rooms // 2):
                info["people"] |= who
                info["count"] += 1
                row["fixed_slot"] = slot
                break
    return pd.DataFrame(rows, columns=CLASS_COLS)


def generate(out="data_large", n_classes=30, n_rooms=12, days=4, slots_per_day=5,
             n_instructors=12, fixed_fraction=0.2, oversized=0, seed=42):
    rng = random.Random(seed)
    rooms = make_rooms(n_rooms, rng)
    slots = make_slots(days, slots_per_day)
    classes = make_classes(n_classes, int(rooms["capacity"].max()), slots, n_rooms,
                           n_instructors, fixed_fraction, oversized, rng)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rooms.to_csv(out / "classrooms.csv", index=False)
    classes.to_csv(out / "classes.csv", index=False)
    slots.to_csv(out / "time_slots.csv", index=False)
    DataManager(out).get_clean_data()  # fails loudly if the generated data were invalid
    return {"rooms": rooms, "classes": classes, "slots": slots}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="data_large")
    p.add_argument("--classes", type=int, default=30)
    p.add_argument("--rooms", type=int, default=12)
    p.add_argument("--days", type=int, default=4)
    p.add_argument("--slots-per-day", type=int, default=5)
    p.add_argument("--instructors", type=int, default=12)
    p.add_argument("--fixed-fraction", type=float, default=0.2)
    p.add_argument("--oversized", type=int, default=0, help="classes too big for every room")
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args()
    d = generate(a.out, a.classes, a.rooms, a.days, a.slots_per_day, a.instructors,
                 a.fixed_fraction, a.oversized, a.seed)
    fixed = int((d["classes"]["fixed_slot"] != "").sum())
    print(f"Wrote {a.out}/: {len(d['classes'])} classes ({fixed} fixed), "
          f"{len(d['rooms'])} rooms, {len(d['slots'])} slots")
    print("Classes too large for every room:", DataManager(a.out).oversized_classes() or "none")


if __name__ == "__main__":
    main()
