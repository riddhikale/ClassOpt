
import pandas as pd
import pytest

from src.optimization import optimize_allocation


@pytest.fixture
def sample_data():
    return {
        "rooms": pd.DataFrame([
            {"room_id": "R1", "capacity": 30, "facilities": ""},
            {"room_id": "R2", "capacity": 60, "facilities": ""},
            {"room_id": "R3", "capacity": 100, "facilities": ""}
        ]),

        "classes": pd.DataFrame([
            {
                "class_id": "C1",
                "class_name": "IT-A",
                "students": 25,
                "instructor": "Teacher1",
                "student_group": "Group1",
                "fixed_slot": ""
            },
            {
                "class_id": "C2",
                "class_name": "IT-B",
                "students": 55,
                "instructor": "Teacher2",
                "student_group": "Group2",
                "fixed_slot": ""
            }
        ]),

        "slots": pd.DataFrame([
            {"slot_id": "T1", "day": "Monday", "time": "09:00-10:00"},
            {"slot_id": "T2", "day": "Monday", "time": "10:00-11:00"}
        ])
    }


def test_all_classes_are_allocated(sample_data):
    result = optimize_allocation(sample_data)

    assert result["status"] in ("OPTIMAL", "FEASIBLE")
    assert len(result["assignments"]) == 2
    assert result["unallocated_classes"] == []


def test_room_capacity_is_sufficient(sample_data):
    result = optimize_allocation(sample_data)

    for assignment in result["assignments"]:
        assert assignment["capacity"] >= assignment["students"]


def test_same_room_is_not_used_twice_in_same_slot(sample_data):
    result = optimize_allocation(sample_data)

    used_rooms = [
        (a["room_id"], a["slot_id"])
        for a in result["assignments"]
    ]

    assert len(used_rooms) == len(set(used_rooms))


def test_fixed_slot_is_respected(sample_data):
    sample_data["classes"].loc[
        sample_data["classes"]["class_id"] == "C1",
        "fixed_slot"
    ] = "T2"

    result = optimize_allocation(sample_data)

    assignment = next(
        a for a in result["assignments"]
        if a["class_id"] == "C1"
    )

    assert assignment["slot_id"] == "T2"


def test_instructor_conflict_is_prevented(sample_data):
    sample_data["classes"].loc[
        sample_data["classes"]["class_id"] == "C2",
        "instructor"
    ] = "Teacher1"

    result = optimize_allocation(sample_data)

    c1 = next(a for a in result["assignments"] if a["class_id"] == "C1")
    c2 = next(a for a in result["assignments"] if a["class_id"] == "C2")

    assert c1["slot_id"] != c2["slot_id"]


def test_student_group_conflict_is_prevented(sample_data):
    sample_data["classes"].loc[
        sample_data["classes"]["class_id"] == "C2",
        "student_group"
    ] = "Group1"

    result = optimize_allocation(sample_data)

    c1 = next(a for a in result["assignments"] if a["class_id"] == "C1")
    c2 = next(a for a in result["assignments"] if a["class_id"] == "C2")

    assert c1["slot_id"] != c2["slot_id"]


def test_oversized_class_is_unallocated(sample_data):
    sample_data["classes"].loc[
        sample_data["classes"]["class_id"] == "C1",
        "students"
    ] = 150

    result = optimize_allocation(sample_data)

    assert "C1" in result["unallocated_classes"]
    assert all(
        a["class_id"] != "C1"
        for a in result["assignments"]
    )
