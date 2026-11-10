"""CSV-backed data store for ClassOpt (Member 1).

Other modules should only call get_clean_data(); the dashboard uses
get_all / add / update / delete for the management screens.
"""
from pathlib import Path

import pandas as pd

from . import validation as v

TABLES = {
    "rooms": {
        "file": "classrooms.csv", "id": "room_id", "cols": v.ROOM_COLS,
        "numeric": ["capacity"], "validate": v.validate_rooms,
    },
    "classes": {
        "file": "classes.csv", "id": "class_id", "cols": v.CLASS_COLS,
        "numeric": ["students"], "validate": v.validate_classes,
    },
    "slots": {
        "file": "time_slots.csv", "id": "slot_id", "cols": v.SLOT_COLS,
        "numeric": [], "validate": v.validate_slots,
    },
}


class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    # ---------- internal helpers ----------
    def _cfg(self, table):
        if table not in TABLES:
            raise KeyError(f"Unknown table '{table}'. Use one of {list(TABLES)}")
        return TABLES[table]

    def _path(self, table):
        return self.data_dir / self._cfg(table)["file"]

    def _read_raw(self, table):
        cfg, path = self._cfg(table), self._path(table)
        if not path.exists():
            return pd.DataFrame(columns=cfg["cols"])
        df = pd.read_csv(path, dtype=str, keep_default_na=False)
        return df.apply(lambda col: col.str.strip())

    def _save(self, table, df):
        errors = self._cfg(table)["validate"](df)
        if errors:
            raise v.ValidationError("; ".join(errors))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(self._path(table), index=False)

    # ---------- CRUD ----------
    def get_all(self, table):
        cfg = self._cfg(table)
        df = self._read_raw(table)
        for col in cfg["numeric"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        return df

    def get(self, table, record_id):
        cfg = self._cfg(table)
        df = self.get_all(table)
        row = df[df[cfg["id"]] == str(record_id).strip()]
        if row.empty:
            raise KeyError(f"{table}: '{record_id}' not found")
        return row.iloc[0].to_dict()

    def add(self, table, record):
        cfg = self._cfg(table)
        df = self._read_raw(table)
        row = {c: str(record.get(c, "")).strip() for c in cfg["cols"]}
        if row[cfg["id"]] in df[cfg["id"]].values:
            raise v.ValidationError(f"{table}: {row[cfg['id']]} already exists")
        self._save(table, pd.concat([df, pd.DataFrame([row])], ignore_index=True))

    def update(self, table, record_id, changes):
        cfg = self._cfg(table)
        df = self._read_raw(table)
        mask = df[cfg["id"]] == str(record_id).strip()
        if not mask.any():
            raise KeyError(f"{table}: '{record_id}' not found")
        for col, val in changes.items():
            if col == cfg["id"]:
                raise v.ValidationError("IDs cannot be changed; delete and re-add instead")
            if col not in cfg["cols"]:
                raise v.ValidationError(f"Unknown column '{col}' for {table}")
            df.loc[mask, col] = str(val).strip()
        self._save(table, df)

    def delete(self, table, record_id):
        cfg = self._cfg(table)
        df = self._read_raw(table)
        mask = df[cfg["id"]] == str(record_id).strip()
        if not mask.any():
            raise KeyError(f"{table}: '{record_id}' not found")
        self._save(table, df[~mask])

    # ---------- interface for Members 2, 3, 4 ----------
    def validate_all(self):
        return v.validate_all(
            self.get_all("rooms"), self.get_all("classes"), self.get_all("slots")
        )

    def get_clean_data(self):
        """Validated data as {'rooms', 'classes', 'slots'} DataFrames, numeric columns as int.

        Raises ValidationError if anything is wrong, so callers never see bad data.
        """
        errors = self.validate_all()
        if errors:
            raise v.ValidationError("\n".join(errors))
        data = {t: self.get_all(t) for t in TABLES}
        for t, cfg in TABLES.items():
            for col in cfg["numeric"]:
                data[t][col] = data[t][col].astype(int)
        return data

    def oversized_classes(self):
        d = self.get_clean_data()
        return v.find_oversized_classes(d["classes"], d["rooms"])


if __name__ == "__main__":
    dm = DataManager()
    data = dm.get_clean_data()
    for name, df in data.items():
        print(f"\n{name} ({len(df)} rows)\n{df.to_string(index=False)}")
    print("\nClasses too large for every room:", dm.oversized_classes() or "none")
