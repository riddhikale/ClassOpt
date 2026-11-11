
def get_conflicts(cls, slot_id, assignments):
    """Return instructor and student-group conflicts."""

    conflicts = []

    for assigned in assignments:

        if assigned["slot_id"] != slot_id:
            continue

        if cls["instructor"] == assigned["instructor"]:
            conflicts.append(
                f"Instructor {cls['instructor']} is already occupied"
            )

        if cls["student_group"] == assigned["student_group"]:
            conflicts.append(
                f"Student group {cls['student_group']} is already occupied"
            )

    return conflicts


def has_conflict(cls, slot_id, assignments):
    """Return True if any scheduling conflict exists."""

    return bool(get_conflicts(cls, slot_id, assignments))
