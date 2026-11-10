"""Live demo of the Member 1 data module.

Run from the repo root:   python demo_member1.py
Skip the pauses:          python demo_member1.py --fast

Works on temporary copies, so your real data files are never changed.
"""
import shutil
import sys
import tempfile
from pathlib import Path

from src.data_manager import DataManager
from src.database import import_csv
from src.generate_sample_data import generate
from src.validation import ValidationError

FAST = "--fast" in sys.argv


def step(title):
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")
    if not FAST:
        input("(press Enter) ")


def try_it(label, func):
    try:
        func()
        print(f"  ACCEPTED: {label}")
    except (ValidationError, KeyError) as e:
        print(f"  REJECTED: {label}\n            reason: {e}")


with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp) / "data"
    shutil.copytree("data", work)
    dm = DataManager(work)

    step("1. Load clean, validated data (get_clean_data)")
    data = dm.get_clean_data()
    for name, df in data.items():
        print(f"\n{name}: {len(df)} rows\n{df.to_string(index=False)}")

    step("2. Add, update and delete records")
    dm.add("rooms", {"room_id": "R106", "capacity": "50", "facilities": "Projector"})
    print("  added R106  ->", dm.get("rooms", "R106"))
    dm.update("classes", "C101", {"students": "60"})
    print("  updated C101 students ->", dm.get("classes", "C101")["students"])
    dm.delete("rooms", "R106")
    print("  deleted R106; rooms left:", len(dm.get_all("rooms")))

    step("3. Validation rejects bad input")
    try_it("duplicate room ID R101", lambda: dm.add("rooms", {"room_id": "R101", "capacity": "30"}))
    try_it("negative capacity", lambda: dm.add("rooms", {"room_id": "R900", "capacity": "-5"}))
    try_it("capacity 'abc'", lambda: dm.add("rooms", {"room_id": "R901", "capacity": "abc"}))
    try_it("empty class name", lambda: dm.add("classes", {"class_id": "C900", "class_name": "", "students": "20"}))
    try_it("changing an ID", lambda: dm.update("classes", "C101", {"class_id": "C999"}))
    try_it("unknown record", lambda: dm.get("rooms", "R404"))
    print("  rooms still stored:", len(dm.get_all("rooms")), "(bad input never reached the data)")

    step("4. Cross-table check and oversized classes")
    dm.add("classes", {"class_id": "C950", "class_name": "Test", "students": "20", "fixed_slot": "T9"})
    print("  problems found:", dm.validate_all())
    dm.delete("classes", "C950")
    big = DataManager("data_stress")
    print("  data_stress classes too large for every room:", big.oversized_classes())

    step("5. Same data stored in SQLite")
    db = Path(tmp) / "demo.db"
    import_csv("data_large", db)
    sql = DataManager.from_sqlite(db)
    csv_data = DataManager("data_large").get_clean_data()
    sql_data = sql.get_clean_data()
    for t in ("rooms", "classes", "slots"):
        same = csv_data[t].equals(sql_data[t])
        print(f"  {t}: CSV and SQLite identical = {same}  ({len(sql_data[t])} rows)")

    step("6. Generate a custom dataset")
    out = Path(tmp) / "custom"
    d = generate(out=out, n_classes=60, n_rooms=20, seed=1)
    print(f"  generated {len(d['classes'])} classes, {len(d['rooms'])} rooms, {len(d['slots'])} slots")
    print("  valid:", bool(DataManager(out).get_clean_data()))

print("\nDemo finished. Your real data files were not changed.")
