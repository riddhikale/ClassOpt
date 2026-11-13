
import streamlit as st
import pandas as pd
import plotly.express as px

from src.data_manager import DataManager
from src.allocation import allocate_classes
from src.validation import ValidationError


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="ClassOpt | Smart Classroom Planner",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom UI theme
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #f5f8ff 0%, #f8fafc 42%, #f8fafc 100%);
        }

        [data-testid="stHeader"] {
            background: rgba(245, 248, 255, 0.85);
        }

        .block-container {
            max-width: 1440px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #101d38 0%, #172b50 100%);
        }

        [data-testid="stSidebar"] * {
            color: #edf3ff;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #c7d5ee;
        }

        [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
            color: #e5edff;
            font-weight: 600;
        }

        .brand-mark {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 2px 24px 2px;
        }

        .brand-icon {
            width: 42px;
            height: 42px;
            border-radius: 13px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #60a5fa, #2563eb);
            font-size: 23px;
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.28);
        }

        .brand-name {
            color: white;
            font-size: 21px;
            line-height: 1.1;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .brand-caption {
            color: #a9bddc;
            font-size: 10px;
            margin-top: 4px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 30px 34px;
            border-radius: 22px;
            background: linear-gradient(115deg, #112344 0%, #1e4785 62%, #2563c7 100%);
            color: white;
            box-shadow: 0 15px 35px rgba(24, 62, 119, 0.16);
            margin-bottom: 26px;
        }

        .hero:after {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -65px;
            top: -125px;
            border: 1px solid rgba(255,255,255,0.16);
            border-radius: 50%;
            box-shadow: 0 0 0 28px rgba(255,255,255,0.035), 0 0 0 58px rgba(255,255,255,0.025);
        }

        .hero-kicker {
            color: #bfdbfe;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }

        .hero-title {
            color: white;
            font-size: clamp(29px, 4vw, 40px);
            font-weight: 800;
            letter-spacing: -1.2px;
            line-height: 1.12;
            margin: 0;
        }

        .hero-subtitle {
            color: #d8e7ff;
            font-size: 14px;
            margin-top: 10px;
            max-width: 650px;
        }

        .section-heading {
            margin: 28px 0 14px 0;
        }

        .section-title {
            color: #14233f;
            font-size: 21px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .section-caption {
            color: #71819b;
            font-size: 12px;
            margin-top: 3px;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #e6edf7;
            border-radius: 17px;
            padding: 18px 20px;
            box-shadow: 0 5px 18px rgba(18, 42, 82, 0.045);
        }

        [data-testid="stMetricLabel"] p {
            color: #71819b !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricValue"] {
            color: #14233f !important;
            font-weight: 800 !important;
        }

        [data-testid="stTabs"] button {
            font-weight: 650;
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: #1d4ed8;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #e6edf7;
            border-radius: 13px;
            overflow: hidden;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            border-radius: 10px;
            min-height: 42px;
            font-weight: 700;
            transition: all 0.15s ease;
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: linear-gradient(100deg, #1d4ed8, #2563eb);
            border: 0;
            color: white;
            box-shadow: 0 5px 14px rgba(37, 99, 235, 0.18);
        }

        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #e6edf7;
            border-radius: 15px;
            padding: 18px 20px 12px 20px;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }

        .small-note {
            color: #71819b;
            font-size: 11px;
            text-align: center;
            padding-top: 24px;
        }

        @media (max-width: 700px) {
            .hero { padding: 24px 22px; }
            .block-container { padding-top: 1rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Reusable display helpers
# ---------------------------------------------------------
def section_heading(title, caption=""):
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="section-title">{title}</div>
            <div class="section-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def clear_allocation_result():
    st.session_state["allocation_result"] = None


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-mark">
            <div class="brand-icon">🏫</div>
            <div>
                <div class="brand-name">ClassOpt</div>
                <div class="brand-caption">Smart Space Planner</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Workspace")
    dataset = st.selectbox(
        "Select dataset",
        ["data", "data_large", "data_stress"],
        help="Choose the classroom dataset to manage and optimize.",
    )

    st.markdown("---")
    st.markdown("**What you can do**")
    st.markdown("- View classroom, class and slot data")
    st.markdown("- Add, update and delete records")
    st.markdown("- Generate classroom allocations")
    st.markdown("- Review utilization and unallocated classes")

    st.markdown("---")
    st.caption("ClassOpt • Classroom Allocation System")


# Reset old results when dataset changes
if st.session_state.get("selected_dataset") != dataset:
    st.session_state["selected_dataset"] = dataset
    st.session_state["allocation_result"] = None


# ---------------------------------------------------------
# Load and validate data
# ---------------------------------------------------------
try:
    dm = DataManager(dataset)
    data = dm.get_clean_data()

    rooms = data["rooms"]
    classes = data["classes"]
    slots = data["slots"]

    # Hero banner
    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Classroom Occupancy & Space Allocation</div>
            <div class="hero-title">Plan smarter. Use space better.</div>
            <div class="hero-subtitle">
                Manage your academic spaces, organize class schedules and generate
                efficient classroom allocations from one dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Overview metrics
    section_heading("Dashboard overview", "A quick snapshot of your selected dataset")
    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Total classrooms", len(rooms))
    metric2.metric("Total classes", len(classes))
    metric3.metric("Available time slots", len(slots))

    # Project data
    section_heading("Project data", "Explore the records currently stored in this dataset")
    data_tab1, data_tab2, data_tab3 = st.tabs(
        ["🏫 Classrooms", "📚 Classes", "🕒 Time slots"]
    )

    with data_tab1:
        st.dataframe(rooms, width="stretch", hide_index=True)

    with data_tab2:
        st.dataframe(classes, width="stretch", hide_index=True)

    with data_tab3:
        st.dataframe(slots, width="stretch", hide_index=True)

    # -----------------------------------------------------
    # Add records
    # -----------------------------------------------------
    section_heading(
        "Add new records",
        "Create classrooms and classes in the selected dataset"
    )

    add_room_tab, add_class_tab = st.tabs(
        ["➕ Add classroom", "➕ Add class"]
    )

    with add_room_tab:
        with st.form("add_classroom_form", clear_on_submit=True):
            st.markdown("**Classroom details**")

            room_id = st.text_input(
                "Classroom ID",
                placeholder="Example: R107"
            )

            capacity = st.number_input(
                "Classroom capacity",
                min_value=1,
                step=1,
                value=40
            )

            facilities = st.text_input(
                "Facilities",
                placeholder="Example: Projector, Smart board",
            )

            submitted_room = st.form_submit_button(
                "Add classroom",
                type="primary",
                width="stretch"
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

                except (ValidationError, KeyError) as e:
                    st.error(str(e))

    with add_class_tab:
        with st.form("add_class_form", clear_on_submit=True):
            st.markdown("**Class details**")

            class_id = st.text_input(
                "Class ID",
                placeholder="Example: C108"
            )

            class_name = st.text_input(
                "Class name",
                placeholder="Example: Java Programming"
            )

            students = st.number_input(
                "Number of students",
                min_value=1,
                step=1,
                value=30
            )

            instructor = st.text_input(
                "Instructor name",
                placeholder="Example: Priya"
            )

            student_group = st.text_input(
                "Student group",
                placeholder="Example: IT Third Year"
            )

            slot_options = [""] + slots["slot_id"].tolist()

            fixed_slot = st.selectbox(
                "Fixed time slot (optional)",
                slot_options
            )

            submitted_class = st.form_submit_button(
                "Add class",
                type="primary",
                width="stretch"
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

                except (ValidationError, KeyError) as e:
                    st.error(str(e))

    # -----------------------------------------------------
    # Update and delete records
    # -----------------------------------------------------
    section_heading(
        "Manage records",
        "Update existing details or remove records you no longer need"
    )

    manage_room_tab, manage_class_tab = st.tabs(
        ["🏫 Manage classrooms", "📚 Manage classes"]
    )

    with manage_room_tab:
        room_ids = rooms["room_id"].tolist()

        if room_ids:
            selected_room = st.selectbox(
                "Choose classroom",
                room_ids,
                key="manage_room_select"
            )

            current_room = dm.get("rooms", selected_room)

            with st.form("update_room_form"):
                st.markdown(f"**Editing classroom: {selected_room}**")

                new_capacity = st.number_input(
                    "Capacity",
                    min_value=1,
                    value=int(current_room["capacity"]),
                    key=f"update_room_capacity_{selected_room}",
                )

                new_facilities = st.text_input(
                    "Facilities",
                    value=current_room["facilities"],
                    key=f"update_room_facilities_{selected_room}",
                )

                update_room = st.form_submit_button(
                    "Save classroom changes",
                    type="primary"
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

                    except (ValidationError, KeyError) as e:
                        st.error(str(e))

            with st.expander("Delete this classroom"):
                st.warning(
                    "Deleting a classroom permanently removes it from this dataset."
                )

                confirm_room_delete = st.checkbox(
                    f"I understand that {selected_room} will be deleted.",
                    key="confirm_room_delete",
                )

                if st.button(
                    "Delete classroom",
                    key="delete_room_button",
                    disabled=not confirm_room_delete
                ):
                    try:
                        dm.delete("rooms", selected_room)
                        clear_allocation_result()
                        st.success("Classroom deleted successfully!")
                        st.rerun()

                    except (ValidationError, KeyError) as e:
                        st.error(str(e))

        else:
            st.info("No classrooms available in this dataset.")

    with manage_class_tab:
        class_ids = classes["class_id"].tolist()

        if class_ids:
            selected_class = st.selectbox(
                "Choose class",
                class_ids,
                key="manage_class_select"
            )

            current_class = dm.get("classes", selected_class)

            with st.form("update_class_form"):
                st.markdown(f"**Editing class: {selected_class}**")

                new_name = st.text_input(
                    "Class name",
                    value=current_class["class_name"],
                    key=f"update_class_name_{selected_class}"
                )

                new_students = st.number_input(
                    "Number of students",
                    min_value=1,
                    value=int(current_class["students"]),
                    key=f"update_class_students_{selected_class}",
                )

                new_instructor = st.text_input(
                    "Instructor",
                    value=current_class["instructor"],
                    key=f"update_class_instructor_{selected_class}"
                )

                new_group = st.text_input(
                    "Student group",
                    value=current_class["student_group"],
                    key=f"update_class_group_{selected_class}"
                )

                class_slot_options = [""] + slots["slot_id"].tolist()
                current_slot = current_class["fixed_slot"]

                slot_index = (
                    class_slot_options.index(current_slot)
                    if current_slot in class_slot_options
                    else 0
                )

                new_slot = st.selectbox(
                    "Fixed time slot",
                    class_slot_options,
                    index=slot_index,
                    key=f"update_class_slot_{selected_class}",
                )

                update_class = st.form_submit_button(
                    "Save class changes",
                    type="primary"
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

                    except (ValidationError, KeyError) as e:
                        st.error(str(e))

            with st.expander("Delete this class"):
                st.warning(
                    "Deleting a class permanently removes it from this dataset."
                )

                confirm_class_delete = st.checkbox(
                    f"I understand that {selected_class} will be deleted.",
                    key="confirm_class_delete",
                )

                if st.button(
                    "Delete class",
                    key="delete_class_button",
                    disabled=not confirm_class_delete
                ):
                    try:
                        dm.delete("classes", selected_class)
                        clear_allocation_result()
                        st.success("Class deleted successfully!")
                        st.rerun()

                    except (ValidationError, KeyError) as e:
                        st.error(str(e))

        else:
            st.info("No classes available in this dataset.")

    # -----------------------------------------------------
    # Allocation engine
    # -----------------------------------------------------
    section_heading(
        "Classroom allocation",
        "Run the planner and review how classes are assigned"
    )

    run_col, note_col = st.columns(
        [1, 2],
        vertical_alignment="center"
    )

    with run_col:
        generate_clicked = st.button(
            "✨ Generate allocation",
            type="primary",
            width="stretch",
        )

    with note_col:
        st.caption(
            "The planner prioritizes larger classes, respects fixed slots "
            "and avoids scheduling conflicts."
        )

    if generate_clicked:
        try:
            result = allocate_classes(rooms, classes, slots)
            st.session_state["allocation_result"] = result

        except (ValidationError, KeyError, ValueError) as e:
            st.error(f"Unable to generate allocation: {e}")

    result = st.session_state.get("allocation_result")

    if result is not None:
        assignments = pd.DataFrame(result["assignments"])
        unallocated = pd.DataFrame(result["unallocated"])

        total_classes = len(classes)
        allocated_count = len(assignments)
        unallocated_count = len(unallocated)

        success_rate = (
            allocated_count / total_classes * 100
            if total_classes else 0
        )

        unused_seats = (
            assignments["unused_seats"].sum()
            if not assignments.empty else 0
        )

        # Allocation summary
        allocation_metric1, allocation_metric2, allocation_metric3, allocation_metric4 = st.columns(4)

        allocation_metric1.metric("Allocated", allocated_count)
        allocation_metric2.metric("Unallocated", unallocated_count)
        allocation_metric3.metric("Success rate", f"{success_rate:.1f}%")
        allocation_metric4.metric("Unused seats", int(unused_seats))

        st.progress(success_rate / 100 if total_classes else 0)

        # Allocation results
        section_heading(
            "Allocation results",
            "The classroom and time-slot assignments generated by ClassOpt"
        )

        if not assignments.empty:
            st.dataframe(
                assignments,
                width="stretch",
                hide_index=True
            )
        else:
            st.info("No classes were allocated.")

        # Unallocated classes
        section_heading(
            "Unallocated classes",
            "Classes that could not be assigned and the reason"
        )

        if not unallocated.empty:
            st.dataframe(
                unallocated,
                width="stretch",
                hide_index=True
            )
        else:
            st.success("All classes were allocated successfully!")

        # Classroom utilization chart
        section_heading(
            "Classroom utilization",
            "Percentage of occupied seats across allocated sessions"
        )

        if not assignments.empty:
            room_usage = (
                assignments.groupby("room_id")
                .agg(
                    students=("students", "sum"),
                    capacity=("capacity", "sum"),
                )
                .reset_index()
            )

            room_usage["utilization"] = (
                room_usage["students"]
                / room_usage["capacity"] * 100
            )

            fig = px.bar(
                room_usage,
                x="room_id",
                y="utilization",
                text_auto=".1f",
                color="utilization",
                color_continuous_scale="Blues",
                title="Room utilization percentage",
                labels={
                    "room_id": "Classroom",
                    "utilization": "Utilization (%)",
                },
            )

            fig.update_layout(
                yaxis_range=[0, 100],
                yaxis_ticksuffix="%",
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(
                    family="DM Sans, sans-serif",
                    color="#243550"
                ),
                title_font=dict(
                    size=17,
                    color="#14233f"
                ),
                margin=dict(
                    l=15,
                    r=15,
                    t=55,
                    b=15
                ),
                coloraxis_showscale=False,
            )

            fig.update_traces(
                texttemplate="%{text}%",
                textposition="outside",
                marker_line_width=0,
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

    # Footer
    st.markdown(
        "<div class='small-note'>ClassOpt • Smart Classroom Occupancy and Space Allocation Planner</div>",
        unsafe_allow_html=True,
    )

except (ValidationError, KeyError, ValueError) as e:
    st.error(f"Unable to load project data: {e}")