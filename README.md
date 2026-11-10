# ClassOpt

## Data module 
Data store with validation for classrooms, classes and time slots. Stores data in
CSV files (default) or SQLite. All data is **simulated**.

### Setup
    git clone https://github.com/riddhikale/ClassOpt.git
    cd ClassOpt
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python -m pytest

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
`oversized_classes()` lists classes that fit no room.

### Columns
- **rooms:** `room_id`, `capacity`, `facilities`
- **classes:** `class_id`, `class_name`, `students`, `instructor`, `student_group`, `fixed_slot` (blank = any slot)
- **slots:** `slot_id`, `day`, `time`

### Validation rules
- Required columns present; IDs not empty and not duplicated
- `capacity` and `students` must be positive whole numbers
- `class_name`, `day` and `time` must not be empty
- `fixed_slot`, if given, must exist in the time slots
- IDs cannot be changed by `update`; delete and re-add instead

### Storage options
CSV files are the default. SQLite is an alternative backend with the same
interface and identical results:

    python -m src.database --from-csv data_large --db classopt.db

    from src.data_manager import DataManager
    dm = DataManager.from_sqlite("classopt.db")
    data = dm.get_clean_data()

`*.db` files are not committed; recreate them with the command above.

### Generate a custom dataset
    python -m src.generate_sample_data --out data_big --classes 60 --rooms 20

The same `--seed` always gives the same files.

### Live demo
    python demo_member1.py

Shows loading, add/update/delete, rejected bad input, oversized classes and
CSV vs SQLite. Use `--fast` to skip the pauses. It works on temporary copies,
so the real data files are never changed.

### Files
- `src/validation.py`: validation rules
- `src/data_manager.py`: add, update, delete, get, `get_clean_data()`
- `src/database.py`: SQLite backend and CSV import
- `src/generate_sample_data.py`: dataset generator
- `tests/`: 25 tests

### Run tests
    python -m pytest