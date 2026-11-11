
"""
ClassOpt - Performance Metrics
Member 3: Optimization Engine

Calculates allocation success, room utilization,
unused seats and optimization performance.
"""


def calculate_metrics(result, data):
    """
    Calculate performance metrics for an allocation result.

    Parameters:
        result: Output dictionary from optimize_allocation()
        data: Validated data from DataManager.get_clean_data()

    Returns:
        Dictionary containing performance metrics.
    """

    assignments = result["assignments"]

    rooms = data["rooms"]
    classes = data["classes"]
    slots = data["slots"]

    total_classes = len(classes)
    allocated_classes = len(assignments)

    # 1. Allocation success rate
    allocation_rate = (
        allocated_classes / total_classes * 100
        if total_classes else 0
    )

    # 2. Total unused seats
    total_unused_seats = sum(
        a["unused_seats"] for a in assignments
    )

    # 3. Total occupied room capacity
    occupied_capacity = sum(
        a["capacity"] for a in assignments
    )

    # 4. Total available room-time capacity
    available_capacity = (
        rooms["capacity"].sum() * len(slots)
    )

    # 5. Room utilization
    room_utilization = (
        occupied_capacity / available_capacity * 100
        if available_capacity else 0
    )

    # 6. Average unused seats per assignment
    average_unused = (
        total_unused_seats / allocated_classes
        if allocated_classes else 0
    )

    # 7. Number of unallocated classes
    unallocated_classes = len(
        result["unallocated_classes"]
    )

    # 8. Solver execution time
    execution_time = result["solver_time"]

    return {
        "total_classes": total_classes,
        "allocated_classes": allocated_classes,
        "unallocated_classes": unallocated_classes,
        "allocation_success_rate": round(allocation_rate, 2),
        "total_unused_seats": total_unused_seats,
        "average_unused_seats": round(average_unused, 2),
        "room_utilization": round(room_utilization, 2),
        "solver_status": result["status"],
        "execution_time": round(execution_time, 4)
    }


if __name__ == "__main__":

    from .data_manager import DataManager
    from .optimization import optimize_allocation

    dm = DataManager()
    data = dm.get_clean_data()

    result = optimize_allocation(data)

    metrics = calculate_metrics(result, data)

    print("\nCLASSOPT - PERFORMANCE REPORT")
    print("=" * 45)

    for name, value in metrics.items():
        print(f"{name.replace('_', ' ').title()}: {value}")
