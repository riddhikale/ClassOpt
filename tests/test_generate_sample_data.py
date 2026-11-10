import tempfile
from pathlib import Path

from src.data_manager import DataManager
from src.generate_sample_data import generate


def test_default_size_and_valid():
    with tempfile.TemporaryDirectory() as d:
        generate(out=d)
        data = DataManager(d).get_clean_data()
        assert len(data["classes"]) == 30
        assert len(data["rooms"]) == 12
        assert len(data["slots"]) == 20


def test_same_seed_gives_same_files():
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        generate(out=a, seed=7)
        generate(out=b, seed=7)
        for name in ["classes.csv", "classrooms.csv", "time_slots.csv"]:
            assert (Path(a) / name).read_text() == (Path(b) / name).read_text()


def test_valid_for_many_seeds_and_nothing_oversized_by_default():
    for seed in range(25):
        with tempfile.TemporaryDirectory() as d:
            generate(out=d, seed=seed)
            assert DataManager(d).oversized_classes() == []


def test_fixed_slots_never_clash():
    for seed in range(25):
        with tempfile.TemporaryDirectory() as d:
            classes = generate(out=d, seed=seed, fixed_fraction=0.5)["classes"]
            fixed = classes[classes["fixed_slot"] != ""]
            for _, grp in fixed.groupby("fixed_slot"):
                assert grp["instructor"].is_unique
                assert grp["student_group"].is_unique


def test_oversized_flag():
    with tempfile.TemporaryDirectory() as d:
        generate(out=d, oversized=2)
        assert len(DataManager(d).oversized_classes()) == 2
