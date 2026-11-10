import shutil
from pathlib import Path

import pytest

from src.data_manager import DataManager
from src.validation import ValidationError, find_oversized_classes

DATA = Path(__file__).resolve().parent.parent / "data"


@pytest.fixture
def dm(tmp_path):
    shutil.copytree(DATA, tmp_path / "data")
    return DataManager(tmp_path / "data")


def test_sample_data_is_valid(dm):
    data = dm.get_clean_data()
    assert len(data["rooms"]) == 5
    assert len(data["classes"]) == 5
    assert len(data["slots"]) == 4
    assert data["rooms"]["capacity"].dtype.kind == "i"


def test_add_and_get(dm):
    dm.add("rooms", {"room_id": "R106", "capacity": "50", "facilities": "Projector"})
    assert dm.get("rooms", "R106")["capacity"] == 50


def test_duplicate_id_rejected(dm):
    with pytest.raises(ValidationError):
        dm.add("rooms", {"room_id": "R101", "capacity": "30"})


@pytest.mark.parametrize("bad", ["0", "-5", "abc", "", "12.5"])
def test_bad_capacity_rejected(dm, bad):
    with pytest.raises(ValidationError):
        dm.add("rooms", {"room_id": "R200", "capacity": bad})


def test_update_and_id_is_locked(dm):
    dm.update("classes", "C101", {"students": "60"})
    assert dm.get("classes", "C101")["students"] == 60
    with pytest.raises(ValidationError):
        dm.update("classes", "C101", {"class_id": "C999"})


def test_update_invalid_value_rejected_and_file_unchanged(dm):
    with pytest.raises(ValidationError):
        dm.update("classes", "C101", {"students": "-1"})
    assert dm.get("classes", "C101")["students"] == 55


def test_delete(dm):
    dm.delete("rooms", "R102")
    assert "R102" not in dm.get_all("rooms")["room_id"].values
    with pytest.raises(KeyError):
        dm.delete("rooms", "R102")


def test_fixed_slot_must_exist(dm):
    dm.add("classes", {"class_id": "C106", "class_name": "X", "students": "20", "fixed_slot": "T9"})
    assert any("T9" in e for e in dm.validate_all())
    with pytest.raises(ValidationError):
        dm.get_clean_data()


def test_oversized_class_is_flagged(dm):
    dm.add("classes", {"class_id": "C107", "class_name": "Big", "students": "150"})
    assert dm.oversized_classes() == ["C107"]
    d = dm.get_clean_data()
    assert find_oversized_classes(d["classes"], d["rooms"]) == ["C107"]
