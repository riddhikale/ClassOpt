"""Validation rules for ClassOpt input data (Member 1)."""
import pandas as pd

ROOM_COLS = ["room_id", "capacity", "facilities"]
CLASS_COLS = ["class_id", "class_name", "students", "instructor", "student_group", "fixed_slot"]
SLOT_COLS = ["slot_id", "day", "time"]


class ValidationError(Exception):
    """Raised when input data breaks a rule."""


def _missing_columns(df, cols, table):
    return [f"{table}: missing column '{c}'" for c in cols if c not in df.columns]


def _id_errors(df, col, table):
    ids = df[col].fillna("").astype(str).str.strip()
    empty = ids == ""
    errors = []
    if empty.any():
        errors.append(f"{table}: {int(empty.sum())} row(s) have an empty {col}")
    valid = ids[~empty]
    for dup in valid[valid.duplicated()].unique():
        errors.append(f"{table}: duplicate {col} '{dup}'")
    return errors


def _text_errors(df, col, id_col, table):
    blank = df[col].fillna("").astype(str).str.strip() == ""
    return [f"{table}: {df.at[i, id_col]} has an empty {col}" for i in df.index[blank]]


def _positive_int_errors(df, col, id_col, table):
    nums = pd.to_numeric(df[col], errors="coerce").astype(float)
    bad = nums.isna() | (nums <= 0) | (nums % 1 != 0)
    return [
        f"{table}: {df.at[i, id_col]} has invalid {col} '{df.at[i, col]}' "
        f"(need a positive whole number)"
        for i in df.index[bad]
    ]


def validate_rooms(df):
    errors = _missing_columns(df, ROOM_COLS, "rooms")
    if errors:
        return errors
    return _id_errors(df, "room_id", "rooms") + _positive_int_errors(
        df, "capacity", "room_id", "rooms"
    )


def validate_classes(df):
    errors = _missing_columns(df, CLASS_COLS, "classes")
    if errors:
        return errors
    return (
        _id_errors(df, "class_id", "classes")
        + _text_errors(df, "class_name", "class_id", "classes")
        + _positive_int_errors(df, "students", "class_id", "classes")
    )


def validate_slots(df):
    errors = _missing_columns(df, SLOT_COLS, "time_slots")
    if errors:
        return errors
    return (
        _id_errors(df, "slot_id", "time_slots")
        + _text_errors(df, "day", "slot_id", "time_slots")
        + _text_errors(df, "time", "slot_id", "time_slots")
    )


def validate_all(rooms, classes, slots):
    """Run every single-table check plus cross-table checks. Returns a list of errors."""
    errors = validate_rooms(rooms) + validate_classes(classes) + validate_slots(slots)
    if errors:
        return errors
    slot_ids = set(slots["slot_id"].astype(str).str.strip())
    for _, row in classes.iterrows():
        fixed = str(row["fixed_slot"]).strip()
        if fixed and fixed not in slot_ids:
            errors.append(f"classes: {row['class_id']} has fixed_slot '{fixed}' not found in time_slots")
    return errors


def find_oversized_classes(classes, rooms):
    """Class IDs whose strength exceeds every room's capacity (cannot be allocated)."""
    max_cap = pd.to_numeric(rooms["capacity"], errors="coerce").max()
    students = pd.to_numeric(classes["students"], errors="coerce")
    return classes.loc[students > max_cap, "class_id"].tolist()
