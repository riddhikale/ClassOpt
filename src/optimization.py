
"""
ClassOpt - Classroom Optimization Engine
Member 3: Optimization Engine

Uses Google OR-Tools CP-SAT to find classroom
assignments that minimize unused seating capacity.
"""

from ortools.sat.python import cp_model


def optimize_allocation(data, time_limit_seconds=30):
    """
    Optimize classroom allocation using OR-Tools.

    Parameters:
        data: Dictionary containing validated DataFrames:
              data["rooms"], data["classes"], data["slots"]

        time_limit_seconds: Maximum solver execution time.

    Returns:
        Dictionary containing solver status, assignments,
        unallocated classes and performance information.
    """

    rooms = data["rooms"].to_dict("records")
    classes = data["classes"].to_dict("records")
    slots = data["slots"].to_dict("records")

    # Identify classes that cannot fit in any classroom.
    max_capacity = max(
        (int(r["capacity"]) for r in rooms), default=0
    )

    oversized_classes = [
        c for c in classes
        if int(c["students"]) > max_capacity
    ]

    oversized_ids = {
        c["class_id"] for c in oversized_classes
    }

    # Only feasible classes enter the optimization model.
    schedulable_classes = [
        c for c in classes
        if c["class_id"] not in oversized_ids
    ]

    if not schedulable_classes:
        return {
            "status": "NO_FEASIBLE_CLASSES",
            "assignments": [],
            "unallocated_classes": [
                c["class_id"] for c in oversized_classes
            ],
            "total_unused_seats": 0,
            "solver_time": 0
        }

    model = cp_model.CpModel()

    # ------------------------------------------------
    # STEP 1: Create binary decision variables
    # x[i,j,t] = 1 if class i uses room j at slot t.
    # ------------------------------------------------

    x = {}

    for i, c in enumerate(schedulable_classes):
        for j, r in enumerate(rooms):

            # A room cannot be used if capacity is insufficient.
            if int(r["capacity"]) < int(c["students"]):
                continue

            for t, slot in enumerate(slots):

                # Respect fixed time slots.
                fixed_slot = str(c.get("fixed_slot", "")).strip()

                if fixed_slot and fixed_slot != str(slot["slot_id"]):
                    continue

                x[i, j, t] = model.NewBoolVar(
                    f"x_{i}_{j}_{t}"
                )

    # ------------------------------------------------
    # STEP 2: Every schedulable class gets exactly
    # one room and one time slot.
    # ------------------------------------------------

    for i, c in enumerate(schedulable_classes):

        variables = [
            var for (ci, j, t), var in x.items()
            if ci == i
        ]

        if not variables:
            return {
                "status": "NO_FEASIBLE_ASSIGNMENT",
                "assignments": [],
                "unallocated_classes": [
                    c["class_id"]
                    for c in schedulable_classes
                ] + [
                    c["class_id"] for c in oversized_classes
                ],
                "total_unused_seats": 0,
                "solver_time": 0
            }

        model.AddExactlyOne(variables)

    # ------------------------------------------------
    # STEP 3: A room can host at most one class
    # during a particular time slot.
    # ------------------------------------------------

    for j, room in enumerate(rooms):
        for t, slot in enumerate(slots):

            variables = [
                var for (i, rj, st), var in x.items()
                if rj == j and st == t
            ]

            if variables:
                model.AddAtMostOne(variables)

    # ------------------------------------------------
    # STEP 4: Prevent instructor and student-group
    # conflicts during the same time slot.
    # ------------------------------------------------

    for i in range(len(schedulable_classes)):
        for k in range(i + 1, len(schedulable_classes)):

            class_a = schedulable_classes[i]
            class_b = schedulable_classes[k]

            instructor_a = str(
                class_a.get("instructor", "")
            ).strip()

            instructor_b = str(
                class_b.get("instructor", "")
            ).strip()

            group_a = str(
                class_a.get("student_group", "")
            ).strip()

            group_b = str(
                class_b.get("student_group", "")
            ).strip()

            same_instructor = (
                instructor_a
                and instructor_b
                and instructor_a == instructor_b
            )

            same_group = (
                group_a
                and group_b
                and group_a == group_b
            )

            if same_instructor or same_group:

                for t, slot in enumerate(slots):

                    variables = [
                        var
                        for (ci, j, st), var in x.items()
                        if ci in (i, k) and st == t
                    ]

                    if variables:
                        model.Add(sum(variables) <= 1)

    # ------------------------------------------------
    # STEP 5: Objective function
    # Minimize total unused seats.
    # ------------------------------------------------

    unused_seats = []

    for (i, j, t), var in x.items():

        capacity = int(rooms[j]["capacity"])
        students = int(schedulable_classes[i]["students"])

        unused = capacity - students

        unused_seats.append(unused * var)

    model.Minimize(sum(unused_seats))

    # ------------------------------------------------
    # STEP 6: Run OR-Tools solver.
    # ------------------------------------------------

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds

    status = solver.Solve(model)
    status_name = solver.StatusName(status)

    assignments = []

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):

        for (i, j, t), var in x.items():

            if solver.Value(var) == 1:

                c = schedulable_classes[i]
                r = rooms[j]
                slot = slots[t]

                capacity = int(r["capacity"])
                students = int(c["students"])

                assignments.append({
                    "class_id": c["class_id"],
                    "room_id": r["room_id"],
                    "day": slot["day"],
                    "time_slot": slot["time"],
                    "slot_id": slot["slot_id"],
                    "students": students,
                    "capacity": capacity,
                    "unused_seats": capacity - students
                })

    # ------------------------------------------------
    # STEP 7: Prepare final results.
    # ------------------------------------------------

    assigned_ids = {
        a["class_id"] for a in assignments
    }

    unallocated = [
        c["class_id"]
        for c in classes
        if c["class_id"] not in assigned_ids
    ]

    total_unused = sum(
        a["unused_seats"] for a in assignments
    )

    return {
        "status": status_name,
        "assignments": assignments,
        "unallocated_classes": unallocated,
        "total_unused_seats": total_unused,
        "solver_time": solver.WallTime()
    }


# ----------------------------------------------------
# Standalone execution
# ----------------------------------------------------

if __name__ == "__main__":

    from .data_manager import DataManager

    dm = DataManager()
    clean_data = dm.get_clean_data()

    result = optimize_allocation(clean_data)

    print("\nCLASSOPT - OPTIMIZATION RESULTS")
    print("=" * 45)

    print("Solver Status:", result["status"])

    print("\nOptimized Assignments:")

    for assignment in result["assignments"]:
        print(assignment)

    print("\nUnallocated Classes:")
    print(result["unallocated_classes"])

    print("\nTotal Unused Seats:",
          result["total_unused_seats"])

    print("Solver Execution Time:",
          result["solver_time"], "seconds")
