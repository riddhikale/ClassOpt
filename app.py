
import streamlit as st
import pandas as pd
import plotly.express as px
import html
 
from src.data_manager import DataManager
from src.allocation import allocate_classes
from src.validation import ValidationError
 
 
# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="ClassOpt | Smart Classroom Planner",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
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
