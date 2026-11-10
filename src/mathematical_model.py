
"""
Mathematical Model for ClassOpt
Member 3 - Optimization Engine

This module defines the mathematical formulation used
for optimal classroom allocation.
"""

# Sets
# C = Set of classes
# R = Set of classrooms
# T = Set of available time slots


def define_model():
    """
    Mathematical formulation:

    Decision Variable:
    x(i,j,t) = 1 if class i is assigned to room j
               at time slot t, otherwise 0.

    Objective Function:
    Minimize total unused seats.

    Z = Sum[(capacity_j - students_i) * x(i,j,t)]

    Constraints:
    1. Every class must receive exactly one assignment.
    2. A room can accommodate at most one class per slot.
    3. Room capacity must be sufficient.
    4. An instructor cannot teach two classes simultaneously.
    5. A student group cannot attend two classes simultaneously.
    6. Fixed time slots must be respected.
    """

    model_details = {
        "sets": {
            "C": "Set of classes",
            "R": "Set of classrooms",
            "T": "Set of available time slots"
        },

        "decision_variable": (
            "x(i,j,t) = 1 if class i is assigned to room j "
            "at time t; otherwise 0"
        ),

        "objective": (
            "Minimize sum of (capacity_j - students_i) "
            "* x(i,j,t)"
        ),

        "constraints": [
            "Each class receives exactly one assignment",
            "A room hosts at most one class per time slot",
            "Room capacity >= number of students",
            "Same instructor cannot teach simultaneously",
            "Same student group cannot attend simultaneously",
            "Fixed class time must be respected"
        ]
    }

    return model_details


if __name__ == "__main__":
    details = define_model()

    print("CLASSOPT - MATHEMATICAL MODEL")
    print("=" * 40)

    for key, value in details.items():
        print(f"\n{key.upper()}:")

        if isinstance(value, dict):
            for k, v in value.items():
                print(f"{k}: {v}")
        elif isinstance(value, list):
            for item in value:
                print("-", item)
        else:
            print(value)
