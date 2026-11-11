
def has_conflict(cls, slot_id, assignments):
    """
    Check whether the instructor or student group is already occupied in the given time slot.
    """

    occupied_instructors = {
        a["instructor"]
        for a in assignments
        if a["slot_id"] == slot_id
    }

    occupied_groups = {
        a["student_group"]
        for a in assignments
        if a["slot_id"] == slot_id
    }

    return (
        cls["instructor"] in occupied_instructors
        or cls["student_group"] in occupied_groups
    )
