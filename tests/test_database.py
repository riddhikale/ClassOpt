import tempfile
from pathlib import Path

import pandas as pd

from src.data_manager import DataManager
from src.database import SQLiteStore, import_csv
from src.validation import ValidationError

DATA = Path(__file__).resolve().parent.parent / "data"
LARGE = Path(__file__).resolve().parent.parent / "data_large"


def _seeded(tmp, source=DATA):
    db = Path(tmp) / "test.db"
    import_csv(source, db)
    return db


def _raises(func, exc):
    try:
        func()
    except exc:
        return True
    return False


def test_fresh_database_is_empty_and_accepts_records():
    with tempfile.TemporaryDirectory() as tmp:
        dm = DataManager.from_sqlite(Path(tmp) / "new.db")
        assert len(dm.get_all("rooms")) == 0
        dm.add("rooms", {"room_id": "R1", "capacity": "40", "facilities": "Projector"})
        assert dm.get("rooms", "R1")["capacity"] == 40


def test_import_matches_csv_results():
    for source in (DATA, LARGE):
        with tempfile.TemporaryDirectory() as tmp:
            csv_data = DataManager(source).get_clean_data()
            sql_data = DataManager.from_sqlite(_seeded(tmp, source)).get_clean_data()
            for table in ("rooms", "classes", "slots"):
                pd.testing.assert_frame_equal(csv_data[table], sql_data[table])


def test_crud_on_sqlite():
    with tempfile.TemporaryDirectory() as tmp:
        dm = DataManager.from_sqlite(_seeded(tmp))
        dm.add("rooms", {"room_id": "R106", "capacity": "50"})
        dm.update("classes", "C101", {"students": "60"})
        dm.delete("rooms", "R102")
        assert dm.get("rooms", "R106")["capacity"] == 50
        assert dm.get("classes", "C101")["students"] == 60
        assert "R102" not in dm.get_all("rooms")["room_id"].values
        assert _raises(lambda: dm.get("rooms", "R102"), KeyError)


def test_data_persists_after_reopening():
    with tempfile.TemporaryDirectory() as tmp:
        db = _seeded(tmp)
        DataManager.from_sqlite(db).add("rooms", {"room_id": "R200", "capacity": "70"})
        assert DataManager.from_sqlite(db).get("rooms", "R200")["capacity"] == 70


def test_validation_still_blocks_bad_input_and_db_is_unchanged():
    with tempfile.TemporaryDirectory() as tmp:
        dm = DataManager.from_sqlite(_seeded(tmp))
        assert _raises(lambda: dm.add("rooms", {"room_id": "R101", "capacity": "30"}), ValidationError)
        assert _raises(lambda: dm.add("rooms", {"room_id": "R300", "capacity": "-5"}), ValidationError)
        assert _raises(lambda: dm.update("classes", "C101", {"students": "abc"}), ValidationError)
        assert len(dm.get_all("rooms")) == 5
        assert dm.get("classes", "C101")["students"] == 55


def test_cross_table_check_and_oversized_work_on_sqlite():
    with tempfile.TemporaryDirectory() as tmp:
        dm = DataManager.from_sqlite(_seeded(tmp))
        dm.add("classes", {"class_id": "C106", "class_name": "X", "students": "20", "fixed_slot": "T9"})
        assert any("T9" in e for e in dm.validate_all())
        dm.update("classes", "C106", {"fixed_slot": "T2", "students": "150"})
        assert dm.oversized_classes() == ["C106"]


def test_import_rejects_invalid_csv_and_writes_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "bad"
        bad.mkdir()
        for name in ("classes.csv", "time_slots.csv"):
            (bad / name).write_text((DATA / name).read_text())
        (bad / "classrooms.csv").write_text("room_id,capacity,facilities\nR1,0,\n")
        db = Path(tmp) / "x.db"
        assert _raises(lambda: import_csv(bad, db), ValidationError)
        assert not db.exists() or len(SQLiteStore(db).read("rooms")) == 0
