"""SQLite storage backend for ClassOpt (Member 1).

DataManager can store its tables in CSV files (default) or in this SQLite database.
Both give identical results, so other modules never need to know which one is used.

    from src.data_manager import DataManager
    dm = DataManager.from_sqlite("classopt.db")

Fill a database from CSV files (validated first):
    python -m src.database --from-csv data_large --db classopt.db
"""
import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd

from . import validation as v

# table -> (id column, all columns)
SCHEMA = {
    "rooms": ("room_id", v.ROOM_COLS),
    "classes": ("class_id", v.CLASS_COLS),
    "slots": ("slot_id", v.SLOT_COLS),
}
CSV_FILES = {"rooms": "classrooms.csv", "classes": "classes.csv", "slots": "time_slots.csv"}
VALIDATORS = {
    "rooms": v.validate_rooms,
    "classes": v.validate_classes,
    "slots": v.validate_slots,
}


class SQLiteStore:
    """Stores each table as a SQLite table. Table and column names come only from SCHEMA;
    all values are passed as '?' parameters, never pasted into SQL."""

    def __init__(self, db_path="classopt.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self):
        with closing(self._connect()) as conn, conn:
            for table, (id_col, cols) in SCHEMA.items():
                defs = ", ".join(
                    f"{c} TEXT PRIMARY KEY" if c == id_col else f"{c} TEXT NOT NULL DEFAULT ''"
                    for c in cols
                )
                conn.execute(f"CREATE TABLE IF NOT EXISTS {table} ({defs})")

    def read(self, table):
        cols = SCHEMA[table][1]
        with closing(self._connect()) as conn:
            rows = conn.execute(
                f"SELECT {', '.join(cols)} FROM {table} ORDER BY rowid"
            ).fetchall()
        return pd.DataFrame(rows, columns=cols, dtype=str)

    def write(self, table, df):
        """Replace the whole table in one transaction (all rows saved, or none)."""
        cols = SCHEMA[table][1]
        rows = [tuple(str(x) for x in r) for r in df[cols].itertuples(index=False, name=None)]
        marks = ", ".join("?" * len(cols))
        with closing(self._connect()) as conn, conn:
            conn.execute(f"DELETE FROM {table}")
            conn.executemany(
                f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({marks})", rows
            )


def import_csv(data_dir, db_path="classopt.db"):
    """Load the three CSV files into the database, replacing its contents.

    Every file is validated first; if any has an error nothing is written.
    """
    frames = {}
    for table, filename in CSV_FILES.items():
        df = pd.read_csv(Path(data_dir) / filename, dtype=str, keep_default_na=False)
        errors = VALIDATORS[table](df)
        if errors:
            raise v.ValidationError(f"{filename}: " + "; ".join(errors))
        frames[table] = df.apply(lambda col: col.str.strip())
    store = SQLiteStore(db_path)
    for table, df in frames.items():
        store.write(table, df)
    return store


def main():
    p = argparse.ArgumentParser(description="Load CSV data into a ClassOpt SQLite database.")
    p.add_argument("--from-csv", required=True, help="folder with the three CSV files")
    p.add_argument("--db", default="classopt.db", help="database file to create or replace")
    a = p.parse_args()
    store = import_csv(a.from_csv, a.db)
    for table in SCHEMA:
        print(f"{table}: {len(store.read(table))} rows")
    print(f"Saved to {a.db}")


if __name__ == "__main__":
    main()
