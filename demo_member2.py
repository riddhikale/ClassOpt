from src.data_manager import DataManager
from src.allocation import allocate_classes

# Load validated data
dm = DataManager()
data = dm.get_clean_data()

# Run greedy allocation
result = allocate_classes(
    data["rooms"],
    data["classes"],
    data["slots"]
)

print("\n===== CLASSROOM ALLOCATION =====")

for item in result["assignments"]:
    print(
        f'{item["class_id"]} | '
        f'{item["room_id"]} | '
        f'{item["day"]} | '
        f'{item["time"]} | '
        f'Unused seats: {item["unused_seats"]}'
    )

print("\n===== UNALLOCATED CLASSES =====")

for item in result["unallocated"]:
    print(item)

print("\nTotal allocated:", len(result["assignments"]))
print("Total unallocated:", len(result["unallocated"]))

print(
    "Total unused seats:",
    sum(a["unused_seats"] for a in result["assignments"])
)