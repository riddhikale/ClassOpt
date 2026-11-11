
import pandas as pd

from src.allocation import allocate_classes


def create_data():
    rooms = pd.DataFrame([
        {"room_id": "R1", "capacity": 30},
        {"room_id": "R2", "capacity": 50},
        {"room_id": "R3", "capacity": 100}
    ])

    classes = pd.DataFrame([
        {
            "class_id": "C1",
            "class_name": "IT-A",
            "students": 45,
            "instructor": "Dr. Rao",
            "student_group": "IT-A",
            "fixed_slot": ""
        },
        {
            "class_id": "C2",
            "class_name": "CS-A",
            "students": 25,
            "instructor": "Dr. Shah",
            "student_group": "CS-A",
            "fixed_slot": ""
        }
    ])

    slots = pd.DataFrame([
        {"slot_id": "T1", "day": "Monday", "time": "09:00-10:00"},
        {"slot_id": "T2", "day": "Monday", "time": "10:00-11:00"}
    ])

    return rooms, classes, slots


def test_successful_allocation():
    rooms, classes, slots = create_data()
    result = allocate_classes(rooms, classes, slots)

    assert len(result["assignments"]) == 2
    assert len(result["unallocated"]) == 0


def test_best_fit_room_selection():
    rooms, classes, slots = create_data()
    result = allocate_classes(rooms, classes, slots)

    c1 = next(
        a for a in result["assignments"]
        if a["class_id"] == "C1"
    )

    assert c1["room_id"] == "R2"
    assert c1["unused_seats"] == 5


def test_room_capacity():
    rooms, classes, slots = create_data()
    result = allocate_classes(rooms, classes, slots)

    for item in result["assignments"]:
        assert item["capacity"] >= item["students"]


def test_fixed_slot_respected():
    rooms, classes, slots = create_data()
    classes.loc[classes["class_id"] == "C1", "fixed_slot"] = "T2"

    result = allocate_classes(rooms, classes, slots)

    c1 = next(
        a for a in result["assignments"]
        if a["class_id"] == "C1"
    )

    assert c1["slot_id"] == "T2"


def test_oversized_class_unallocated():
    rooms, classes, slots = create_data()
    classes.loc[classes["class_id"] == "C1", "students"] = 150

    result = allocate_classes(rooms, classes, slots)

    assert len(result["unallocated"]) == 1
    assert "Exceeds maximum room capacity" in (
        result["unallocated"][0]["reason"]
    )


def test_room_not_used_twice_in_same_slot():
    rooms, classes, slots = create_data()
    result = allocate_classes(rooms, classes, slots)

    room_slot_pairs = [
        (a["room_id"], a["slot_id"])
        for a in result["assignments"]
    ]

    assert len(room_slot_pairs) == len(set(room_slot_pairs))



def test_instructor_conflict():
    rooms, classes, slots = create_data()

    # Both classes have the same instructor and fixed slot.
    classes.loc[classes["class_id"] == "C1", "fixed_slot"] = "T1"
    classes.loc[classes["class_id"] == "C2", "fixed_slot"] = "T1"
    classes.loc[classes["class_id"] == "C2", "instructor"] = "Dr. Rao"

    result = allocate_classes(rooms, classes, slots)

    assert len(result["assignments"]) == 1
    assert len(result["unallocated"]) == 1
    assert "Instructor" in result["unallocated"][0]["reason"]


def test_student_group_conflict():
    rooms, classes, slots = create_data()

    # Both classes have the same student group and fixed slot.
    classes.loc[classes["class_id"] == "C1", "fixed_slot"] = "T1"
    classes.loc[classes["class_id"] == "C2", "fixed_slot"] = "T1"
    classes.loc[classes["class_id"] == "C2", "student_group"] = "IT-A"

    result = allocate_classes(rooms, classes, slots)

    assert len(result["assignments"]) == 1
    assert len(result["unallocated"]) == 1
    assert "Student group" in result["unallocated"][0]["reason"]
