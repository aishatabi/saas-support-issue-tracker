import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ======================================================
# DATABASE
# ======================================================

DB_NAME = "support_issues.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT,
            company TEXT,
            issue_summary TEXT NOT NULL,
            issue_details TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            escalation_required TEXT NOT NULL,
            investigation_notes TEXT,
            next_steps TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_issue(
    customer_name,
    customer_email,
    company,
    issue_summary,
    issue_details,
    category,
    priority,
    status,
    escalation_required,
    investigation_notes,
    next_steps
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO issues (
            customer_name,
            customer_email,
            company,
            issue_summary,
            issue_details,
            category,
            priority,
            status,
            escalation_required,
            investigation_notes,
            next_steps,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        customer_name,
        customer_email,
        company,
        issue_summary,
        issue_details,
        category,
        priority,
        status,
        escalation_required,
        investigation_notes,
        next_steps,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_issues():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM issues ORDER BY created_at DESC", conn)
    conn.close()
    return df


def update_issue(issue_id, new_status, new_notes, new_next_steps):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE issues
        SET status = ?,
            investigation_notes = ?,
            next_steps = ?
        WHERE id = ?
    """, (new_status, new_notes, new_next_steps, issue_id))

    conn.commit()
    conn.close()


# ======================================================
# PAGE SETUP
# ======================================================

st.set_page_config(
    page_title="Support Issue Tracker",
    page_icon="🎧",
    layout="wide"
)

init_db()


# ======================================================
# STYLING
# ======================================================

st.markdown("""
<style>
    /* Whole app */
    .stApp {
        background: #f6f7fb;
        color: #111827;
    }

    /* Remove Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    /* Hero */
    .hero-card {
        background: linear-gradient(135deg, #ffffff 0%, #f2efff 100%);
        border: 1px solid #e5e7eb;
        border-radius: 28px;
        padding: 32px;
        margin-bottom: 26px;
        box-shadow: 0 18px 45px rgba(17, 24, 39, 0.08);
    }

    .hero-pill {
        display: inline-block;
        background: #ede9fe;
        color: #6d28d9;
        padding: 7px 14px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #111827;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 17px;
        color: #6b7280;
        max-width: 750px;
        line-height: 1.6;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 22px;
        border-radius: 22px;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.06);
    }

    div[data-testid="stMetricValue"] {
        font-size: 30px;
        font-weight: 900;
        color: #111827;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #6b7280;
        font-weight: 700;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        background: #ffffff;
        border-radius: 999px;
        padding: 10px 20px;
        margin-right: 8px;
        border: 1px solid #e5e7eb;
        font-weight: 800;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: #111827;
        color: white;
    }

    /* Forms */
    section[data-testid="stForm"] {
        background: #ffffff;
        padding: 28px;
        border-radius: 26px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.06);
    }

    /* Inputs */
    .stTextInput input,
    .stTextArea textarea {
        border-radius: 14px;
        border: 1px solid #d1d5db;
    }

    .stSelectbox div[data-baseweb="select"] {
        border-radius: 14px;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button,
    .stFormSubmitButton button {
        background: #111827;
        color: white;
        border-radius: 14px;
        border: none;
        padding: 0.65rem 1.3rem;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(17, 24, 39, 0.15);
    }

    .stButton button:hover,
    .stDownloadButton button:hover,
    .stFormSubmitButton button:hover {
        background: #374151;
        color: white;
        border: none;
    }

    /* Data table */
    div[data-testid="stDataFrame"] {
        background: white;
        border-radius: 22px;
        padding: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.06);
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 16px;
    }

    /* Small cards */
    .info-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 22px;
        padding: 24px;
        box-shadow: 0 12px 30px rgba(17, 24, 39, 0.05);
        margin-bottom: 20px;
    }

    .section-heading {
        font-size: 24px;
        font-weight: 900;
        color: #111827;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #6b7280;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:
    st.markdown("## 🎧 Support Desk")
    st.markdown("A simple internal tool for managing customer issues.")
    st.markdown("---")
    st.markdown("### Workflow")
    st.markdown("**1.** Log the issue")
    st.markdown("**2.** Investigate")
    st.markdown("**3.** Escalate if needed")
    st.markdown("**4.** Resolve and document")
    st.markdown("---")
    st.markdown("### Built with")
    st.markdown("Python")
    st.markdown("Streamlit")
    st.markdown("SQLite")
    st.markdown("---")
    st.markdown("### Skills shown")
    st.markdown("Technical support")
    st.markdown("Issue triage")
    st.markdown("Documentation")
    st.markdown("Escalation handling")


# ======================================================
# HEADER
# ======================================================

st.markdown("""
<div class="hero-card">
    <div class="hero-pill">Internal Support Tool</div>
    <div class="hero-title">Support Issue Tracker</div>
    <div class="hero-subtitle">
        A clean dashboard for logging customer issues, tracking investigations,
        managing escalations and keeping support workflows clear.
    </div>
</div>
""", unsafe_allow_html=True)


# ======================================================
# LOAD DATA
# ======================================================

issues_df = get_issues()

total_issues = len(issues_df)

if issues_df.empty:
    open_issues = 0
    escalated_issues = 0
    high_priority = 0
else:
    open_issues = len(issues_df[issues_df["status"] != "Resolved"])
    escalated_issues = len(issues_df[issues_df["escalation_required"] == "Yes"])
    high_priority = len(issues_df[issues_df["priority"] == "High"])


# ======================================================
# METRICS
# ======================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Issues", total_issues)

with col2:
    st.metric("Open Issues", open_issues)

with col3:
    st.metric("Escalated", escalated_issues)

with col4:
    st.metric("High Priority", high_priority)


st.write("")


# ======================================================
# TABS
# ======================================================

tab1, tab2, tab3 = st.tabs(["New Issue", "Dashboard", "Update Issue"])


# ======================================================
# TAB 1: NEW ISSUE
# ======================================================

with tab1:
    st.markdown('<div class="section-heading">Log a new customer issue</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Capture the customer problem, investigation notes and next steps in one place.</div>',
        unsafe_allow_html=True
    )

    with st.form("new_issue_form"):
        col_a, col_b = st.columns(2)

        with col_a:
            customer_name = st.text_input("Customer name")
            customer_email = st.text_input("Customer email")
            company = st.text_input("Company")

        with col_b:
            category = st.selectbox(
                "Issue category",
                [
                    "Login / Access",
                    "Billing",
                    "Bug",
                    "Feature Question",
                    "Configuration",
                    "Performance",
                    "Data / Reporting",
                    "Other"
                ]
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Medium", "High"]
            )

            status = st.selectbox(
                "Status",
                ["New", "Investigating", "Waiting for Customer", "Escalated", "Resolved"]
            )

            escalation_required = st.radio(
                "Engineering escalation required?",
                ["No", "Yes"],
                horizontal=True
            )

        issue_summary = st.text_input(
            "Short issue summary",
            placeholder="Example: Customer cannot access their dashboard"
        )

        issue_details = st.text_area(
            "Customer issue details",
            placeholder="What did the customer report? What were they trying to do?"
        )

        investigation_notes = st.text_area(
            "Investigation notes",
            placeholder="What did you check? What patterns or possible causes did you find?"
        )

        next_steps = st.text_area(
            "Next steps",
            placeholder="What happens next? Customer reply, engineering escalation, documentation update..."
        )

        submitted = st.form_submit_button("Save Issue")

        if submitted:
            if not customer_name or not issue_summary or not issue_details:
                st.error("Please complete customer name, issue summary and issue details.")
            else:
                add_issue(
                    customer_name,
                    customer_email,
                    company,
                    issue_summary,
                    issue_details,
                    category,
                    priority,
                    status,
                    escalation_required,
                    investigation_notes,
                    next_steps
                )
                st.success("Issue saved successfully.")


# ======================================================
# TAB 2: DASHBOARD
# ======================================================

with tab2:
    st.markdown('<div class="section-heading">Issue dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Review, filter and export customer issues.</div>',
        unsafe_allow_html=True
    )

    if issues_df.empty:
        st.info("No issues logged yet. Add your first issue in the New Issue tab.")
    else:
        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            selected_status = st.selectbox(
                "Filter by status",
                ["All"] + sorted(issues_df["status"].unique().tolist())
            )

        with filter_col2:
            selected_priority = st.selectbox(
                "Filter by priority",
                ["All"] + sorted(issues_df["priority"].unique().tolist())
            )

        with filter_col3:
            selected_escalation = st.selectbox(
                "Filter by escalation",
                ["All", "Yes", "No"]
            )

        filtered_df = issues_df.copy()

        if selected_status != "All":
            filtered_df = filtered_df[filtered_df["status"] == selected_status]

        if selected_priority != "All":
            filtered_df = filtered_df[filtered_df["priority"] == selected_priority]

        if selected_escalation != "All":
            filtered_df = filtered_df[filtered_df["escalation_required"] == selected_escalation]

        st.dataframe(
            filtered_df[
                [
                    "id",
                    "created_at",
                    "customer_name",
                    "company",
                    "issue_summary",
                    "category",
                    "priority",
                    "status",
                    "escalation_required"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            label="Download CSV",
            data=filtered_df.to_csv(index=False),
            file_name="support_issues.csv",
            mime="text/csv"
        )


# ======================================================
# TAB 3: UPDATE ISSUE
# ======================================================

with tab3:
    st.markdown('<div class="section-heading">Update an issue</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Update status, investigation notes and next steps.</div>',
        unsafe_allow_html=True
    )

    if issues_df.empty:
        st.info("No issues available to update.")
    else:
        issue_ids = issues_df["id"].tolist()

        selected_issue_id = st.selectbox("Select issue ID", issue_ids)

        selected_issue = issues_df[issues_df["id"] == selected_issue_id].iloc[0]

        st.markdown("""
        <div class="info-card">
            <strong>Selected issue</strong>
        </div>
        """, unsafe_allow_html=True)

        st.write("**Customer:**", selected_issue["customer_name"])
        st.write("**Company:**", selected_issue["company"])
        st.write("**Issue:**", selected_issue["issue_summary"])
        st.write("**Current status:**", selected_issue["status"])
        st.write("**Priority:**", selected_issue["priority"])
        st.write("**Escalation required:**", selected_issue["escalation_required"])

        new_status = st.selectbox(
            "New status",
            ["New", "Investigating", "Waiting for Customer", "Escalated", "Resolved"],
            index=["New", "Investigating", "Waiting for Customer", "Escalated", "Resolved"].index(selected_issue["status"])
        )

        current_notes = selected_issue["investigation_notes"]
        if pd.isna(current_notes):
            current_notes = ""

        current_next_steps = selected_issue["next_steps"]
        if pd.isna(current_next_steps):
            current_next_steps = ""

        new_notes = st.text_area(
            "Updated investigation notes",
            value=current_notes
        )

        new_next_steps = st.text_area(
            "Updated next steps",
            value=current_next_steps
        )

        if st.button("Update Issue"):
            update_issue(
                selected_issue_id,
                new_status,
                new_notes,
                new_next_steps
            )
            st.success("Issue updated successfully. Refresh the page to see the latest version.")