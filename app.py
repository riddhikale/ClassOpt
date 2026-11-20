import html
from pathlib import Path

import pandas as pd
import plotly.express as px
<<<<<<< HEAD
import streamlit as st

from src.data_manager import DataManager
from src.allocation import allocate_classes
from src.validation import ValidationError


=======
import html
 
from src.data_manager import DataManager
from src.allocation import allocate_classes
from src.validation import ValidationError
 
 
# =========================================================
# PAGE CONFIGURATION
# =========================================================
>>>>>>> 7bfeb50ee1dd3f8d78c1979e937619bf2ba6dbb0
st.set_page_config(
    page_title="ClassOpt | Classroom Planner",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed",
)
<<<<<<< HEAD

PAGES = ["Dashboard", "Allocation", "Records"]
ACCENT = "#0F766E"
INK = "#0F172A"


def find_datasets():
    """List every folder next to app.py that holds a classrooms.csv, 'data' first."""
    root = Path(__file__).parent
    found = sorted(
        p.name for p in root.iterdir() if p.is_dir() and (p / "classrooms.csv").exists()
    )
    if "data" in found:
        found.remove("data")
        found.insert(0, "data")
    return found or ["data", "data_large", "data_stress", "data_test"]


DATASETS = find_datasets()

LOGO_SVG = """
<svg width="46" height="46" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <rect width="44" height="44" rx="11" fill="#0F766E" stroke="rgba(255,255,255,0.25)"/>
  <rect x="9" y="9" width="11" height="11" rx="3" fill="#FFFFFF"/>
  <rect x="24" y="9" width="11" height="11" rx="3" fill="#FFFFFF" opacity="0.55"/>
  <rect x="9" y="24" width="11" height="11" rx="3" fill="#FFFFFF" opacity="0.55"/>
  <rect x="24" y="24" width="11" height="11" rx="3" fill="#F59E0B"/>
</svg>
"""

LOGO_SVG = "".join(line.strip() for line in LOGO_SVG.splitlines())


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&display=swap');

    :root {
        color-scheme: light;
        --navy: #0B2545;
        --ink: #0F172A;
        --muted: #556275;
        --line: #DCE3EC;
        --bg: #F2F5F9;
        --surface: #FFFFFF;
        --accent: #0F766E;
        --accent-dark: #0B5F58;
        --accent-soft: #E0F2F0;
        --amber: #F59E0B;
        --warn: #B45309;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Instrument Sans', system-ui, sans-serif;
        color: var(--ink);
    }
    .stApp { background: var(--bg); }
    [data-testid="stHeader"] { background: transparent; }
    .block-container { max-width: 1280px; padding-top: 1.6rem; padding-bottom: 3rem; }

    /* No sidebar: everything lives on the page */
    [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] { display: none !important; }

    /* Top bar */
    .topbar {
        display: flex; align-items: center; gap: 14px;
        background: var(--navy); border-radius: 14px; padding: 14px 22px;
    }
    .tb-name { color: #FFFFFF; font-size: 24px; font-weight: 700; letter-spacing: -0.5px; line-height: 1.1; }
    .tb-tag { color: #B9C7DB; font-size: 13px; margin-top: 3px; }

    /* Navigation (pill buttons) */
    div[role="radiogroup"] { gap: 8px; }
    div[role="radiogroup"] > label {
        background: var(--surface); border: 1px solid var(--line);
        border-radius: 10px; padding: 8px 20px; margin: 0; cursor: pointer;
    }
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] > label p { font-weight: 600; }
    div[role="radiogroup"] > label:has(input:checked) {
        background: var(--accent); border-color: var(--accent);
    }
    div[role="radiogroup"] > label:has(input:checked) p { color: #FFFFFF !important; }

    /* Section headings */
    .page-head { margin: 22px 0 14px 0; }
    .page-title { font-size: 22px; font-weight: 700; letter-spacing: -0.4px; margin: 0; }
    .page-sub { color: var(--muted); font-size: 14px; margin-top: 3px; max-width: 700px; }
    .block-title { font-size: 16px; font-weight: 650; margin: 24px 0 3px 0; }
    .block-sub { color: var(--muted); font-size: 13px; margin-bottom: 10px; }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: var(--surface); border: 1px solid var(--line);
        border-left: 4px solid var(--accent);
        border-radius: 12px; padding: 14px 18px;
    }
    [data-testid="stMetricLabel"] p { color: var(--muted) !important; font-size: 13px !important; }
    [data-testid="stMetricValue"] { font-weight: 700 !important; letter-spacing: -0.5px; }

    /* Buttons, forms, tables */
    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
        border-radius: 8px; font-weight: 600; min-height: 42px;
    }
    .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
        background: var(--accent); border-color: var(--accent);
    }
    .stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
        background: var(--accent-dark); border-color: var(--accent-dark);
    }
    div[data-testid="stForm"] { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
    div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
    div[data-testid="stAlert"] { border-radius: 10px; }

    /* Panels and checklist */
    .panel { background: var(--surface); border: 1px solid var(--line); border-radius: 12px; padding: 6px 18px; }
    .check { display: flex; gap: 10px; padding: 11px 0; border-bottom: 1px solid var(--line); font-size: 14px; color: var(--ink); }
    .check:last-child { border-bottom: 0; }
    .dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex: none; }
    .dot.ok { background: var(--accent); }
    .dot.warn { background: var(--amber); }
    .empty-state {
        background: var(--surface); border: 1px dashed #B8C4D4; border-radius: 12px;
        padding: 26px; text-align: center; color: var(--muted); font-size: 14px;
    }

    /* Timetable */
    .tt-wrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 12px; }
    table.tt { border-collapse: collapse; width: 100%; font-size: 13px; }
    table.tt th {
        text-align: left; padding: 10px 12px; font-weight: 600; color: var(--muted);
        background: #F6F8FB; border-bottom: 1px solid var(--line); white-space: nowrap;
    }
    table.tt td { padding: 6px; border-bottom: 1px solid var(--line); border-right: 1px solid var(--line); vertical-align: top; min-width: 130px; }
    table.tt tr:last-child td, table.tt tr:last-child th { border-bottom: 0; }
    table.tt td:last-child { border-right: 0; }
    table.tt th.room { background: #F6F8FB; color: var(--ink); border-right: 1px solid var(--line); }
    table.tt th.room small { display: block; font-weight: 500; color: var(--muted); }
    .cell { border-radius: 7px; padding: 7px 9px; color: var(--ink); }
    .cell b { display: block; font-weight: 650; line-height: 1.25; }
    .cell span { font-size: 11.5px; color: #12302E; }
    .empty { color: #A5B1C2; padding: 7px 9px; }
    .legend { font-size: 12px; color: var(--muted); margin-top: 8px; }

    /* ---- Readability: dark text on light surfaces whatever the browser theme ---- */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stCheckbox"] label,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stAlert"] p,
    [data-testid="stToast"] p { color: var(--ink) !important; }
    [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }

    input, textarea, [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
        color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; background: #FFFFFF !important;
    }
    input::placeholder, textarea::placeholder {
        color: #8793A5 !important; -webkit-text-fill-color: #8793A5 !important; opacity: 1 !important;
    }
    [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
        background: #FFFFFF !important; border-color: var(--line) !important;
    }
    [data-baseweb="select"] *, [data-testid="stNumberInput"] button { color: var(--ink) !important; fill: var(--ink) !important; }
    [data-testid="stNumberInput"] button { background: #F2F5F9 !important; }
    [data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"],
    [role="listbox"], [role="option"] { background: #FFFFFF !important; color: var(--ink) !important; }
    [role="option"]:hover, [role="option"][aria-selected="true"] { background: var(--accent-soft) !important; }

    [data-testid="stTabs"] button p { color: var(--muted) !important; font-weight: 600; }
    [data-testid="stTabs"] button[aria-selected="true"] p { color: var(--accent) !important; }
    [data-testid="stExpander"] details { background: #FFFFFF; border-color: var(--line); border-radius: 10px; }

    .stButton > button[kind="secondary"], .stDownloadButton > button { background: #FFFFFF; border: 1px solid var(--line); }
    .stButton > button[kind="secondary"] *, .stDownloadButton > button * { color: var(--ink) !important; }
    .stButton > button[kind="primary"] *, .stFormSubmitButton > button[kind="primary"] * { color: #FFFFFF !important; }
    .stButton > button:disabled { opacity: 0.5; }

    @media (max-width: 700px) {
        .tb-name { font-size: 20px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def page_header(title, subtitle, chip=None):
    st.markdown(
        f"""
        <div class="page-head">
            <h1 class="page-title">{html.escape(title)}</h1>
            <div class="page-sub">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def block(title, subtitle=""):
    st.markdown(
        f"""
        <div class="block-title">{html.escape(title)}</div>
        <div class="block-sub">{html.escape(subtitle)}</div>
        """,
        unsafe_allow_html=True,
    )


def clear_allocation_result():
    st.session_state["allocation_result"] = None


def go_to(page):
    st.session_state["page"] = page


def run_action(action, success_message):
    """Run a data change, reset any stale allocation, and refresh the page."""
    try:
        action()
        clear_allocation_result()
        st.toast(success_message, icon="✅")
        st.rerun()
    except (ValidationError, KeyError) as e:
        st.error(str(e))


def search_filter(df, label, key):
    query = st.text_input(label, key=key, placeholder="Search…", label_visibility="collapsed")
    if query:
        mask = df.astype(str).apply(
            lambda col: col.str.contains(query, case=False, na=False)
        ).any(axis=1)
        return df[mask]
    return df


def style_chart(fig, height):
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Instrument Sans, sans-serif", color=INK),
        margin=dict(l=10, r=10, t=20, b=10),
        height=height,
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="#E8EDF3")
    fig.update_yaxes(gridcolor="#E8EDF3")
    return fig


def readiness_checks(rooms, classes, slots):
    seats = pd.to_numeric(rooms["capacity"], errors="coerce")
    sizes = pd.to_numeric(classes["students"], errors="coerce")
    checks = []

    too_big = classes[sizes > seats.max()] if len(seats.dropna()) else classes.iloc[0:0]
    if len(too_big):
        names = ", ".join(too_big["class_id"].astype(str).head(4))
        more = "…" if len(too_big) > 4 else ""
        checks.append(("warn", f"{len(too_big)} class(es) are larger than every room ({names}{more})."))
    else:
        checks.append(("ok", "Every class fits in at least one room."))

    fixed = classes["fixed_slot"].astype(str).str.strip()
    fixed = fixed[fixed != ""]
    crowded = fixed.value_counts()
    crowded = crowded[crowded > len(rooms)]
    if len(crowded):
        checks.append(("warn", f"More classes are fixed to {', '.join(crowded.index.astype(str)[:4])} than there are rooms."))
    else:
        checks.append(("ok", f"{len(fixed)} class(es) have a fixed slot, and none overload a slot."))

    combos = len(rooms) * len(slots)
    if len(classes) > combos:
        checks.append(("warn", "There are more classes than room and slot combinations."))
    else:
        checks.append(("ok", f"{combos} room and slot combinations for {len(classes)} classes."))
    return checks


def summarize_result(result, total_classes):
    assignments = pd.DataFrame(result["assignments"])
    unallocated = pd.DataFrame(result["unallocated"])
    placed = len(assignments)
    rate = placed / total_classes * 100 if total_classes else 0
    avg_use = 0
    if not assignments.empty:
        students = pd.to_numeric(assignments["students"], errors="coerce").sum()
        capacity = pd.to_numeric(assignments["capacity"], errors="coerce").sum()
        avg_use = students / capacity * 100 if capacity else 0
    return assignments, unallocated, placed, rate, avg_use


def allocation_metrics(placed, total, unplaced, rate, avg_use):
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Classes placed", f"{placed} of {total}")
    m2.metric("Not placed", unplaced)
    m3.metric("Placement rate", f"{rate:.0f}%")
    m4.metric("Average seat use", f"{avg_use:.0f}%")


def usage_chart(assignments):
    usage = (
        assignments.assign(
            students=pd.to_numeric(assignments["students"], errors="coerce"),
            capacity=pd.to_numeric(assignments["capacity"], errors="coerce"),
        )
        .groupby("room_id")
        .agg(students=("students", "sum"), capacity=("capacity", "sum"))
        .reset_index()
    )
    usage["utilization"] = usage["students"] / usage["capacity"] * 100
    usage = usage.sort_values("utilization")
    fig = px.bar(
        usage,
        x="utilization",
        y="room_id",
        orientation="h",
        text=usage["utilization"].round(0).astype(int).astype(str) + "%",
        labels={"room_id": "Classroom", "utilization": "Seats filled (%)"},
    )
    fig.update_traces(marker_color=ACCENT, textposition="outside", marker_line_width=0)
    fig.update_xaxes(range=[0, 112], ticksuffix="%")
    return style_chart(fig, max(260, 32 * len(usage) + 70))


def timetable_html(assignments, rooms, slots, compact=True):
    """Rooms down the side, time slots across the top, one card per class."""
    if assignments.empty or not {"room_id", "slot_id"}.issubset(assignments.columns):
        return None

    label_col = next((c for c in ("class_name", "class_id") if c in assignments.columns), None)
    lookup = {(r["room_id"], r["slot_id"]): r for _, r in assignments.iterrows()}
    room_cap = dict(zip(rooms["room_id"], pd.to_numeric(rooms["capacity"], errors="coerce")))

    slot_ids = slots["slot_id"].tolist()
    room_ids = rooms["room_id"].tolist()
    if compact:
        used_slots = set(assignments["slot_id"])
        used_rooms = set(assignments["room_id"])
        slot_ids = [s for s in slot_ids if s in used_slots]
        room_ids = [r for r in room_ids if r in used_rooms]

    head = "".join(f"<th>{html.escape(str(s))}</th>" for s in slot_ids)
    rows = []
    for room_id in room_ids:
        cap = room_cap.get(room_id)
        cap_txt = f"{int(cap)} seats" if pd.notna(cap) else ""
        cells = []
        for slot_id in slot_ids:
            row = lookup.get((room_id, slot_id))
            if row is None:
                cells.append('<td><div class="empty">Free</div></td>')
                continue
            students = pd.to_numeric(row.get("students"), errors="coerce")
            capacity = pd.to_numeric(row.get("capacity"), errors="coerce")
            use = (students / capacity) if capacity and pd.notna(capacity) else 0
            alpha = 0.14 + 0.5 * min(max(use, 0), 1)
            name = html.escape(str(row[label_col])) if label_col else "Class"
            detail = (
                f"{int(students)} of {int(capacity)} seats"
                if pd.notna(students) and pd.notna(capacity)
                else ""
            )
            cells.append(
                f'<td><div class="cell" style="background: rgba(15,118,110,{alpha:.2f})">'
                f"<b>{name}</b><span>{detail}</span></div></td>"
            )
        rows.append(
            f'<tr><th class="room">{html.escape(str(room_id))}<small>{cap_txt}</small></th>'
            f'{"".join(cells)}</tr>'
        )

    return (
        '<div class="tt-wrap"><table class="tt">'
        f'<thead><tr><th class="room">Room</th>{head}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
        '<div class="legend">Darker cells mean fuller rooms.</div>'
    )


st.session_state.setdefault("page", "Dashboard")

brand_col, dataset_col = st.columns([4, 1.2], vertical_alignment="bottom", gap="medium")

with brand_col:
    topbar = (
        '<div class="topbar">'
        + LOGO_SVG
        + "<div>"
        + '<div class="tb-name">ClassOpt</div>'
        + '<div class="tb-tag">Classroom occupancy and space allocation</div>'
        + "</div></div>"
    )
    st.markdown(topbar, unsafe_allow_html=True)

with dataset_col:
    dataset = st.selectbox(
        "Dataset",
        DATASETS,
        help="Choose which set of classrooms, classes and slots to work with.",
    )

if st.session_state.get("selected_dataset") != dataset:
    st.session_state["selected_dataset"] = dataset
    st.session_state["allocation_result"] = None

st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
st.radio("Navigate", PAGES, key="page", horizontal=True, label_visibility="collapsed")


def dashboard_page(rooms, classes, slots):
    seats = pd.to_numeric(rooms["capacity"], errors="coerce")
    sizes = pd.to_numeric(classes["students"], errors="coerce")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Classrooms", len(rooms))
    m2.metric("Classes", len(classes))
    m3.metric("Time slots", len(slots))
    m4.metric("Total seats", int(seats.sum()) if len(seats) else 0)

    left, right = st.columns([3, 2], gap="large")

    with left:
        block("Class sizes", "How many students each class has, compared with your biggest room")
        if len(sizes.dropna()):
            fig = px.histogram(sizes.dropna(), nbins=12, labels={"value": "Students per class"})
            fig.update_traces(marker_color=ACCENT, marker_line_width=0)
            if len(seats.dropna()):
                fig.add_vline(
                    x=seats.max(),
                    line_dash="dash",
                    line_color="#B45309",
                    annotation_text=f"Largest room: {int(seats.max())}",
                    annotation_position="top left",
                )
            fig.update_layout(yaxis_title="Classes")
            st.plotly_chart(style_chart(fig, 300), width="stretch")
        else:
            st.markdown('<div class="empty-state">Add classes to see how their sizes compare with your rooms.</div>', unsafe_allow_html=True)

    with right:
        block("Readiness checks", "Things that may stop a class from getting a room")
        items = "".join(
            f'<div class="check"><span class="dot {kind}"></span><span>{html.escape(text)}</span></div>'
            for kind, text in readiness_checks(rooms, classes, slots)
        )
        st.markdown(f'<div class="panel">{items}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        st.button(
            "Go to allocation",
            type="primary",
            width="stretch",
            on_click=go_to,
            args=("Allocation",),
        )

    block("Latest allocation", "Results from the most recent run on this dataset")
    result = st.session_state.get("allocation_result")
    if result is None:
        st.markdown(
            '<div class="empty-state">No allocation yet. Open <b>Allocation</b> and select '
            "<b>Run allocation</b>. Editing any record clears the previous result.</div>",
            unsafe_allow_html=True,
        )
        return

    assignments, unallocated, placed, rate, avg_use = summarize_result(result, len(classes))
    allocation_metrics(placed, len(classes), len(unallocated), rate, avg_use)

    a, b = st.columns([3, 2], gap="large")
    with a:
        block("Seats filled by room", "Share of seats filled across all sessions in each room")
        if assignments.empty:
            st.info("No classes were placed.")
        else:
            st.plotly_chart(usage_chart(assignments), width="stretch")
    with b:
        block("Classes not placed", "These need a bigger room or a different slot")
        if unallocated.empty:
            st.success("Every class has a room and a time slot.")
        else:
            st.dataframe(unallocated, width="stretch", hide_index=True)


def records_page(dm, rooms, classes, slots):
    page_header(
        "Records",
        "Browse, add, edit and delete classrooms and classes.",
    )

    kind = st.radio(
        "Record type",
        ["Classrooms", "Classes"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if kind == "Classrooms":
        rooms_records(dm, rooms)
    else:
        classes_records(dm, classes, slots)

    with st.expander("View time slots"):
        st.dataframe(slots, width="stretch", hide_index=True)


def rooms_records(dm, rooms):
    shown = search_filter(rooms, "Search classrooms", "search_rooms")
    st.caption(f"Showing {len(shown)} of {len(rooms)} classrooms")
    st.dataframe(shown, width="stretch", hide_index=True)

    add_tab, edit_tab, delete_tab = st.tabs(["Add classroom", "Edit classroom", "Delete classroom"])

    with add_tab:
        with st.form("add_classroom_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            room_id = c1.text_input("Classroom ID", placeholder="R107")
            capacity = c2.number_input("Capacity (seats)", min_value=1, step=1, value=40)
            facilities = st.text_input("Facilities", placeholder="Projector, smart board")

            if st.form_submit_button("Add classroom", type="primary", width="stretch"):
                run_action(
                    lambda: dm.add(
                        "rooms",
                        {"room_id": room_id, "capacity": str(capacity), "facilities": facilities},
                    ),
                    "Classroom added",
                )

    room_ids = rooms["room_id"].tolist()

    with edit_tab:
        if not room_ids:
            st.info("There are no classrooms yet. Add one in the first tab.")
        else:
            selected = st.selectbox("Classroom", room_ids, key="edit_room_select")
            current = dm.get("rooms", selected)
            with st.form("update_room_form"):
                c1, c2 = st.columns(2)
                new_capacity = c1.number_input(
                    "Capacity (seats)",
                    min_value=1,
                    value=int(current["capacity"]),
                    key=f"room_cap_{selected}",
                )
                new_facilities = c2.text_input(
                    "Facilities",
                    value=current["facilities"],
                    key=f"room_fac_{selected}",
                )
                if st.form_submit_button("Save changes", type="primary", width="stretch"):
                    run_action(
                        lambda: dm.update(
                            "rooms",
                            selected,
                            {"capacity": str(new_capacity), "facilities": new_facilities},
                        ),
                        "Changes saved",
                    )

    with delete_tab:
        if not room_ids:
            st.info("There are no classrooms to delete.")
        else:
            selected = st.selectbox("Classroom", room_ids, key="delete_room_select")
            st.warning(f"Deleting {selected} removes it from this dataset for good.")
            confirm = st.checkbox(f"Yes, delete {selected}", key="confirm_room_delete")
            if st.button("Delete classroom", disabled=not confirm, key="delete_room_button"):
                run_action(lambda: dm.delete("rooms", selected), "Classroom deleted")


def classes_records(dm, classes, slots):
    shown = search_filter(classes, "Search classes", "search_classes")
    st.caption(f"Showing {len(shown)} of {len(classes)} classes")
    st.dataframe(shown, width="stretch", hide_index=True)

    add_tab, edit_tab, delete_tab = st.tabs(["Add class", "Edit class", "Delete class"])
    slot_options = [""] + slots["slot_id"].tolist()

    with add_tab:
        with st.form("add_class_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            class_id = c1.text_input("Class ID", placeholder="C108")
            class_name = c2.text_input("Class name", placeholder="Java Programming")
            c3, c4 = st.columns(2)
            students = c3.number_input("Students", min_value=1, step=1, value=30)
            instructor = c4.text_input("Instructor", placeholder="Priya")
            c5, c6 = st.columns(2)
            student_group = c5.text_input("Student group", placeholder="IT Third Year")
            fixed_slot = c6.selectbox(
                "Fixed time slot",
                slot_options,
                help="Leave empty to let ClassOpt choose the slot.",
            )

            if st.form_submit_button("Add class", type="primary", width="stretch"):
                run_action(
                    lambda: dm.add(
                        "classes",
                        {
                            "class_id": class_id,
                            "class_name": class_name,
                            "students": str(students),
                            "instructor": instructor,
                            "student_group": student_group,
                            "fixed_slot": fixed_slot,
                        },
                    ),
                    "Class added",
                )

    class_ids = classes["class_id"].tolist()

    with edit_tab:
        if not class_ids:
            st.info("There are no classes yet. Add one in the first tab.")
        else:
            selected = st.selectbox("Class", class_ids, key="edit_class_select")
            current = dm.get("classes", selected)
            current_slot = current["fixed_slot"]
            slot_index = slot_options.index(current_slot) if current_slot in slot_options else 0

            with st.form("update_class_form"):
                c1, c2 = st.columns(2)
                new_name = c1.text_input(
                    "Class name", value=current["class_name"], key=f"cls_name_{selected}"
                )
                new_students = c2.number_input(
                    "Students",
                    min_value=1,
                    value=int(current["students"]),
                    key=f"cls_students_{selected}",
                )
                c3, c4 = st.columns(2)
                new_instructor = c3.text_input(
                    "Instructor", value=current["instructor"], key=f"cls_instr_{selected}"
                )
                new_group = c4.text_input(
                    "Student group", value=current["student_group"], key=f"cls_group_{selected}"
                )
                new_slot = st.selectbox(
                    "Fixed time slot",
                    slot_options,
                    index=slot_index,
                    key=f"cls_slot_{selected}",
                )
                if st.form_submit_button("Save changes", type="primary", width="stretch"):
                    run_action(
                        lambda: dm.update(
                            "classes",
                            selected,
                            {
                                "class_name": new_name,
                                "students": str(new_students),
                                "instructor": new_instructor,
                                "student_group": new_group,
                                "fixed_slot": new_slot,
                            },
                        ),
                        "Changes saved",
                    )

    with delete_tab:
        if not class_ids:
            st.info("There are no classes to delete.")
        else:
            selected = st.selectbox("Class", class_ids, key="delete_class_select")
            st.warning(f"Deleting {selected} removes it from this dataset for good.")
            confirm = st.checkbox(f"Yes, delete {selected}", key="confirm_class_delete")
            if st.button("Delete class", disabled=not confirm, key="delete_class_button"):
                run_action(lambda: dm.delete("classes", selected), "Class deleted")



def allocation_page(rooms, classes, slots):
    page_header(
        "Allocation",
        "Assign every class to a room and time slot. Larger classes are placed first, "
        "fixed slots are kept, and clashes are avoided.",
    )

    if st.button("Run allocation", type="primary"):
        try:
            with st.spinner("Placing classes…"):
                st.session_state["allocation_result"] = allocate_classes(rooms, classes, slots)
        except (ValidationError, KeyError, ValueError) as e:
            st.error(f"Could not run the allocation: {e}")

    result = st.session_state.get("allocation_result")
    if result is None:
        st.markdown(
            '<div class="empty-state">No allocation yet. Select <b>Run allocation</b> to see the timetable.</div>',
            unsafe_allow_html=True,
        )
        return

    assignments, unallocated, placed, rate, avg_use = summarize_result(result, len(classes))
    allocation_metrics(placed, len(classes), len(unallocated), rate, avg_use)

    if len(unallocated):
        st.warning(f"{len(unallocated)} class(es) could not be placed. Open the **Not placed** tab to see why.")
    else:
        st.success("Every class has a room and a time slot.")

    tab_tt, tab_list, tab_missing, tab_use = st.tabs(
        ["Timetable", "Assignments", "Not placed", "Room use"]
    )

    with tab_tt:
        compact = st.toggle(
            "Hide empty rooms and time slots",
            value=True,
            help="Turn off to see every room and slot, including the unused ones.",
        )
        grid = timetable_html(assignments, rooms, slots, compact=compact)
        if grid:
            st.markdown(grid, unsafe_allow_html=True)
        else:
            st.info("The timetable needs room and slot details in the results. See the Assignments tab.")

    with tab_list:
        if assignments.empty:
            st.info("No classes were placed.")
        else:
            st.dataframe(assignments, width="stretch", hide_index=True)
            st.download_button(
                "Download assignments (CSV)",
                assignments.to_csv(index=False).encode("utf-8"),
                file_name=f"classopt_{dataset}_assignments.csv",
                mime="text/csv",
            )

    with tab_missing:
        if unallocated.empty:
            st.success("Nothing to review. All classes were placed.")
        else:
            st.dataframe(unallocated, width="stretch", hide_index=True)

    with tab_use:
        if assignments.empty:
            st.info("Room use appears once classes are placed.")
        else:
            st.plotly_chart(usage_chart(assignments), width="stretch")
            st.caption("Share of seats filled across all sessions held in each room.")


try:
    dm = DataManager(dataset)
    data = dm.get_clean_data()
    rooms, classes, slots = data["rooms"], data["classes"], data["slots"]

    page = st.session_state["page"]
    if page == "Dashboard":
        dashboard_page(rooms, classes, slots)
    elif page == "Records":
        records_page(dm, rooms, classes, slots)
    else:
        allocation_page(rooms, classes, slots)

except (ValidationError, KeyError, ValueError) as e:
    st.error(f"Could not load the data: {e}")
=======
 
# =========================================================
# SESSION STATE
# =========================================================
if "allocation_result" not in st.session_state:
    st.session_state["allocation_result"] = None
 
if "selected_dataset" not in st.session_state:
    st.session_state["selected_dataset"] = None
 
 
def clear_allocation_result():
    st.session_state["allocation_result"] = None
 
 
# =========================================================
# BLUE UI + BLUE TABLE THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
 
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #F5F8FE;
    color: #172B4D;
}
.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
 
/* NAVY SIDEBAR */
[data-testid="stSidebar"] {
    background: #102344;
}
[data-testid="stSidebar"] * {
    color: #EAF1FF;
}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
.sidebar-brand {
    padding: 12px 5px 25px;
}
.sidebar-brand-icon {
    font-size: 35px;
}
.sidebar-brand-name {
    font-size: 27px;
    font-weight: 800;
    color: #FFFFFF;
}
.sidebar-caption {
    color: #B8C9E5;
    font-size: 11px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}
.sidebar-section {
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 700;
    margin: 8px 0 5px;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(220,232,255,0.18) !important;
}
 
/* SIDEBAR DATASET SELECT */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #D6E0F0 !important;
    border-radius: 9px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: #172B4D !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #234D91 !important;
}
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] {
    background: #FFFFFF !important;
    color: #172B4D !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: #EAF1FC !important;
    color: #172B4D !important;
}
 
/* HERO BANNER - BLUE */
.hero {
    padding: 34px 36px;
    border-radius: 20px;
    background: linear-gradient(115deg, #142B55 0%, #1D4E91 58%, #2874D0 100%);
    margin-bottom: 27px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 12px 28px rgba(24,62,117,0.13);
    position: relative;
    overflow: hidden;
}
.hero-kicker {
    color: #C8DDFB;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.hero-title {
    color: #FFFFFF;
    font-size: clamp(27px, 4vw, 39px);
    font-weight: 800;
    margin-top: 8px;
    line-height: 1.2;
}
.hero-subtitle {
    color: #E2ECFC;
    font-size: 14px;
    margin-top: 10px;
    max-width: 760px;
    line-height: 1.65;
}
 
/* HEADINGS */
.section-title {
    font-size: 21px;
    font-weight: 800;
    color: #172B4D;
    margin-top: 25px;
    margin-bottom: 3px;
}
.section-caption {
    font-size: 12px;
    color: #8290A6;
    margin-bottom: 15px;
}
 
/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E4EAF3;
    border-radius: 16px;
    padding: 19px;
    box-shadow: 0 5px 16px rgba(26,54,93,0.045);
}
[data-testid="stMetricLabel"] p {
    color: #7B8AA3 !important;
    font-weight: 600 !important;
    font-size: 12px !important;
}
[data-testid="stMetricValue"] {
    color: #172B4D !important;
    font-weight: 800 !important;
}
 
/* TABS */
[data-testid="stTabs"] button {
    font-weight: 650;
    color: #71819A;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #315F9F !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: #315F9F !important;
}
 
/* TABLES - BLUE HEADER, CLEAN WHITE / PALE-BLUE BODY */
.classopt-table-wrapper {
    width: 100%;
    overflow-x: auto;
    background: #FFFFFF;
    border: 1px solid #DCE7F5;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(30, 67, 115, 0.04);
}
.classopt-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Sans', sans-serif;
    background: #FFFFFF;
}
.classopt-table th {
    background: #244B78;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 650;
    text-align: left;
    padding: 15px 18px;
    white-space: nowrap;
    border: none;
}
.classopt-table td {
    background: #FFFFFF;
    color: #344B68;
    font-size: 13px;
    font-weight: 500;
    padding: 14px 18px;
    border-bottom: 1px solid #E5EDF7;
    white-space: nowrap;
}
.classopt-table tbody tr:nth-child(even) td {
    background: #F7FAFF;
}
.classopt-table tbody tr:hover td {
    background: #EAF2FC;
}
.classopt-table tbody tr:last-child td {
    border-bottom: none;
}
 
/* FORMS */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E3EAF4;
    border-radius: 15px;
    padding: 20px;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
    color: #172B4D !important;
    background: #FFFFFF !important;
    border-radius: 9px !important;
    border: 1px solid #D6E0F0 !important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #FFFFFF;
    color: #172B4D;
}
[data-testid="stWidgetLabel"] p {
    color: #526783 !important;
    font-weight: 600 !important;
}
 
/* BUTTONS */
.stButton > button,
.stFormSubmitButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 700;
    transition: 0.2s ease;
}
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #245CA6 !important;
    border: 1px solid #245CA6 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(36,92,166,0.16);
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #194982 !important;
    border-color: #194982 !important;
}
.stButton > button:hover {
    border-color: #6E91C1;
}
 
/* ALERTS AND PROGRESS */
div[data-testid="stAlert"] {
    border-radius: 12px;
}
div[data-testid="stProgress"] > div > div {
    background: #315F9F !important;
}
 
/* REMOVE UNWANTED TOP LINE */
[data-testid="stHeader"],
[data-testid="stToolbar"] {
    border-bottom: 0 !important;
    box-shadow: none !important;
}
[data-testid="stMainBlockContainer"] {
    border-top: 0 !important;
}
 
/* FOOTER */
.footer {
    text-align: center;
    color: #8998AE;
    font-size: 11px;
    padding-top: 30px;
}
</style>
""", unsafe_allow_html=True)
 
 
# =========================================================
# REUSABLE FUNCTIONS
# =========================================================
def section_heading(title, caption=""):
    st.markdown(
        f'<div class="section-title">{html.escape(str(title))}</div>'
        f'<div class="section-caption">{html.escape(str(caption))}</div>',
        unsafe_allow_html=True,
    )
 
 
def show_table(df):
    if df is None or df.empty:
        st.info("No records available.")
        return
 
    headers = "".join(
        f"<th>{html.escape(str(col))}</th>" for col in df.columns
    )
    rows = []
    for _, row in df.iterrows():
        cells = "".join(
            f"<td>{html.escape(str(value))}</td>" for value in row
        )
        rows.append(f"<tr>{cells}</tr>")
 
    table_html = f"""
    <div class="classopt-table-wrapper">
      <table class="classopt-table">
        <thead><tr>{headers}</tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)
 
 
def show_utilization_chart(assignments):
    if assignments is None or assignments.empty:
        st.info("No allocation data available for the chart.")
        return
 
    room_usage = (
        assignments.groupby("room_id")
        .agg(
            students=("students", "sum"),
            capacity=("capacity", "sum"),
        )
        .reset_index()
    )
    room_usage["utilization"] = (
        room_usage["students"] / room_usage["capacity"].replace(0, 1) * 100
    )
 
    fig = px.bar(
        room_usage,
        x="room_id",
        y="utilization",
        text_auto=".1f",
        color="utilization",
        color_continuous_scale=["#DCEBFA", "#78A9DC", "#245CA6"],
        labels={
            "room_id": "Classroom",
            "utilization": "Utilization (%)",
        },
    )
    fig.update_layout(
        yaxis_range=[0, 100],
        yaxis_ticksuffix="%",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", color="#344B68"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=25, b=10),
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
 
 
def show_allocation_status_chart(allocated_count, unallocated_count):
    status_data = pd.DataFrame({
        "Status": ["Allocated", "Unallocated"],
        "Classes": [allocated_count, unallocated_count],
    })
    status_data = status_data[status_data["Classes"] > 0]
 
    if status_data.empty:
        st.info("No allocation status is available yet.")
        return
 
    fig = px.pie(
        status_data,
        names="Status",
        values="Classes",
        hole=0.62,
        color="Status",
        color_discrete_map={
            "Allocated": "#245CA6",
            "Unallocated": "#A9BBD3",
        },
    )
    fig.update_traces(
        textposition="inside",
        textinfo="label+percent",
        marker=dict(line=dict(color="#FFFFFF", width=3)),
    )
    fig.update_layout(
        showlegend=True,
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="DM Sans", color="#344B68"),
        margin=dict(l=10, r=10, t=20, b=10),
        legend_title_text="",
    )
    st.plotly_chart(fig, use_container_width=True)
 
 
# =========================================================
# SIDEBAR / NAVIGATION
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🏫</div>
        <div class="sidebar-brand-name">ClassOpt</div>
        <div class="sidebar-caption">Smart Space Planner</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("---")
    st.markdown("### Workspace")
 
    dataset = st.selectbox(
        "Select dataset",
        ["data", "data_large", "data_stress"],
    )
 
    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        ["🏠 Dashboard", "🏫 Manage Records", "📊 Allocation"],
        label_visibility="collapsed",
    )
 
    st.markdown("---")
    st.markdown("**What you can do**")
    st.markdown("• View classroom, class and slot data")
    st.markdown("• Add, update and delete records")
    st.markdown("• Generate classroom allocations")
    st.markdown("• Review utilization and unallocated classes")
    st.markdown("---")
    st.caption("ClassOpt • Classroom Allocation System")
 
 
# =========================================================
# RESET RESULTS WHEN DATASET CHANGES
# =========================================================
if st.session_state["selected_dataset"] != dataset:
    st.session_state["selected_dataset"] = dataset
    clear_allocation_result()
 
 
# =========================================================
# LOAD DATA AND RENDER APP
# =========================================================
try:
    dm = DataManager(dataset)
    data = dm.get_clean_data()
 
    rooms = data["rooms"]
    classes = data["classes"]
    slots = data["slots"]
 
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">Classroom Occupancy &amp; Space Allocation</div>
      <div class="hero-title">Plan smarter. Use space better.</div>
      <div class="hero-subtitle">
        Manage your academic spaces, organize class schedules and generate
        efficient classroom allocations from one dashboard.
      </div>
    </div>
    """, unsafe_allow_html=True)
 
    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------
    if page == "🏠 Dashboard":
        section_heading(
            "Dashboard overview",
            "A quick snapshot of your selected dataset",
        )
 
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🏫 Total classrooms", len(rooms))
        col2.metric("📚 Total classes", len(classes))
        col3.metric("🕒 Available time slots", len(slots))
 
        result = st.session_state.get("allocation_result")
        if result is not None:
            assigned = len(result.get("assignments", []))
            total = len(classes)
            rate = assigned / total * 100 if total else 0
            col4.metric("✅ Allocation success", f"{rate:.1f}%")
        else:
            col4.metric("📊 Allocation", "Not generated")
 
        section_heading(
            "Project data",
            "Explore the records currently stored in this dataset",
        )
        tab1, tab2, tab3 = st.tabs(
            ["🏫 Classrooms", "📚 Classes", "🕒 Time slots"]
        )
        with tab1:
            show_table(rooms)
        with tab2:
            show_table(classes)
        with tab3:
            show_table(slots)
 
        if result is not None:
            assignments = pd.DataFrame(result.get("assignments", []))
            section_heading(
                "Classroom utilization",
                "Seat usage across allocated classrooms",
            )
            show_utilization_chart(assignments)
        else:
            st.info("Generate an allocation to view classroom utilization.")
 
    # -----------------------------------------------------
    # MANAGE RECORDS
    # -----------------------------------------------------
    elif page == "🏫 Manage Records":
        section_heading(
            "Manage classrooms and classes",
            "Add, update or delete records in your selected dataset",
        )
 
        add_tab, update_tab, delete_tab = st.tabs(
            ["➕ Add records", "✏️ Update records", "🗑️ Delete records"]
        )
 
        # ADD
        with add_tab:
            add_room_tab, add_class_tab = st.tabs(
                ["Add classroom", "Add class"]
            )
 
            with add_room_tab:
                with st.form("add_classroom_form", clear_on_submit=True):
                    st.markdown("### Classroom details")
                    room_id = st.text_input(
                        "Classroom ID", placeholder="Example: R107"
                    )
                    capacity = st.number_input(
                        "Classroom capacity", min_value=1, value=40, step=1
                    )
                    facilities = st.text_input(
                        "Facilities", placeholder="Projector, Smart board"
                    )
                    submitted_room = st.form_submit_button(
                        "Add classroom", type="primary", use_container_width=True
                    )
 
                    if submitted_room:
                        try:
                            dm.add(
                                "rooms",
                                {
                                    "room_id": room_id,
                                    "capacity": str(capacity),
                                    "facilities": facilities,
                                },
                            )
                            clear_allocation_result()
                            st.success("Classroom added successfully!")
                            st.rerun()
                        except (ValidationError, KeyError, ValueError) as e:
                            st.error(str(e))
 
            with add_class_tab:
                with st.form("add_class_form", clear_on_submit=True):
                    st.markdown("### Class details")
                    class_id = st.text_input(
                        "Class ID", placeholder="Example: C108"
                    )
                    class_name = st.text_input(
                        "Class name", placeholder="Java Programming"
                    )
                    students = st.number_input(
                        "Number of students", min_value=1, value=30
                    )
                    instructor = st.text_input(
                        "Instructor name", placeholder="Priya"
                    )
                    student_group = st.text_input(
                        "Student group", placeholder="IT Third Year"
                    )
                    slot_options = [""] + slots["slot_id"].astype(str).tolist()
                    fixed_slot = st.selectbox(
                        "Fixed time slot (optional)", slot_options
                    )
                    submitted_class = st.form_submit_button(
                        "Add class", type="primary", use_container_width=True
                    )
 
                    if submitted_class:
                        try:
                            dm.add(
                                "classes",
                                {
                                    "class_id": class_id,
                                    "class_name": class_name,
                                    "students": str(students),
                                    "instructor": instructor,
                                    "student_group": student_group,
                                    "fixed_slot": fixed_slot,
                                },
                            )
                            clear_allocation_result()
                            st.success("Class added successfully!")
                            st.rerun()
                        except (ValidationError, KeyError, ValueError) as e:
                            st.error(str(e))
 
        # UPDATE
        with update_tab:
            update_room_tab, update_class_tab = st.tabs(
                ["Update classroom", "Update class"]
            )
 
            with update_room_tab:
                room_ids = rooms["room_id"].astype(str).tolist()
                if room_ids:
                    selected_room = st.selectbox(
                        "Select classroom", room_ids, key="update_room_select"
                    )
                    current_room = dm.get("rooms", selected_room)
 
                    with st.form("update_room_form"):
                        new_capacity = st.number_input(
                            "Capacity",
                            min_value=1,
                            value=int(current_room["capacity"]),
                        )
                        new_facilities = st.text_input(
                            "Facilities", value=str(current_room["facilities"])
                        )
                        update_room = st.form_submit_button(
                            "Save classroom changes", type="primary"
                        )
                        if update_room:
                            try:
                                dm.update(
                                    "rooms",
                                    selected_room,
                                    {
                                        "capacity": str(new_capacity),
                                        "facilities": new_facilities,
                                    },
                                )
                                clear_allocation_result()
                                st.success("Classroom updated successfully!")
                                st.rerun()
                            except (ValidationError, KeyError, ValueError) as e:
                                st.error(str(e))
                else:
                    st.info("No classrooms available.")
 
            with update_class_tab:
                class_ids = classes["class_id"].astype(str).tolist()
                if class_ids:
                    selected_class = st.selectbox(
                        "Select class", class_ids, key="update_class_select"
                    )
                    current_class = dm.get("classes", selected_class)
 
                    with st.form("update_class_form"):
                        new_name = st.text_input(
                            "Class name", value=str(current_class["class_name"])
                        )
                        new_students = st.number_input(
                            "Number of students",
                            min_value=1,
                            value=int(current_class["students"]),
                        )
                        new_instructor = st.text_input(
                            "Instructor",
                            value=str(current_class["instructor"]),
                        )
                        new_group = st.text_input(
                            "Student group",
                            value=str(current_class["student_group"]),
                        )
                        class_slot_options = (
                            [""] + slots["slot_id"].astype(str).tolist()
                        )
                        current_slot = str(current_class.get("fixed_slot", ""))
                        slot_index = (
                            class_slot_options.index(current_slot)
                            if current_slot in class_slot_options else 0
                        )
                        new_slot = st.selectbox(
                            "Fixed time slot",
                            class_slot_options,
                            index=slot_index,
                        )
                        update_class = st.form_submit_button(
                            "Save class changes", type="primary"
                        )
 
                        if update_class:
                            try:
                                dm.update(
                                    "classes",
                                    selected_class,
                                    {
                                        "class_name": new_name,
                                        "students": str(new_students),
                                        "instructor": new_instructor,
                                        "student_group": new_group,
                                        "fixed_slot": new_slot,
                                    },
                                )
                                clear_allocation_result()
                                st.success("Class updated successfully!")
                                st.rerun()
                            except (ValidationError, KeyError, ValueError) as e:
                                st.error(str(e))
                else:
                    st.info("No classes available.")
 
        # DELETE
        with delete_tab:
            delete_room_tab, delete_class_tab = st.tabs(
                ["Delete classroom", "Delete class"]
            )
 
            with delete_room_tab:
                room_ids = rooms["room_id"].astype(str).tolist()
                if room_ids:
                    delete_room = st.selectbox(
                        "Select classroom to delete",
                        room_ids,
                        key="delete_room_select",
                    )
                    confirm_room = st.checkbox(
                        f"I confirm deletion of {delete_room}",
                        key="confirm_delete_room",
                    )
                    if st.button(
                        "Delete classroom",
                        disabled=not confirm_room,
                        type="primary",
                    ):
                        try:
                            dm.delete("rooms", delete_room)
                            clear_allocation_result()
                            st.success("Classroom deleted successfully!")
                            st.rerun()
                        except (ValidationError, KeyError, ValueError) as e:
                            st.error(str(e))
                else:
                    st.info("No classrooms available.")
 
            with delete_class_tab:
                class_ids = classes["class_id"].astype(str).tolist()
                if class_ids:
                    delete_class = st.selectbox(
                        "Select class to delete",
                        class_ids,
                        key="delete_class_select",
                    )
                    confirm_class = st.checkbox(
                        f"I confirm deletion of {delete_class}",
                        key="confirm_delete_class",
                    )
                    if st.button(
                        "Delete class",
                        disabled=not confirm_class,
                        type="primary",
                    ):
                        try:
                            dm.delete("classes", delete_class)
                            clear_allocation_result()
                            st.success("Class deleted successfully!")
                            st.rerun()
                        except (ValidationError, KeyError, ValueError) as e:
                            st.error(str(e))
                else:
                    st.info("No classes available.")
 
    # -----------------------------------------------------
    # ALLOCATION
    # -----------------------------------------------------
    elif page == "📊 Allocation":
        section_heading(
            "Classroom allocation",
            "Generate optimized classroom and time-slot assignments",
        )
 
        left, right = st.columns([2, 1])
        with left:
            st.markdown("### Smart allocation engine")
            st.write(
                "ClassOpt prioritizes larger classes, respects fixed time "
                "slots and avoids scheduling conflicts."
            )
        with right:
            generate_clicked = st.button(
                "✨ Generate allocation",
                type="primary",
                use_container_width=True,
            )
 
        if generate_clicked:
            try:
                result = allocate_classes(rooms, classes, slots)
                st.session_state["allocation_result"] = result
            except (ValidationError, KeyError, ValueError) as e:
                st.error(f"Unable to generate allocation: {e}")
 
        result = st.session_state.get("allocation_result")
 
        if result is not None:
            assignments = pd.DataFrame(result.get("assignments", []))
            unallocated = pd.DataFrame(result.get("unallocated", []))
 
            total_classes = len(classes)
            allocated_count = len(assignments)
            unallocated_count = len(unallocated)
            success_rate = (
                allocated_count / total_classes * 100 if total_classes else 0
            )
            unused_seats = (
                assignments["unused_seats"].sum()
                if not assignments.empty and "unused_seats" in assignments.columns
                else 0
            )
 
            st.markdown("---")
            section_heading(
                "Allocation summary",
                "Overview of generated classroom assignments",
            )
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Allocated", allocated_count)
            m2.metric("Unallocated", unallocated_count)
            m3.metric("Success rate", f"{success_rate:.1f}%")
            m4.metric("Unused seats", int(unused_seats))
            st.progress(success_rate / 100 if total_classes else 0)
 
            section_heading(
                "Allocation results",
                "Classroom and time-slot assignments",
            )
            if not assignments.empty:
                show_table(assignments)
            else:
                st.info("No classes were allocated.")
 
            section_heading(
                "Unallocated classes",
                "Classes that could not be assigned",
            )
            if not unallocated.empty:
                show_table(unallocated)
            else:
                st.success("All classes were allocated successfully!")
 
            chart_left, chart_right = st.columns(2)
 
            with chart_left:
                section_heading(
                    "Classroom utilization",
                    "Percentage of occupied seats in allocated rooms",
                )
                if not assignments.empty:
                    show_utilization_chart(assignments)
                else:
                    st.info("Utilization chart will appear when classes are allocated.")
 
            with chart_right:
                section_heading(
                    "Allocation status",
                    "Share of allocated and unallocated classes",
                )
                show_allocation_status_chart(
                    allocated_count,
                    unallocated_count,
                )
        else:
            st.info("Click Generate Allocation to see classroom assignments.")
 
    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------
    st.markdown("""
    <div class="footer">
      ClassOpt • Smart Classroom Occupancy and Space Allocation Planner
      <br>Plan smarter. Use space better.
    </div>
    """, unsafe_allow_html=True)
 
 
except (ValidationError, KeyError, ValueError) as e:
    st.error(f"Unable to load project data: {e}")
>>>>>>> 7bfeb50ee1dd3f8d78c1979e937619bf2ba6dbb0
