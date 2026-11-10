# ClassOpt
## Data module (Member 1)

CSV-backed data store with validation. All data is **simulated**.

### Datasets
| Folder | Contents |
|---|---|
| `data/` | Small sample: 5 classes, 5 rooms, 4 slots |
| `data_large/` | 30 classes, 12 rooms, 20 slots (4 days x 5) |
| `data_stress/` | Edge cases: more clashes, 12 fixed-slot classes, 2 oversized classes |

### Usage
    from src.data_manager import DataManager
    data = DataManager("data_large").get_clean_data()
    rooms, classes, slots = data["rooms"], data["classes"], data["slots"]

`get_clean_data()` returns validated DataFrames or raises `ValidationError`.

### Columns
- **rooms:** `room_id`, `capacity`, `facilities`
- **classes:** `class_id`, `class_name`, `students`, `instructor`, `student_group`, `fixed_slot` (blank = any slot)
- **slots:** `slot_id`, `day`, `time`

### Generate a custom dataset
    python -m src.generate_sample_data --out data_big --classes 60 --rooms 20

### Run tests
    python -m pytest