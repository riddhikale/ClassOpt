
from .conflict_detector import get_conflicts


def allocate_classes(rooms, classes, slots):
    """
    Allocate classes to classrooms using Greedy Best-Fit.

    Strategy:
    1. Allocate larger classes first.
    2. Respect fixed time slots.
    3. Check instructor and student-group conflicts.
    4. Select the room with minimum unused seats.
    5. Report reasons for unallocated classes.
    """

    assignments = []
    unallocated = []

    # Track occupied room-slot combinations using a set.
    occupied_rooms = set()

    # Find the maximum classroom capacity.
    max_capacity = int(rooms["capacity"].max())

    # Process larger classes first.
    ordered_classes = classes.sort_values(
        by="students",
        ascending=False
    )

    for _, cls in ordered_classes.iterrows():

        students = int(cls["students"])
        fixed_slot = str(cls["fixed_slot"]).strip()

        # Respect fixed slots; otherwise consider all slots.
        if fixed_slot:
            available_slots = slots[
                slots["slot_id"] == fixed_slot
            ]
        else:
            available_slots = slots

        best_choice = None
        min_unused = float("inf")

        # Store reasons for scheduling conflicts.
        conflict_reasons = set()

        # Examine all possible room-slot combinations.
        for _, slot in available_slots.iterrows():

            slot_id = slot["slot_id"]

            # Check instructor and student-group conflicts.
            conflicts = get_conflicts(
                cls, slot_id, assignments
            )

            if conflicts:
                conflict_reasons.update(conflicts)
                continue

            # Check available rooms.
            for _, room in rooms.iterrows():

                room_id = room["room_id"]
                capacity = int(room["capacity"])

                # Check capacity.
                if capacity < students:
                    continue

                # Check whether the room is already occupied.
                if (room_id, slot_id) in occupied_rooms:
                    continue

                unused = capacity - students

                # Select the combination with minimum unused seats.
                if unused < min_unused:

                    min_unused = unused

                    best_choice = {
                        "room_id": room_id,
                        "capacity": capacity,
                        "slot_id": slot_id,
                        "day": slot["day"],
                        "time": slot["time"]
                    }

        # Save the best allocation.
        if best_choice is not None:

            assignments.append({
                "class_id": cls["class_id"],
                "class_name": cls["class_name"],
                "room_id": best_choice["room_id"],
                "slot_id": best_choice["slot_id"],
                "day": best_choice["day"],
                "time": best_choice["time"],
                "students": students,
                "capacity": best_choice["capacity"],
                "unused_seats": min_unused,
                "instructor": cls["instructor"],
                "student_group": cls["student_group"]
            })

            occupied_rooms.add(
                (best_choice["room_id"], best_choice["slot_id"])
            )

        # Explain why the class could not be allocated.
        else:

            if students > max_capacity:
                reason = (
                    f"Exceeds maximum room capacity "
                    f"({students} > {max_capacity})"
                )

            elif conflict_reasons:
                reason = (
                    "Scheduling conflicts: "
                    + "; ".join(sorted(conflict_reasons))
                )

            else:
                reason = (
                    "No available room in permitted time slots"
                )

            unallocated.append({
                "class_id": cls["class_id"],
                "class_name": cls["class_name"],
                "students": students,
                "reason": reason
            })

    return {
        "assignments": assignments,
        "unallocated": unallocated
    }
