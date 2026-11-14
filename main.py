import html
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Make src folder accessible
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from agent.email_agent import EmailAgent
from memory.database import get_email_history, save_feedback


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Intelligent Email Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menu names (defined once so the menu and the page logic always match)
PAGE_DASHBOARD = "Dashboard"
PAGE_PROCESS = "Process Email"
PAGE_HISTORY = "Email History"
PAGE_ABOUT = "About Project"

# Optional: write your database column names here so the tables show proper
# headings, for example ["ID", "Subject", "Categories", "Priority", "Action"].
# Leave the list empty to keep the default numbered columns.
HISTORY_COLUMNS = []


# --------------------------------------------------
# CUSTOM CSS (light professional theme, larger text,
# hover effects and responsive layout)
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ---------- Colour palette ---------- */
:root {
    --bg: #F4F8FD;
    --surface: #FFFFFF;
    --primary: #2F6FDE;
    --primary-dark: #1F57B8;
    --primary-soft: #E6F0FF;
    --primary-soft-2: #D5E5FF;
    --text: #1E3A5F;
    --muted: #51627A;
    --border: #DCE6F4;
    --shadow: 0 4px 14px rgba(30, 64, 110, 0.07);
    --shadow-hover: 0 10px 24px rgba(30, 64, 110, 0.14);
}

/* ---------- Base typography (larger and easier to read) ---------- */
html {
    font-size: 17px;
}

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
}

.stApp {
    background-color: var(--bg);
}

.stMarkdown p,
.stMarkdown li {
    font-size: 1.08rem;
    line-height: 1.7;
    color: var(--text);
}

h1, h2, h3, h4 {
    color: var(--text);
    font-weight: 700;
}

h2 { font-size: 1.8rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

/* Widget labels */
[data-testid="stWidgetLabel"] p {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
}

/* Hide Streamlit footer, keep header so the sidebar toggle still works */
footer { visibility: hidden; }

[data-testid="stHeader"] { background: transparent; }

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EAF3FF 0%, #F8FBFF 100%);
    border-right: 1px solid var(--border);
}

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 4px 6px 4px;
}

.brand-logo {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: linear-gradient(135deg, #4C8DF0, #2F6FDE);
    color: white;
    font-weight: 700;
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(47, 111, 222, 0.30);
}

.brand-title {
    color: var(--text);
    font-size: 1.45rem;
    font-weight: 700;
    line-height: 1.2;
}

.brand-sub {
    color: var(--muted);
    font-size: 0.95rem;
    margin-top: 2px;
}

/* Menu heading */
[data-testid="stSidebar"] .stRadio > label p {
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
}

/* Menu items */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 8px;
}

[data-testid="stSidebar"] div[role="radiogroup"] > label {
    width: 100%;
    padding: 14px 16px;
    border-radius: 12px;
    border: 1px solid transparent;
    background-color: transparent;
    cursor: pointer;
    transition: all 0.25s ease;
}

/* Hide the small radio circle so the menu looks like navigation buttons */
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none;
}

/* Menu text */
[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text);
    margin: 0;
}

/* Hover effect */
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: var(--primary-soft);
    border: 1px solid #C4D9F7;
    padding-left: 24px;
    box-shadow: 0 4px 12px rgba(47, 111, 222, 0.12);
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:hover p {
    color: var(--primary-dark);
}

/* Selected menu item */
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, var(--primary-soft-2), #EEF5FF);
    border: 1px solid #B5CFF5;
    box-shadow: inset 5px 0 0 var(--primary);
}

[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: var(--primary-dark);
    font-weight: 700;
}

/* Sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    font-size: 0.95rem;
    color: var(--muted);
}

/* ---------- Page header ---------- */
.page-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #EAF3FF 100%);
    border: 1px solid var(--border);
    border-left: 6px solid var(--primary);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 28px;
    box-shadow: var(--shadow);
}

.main-heading {
    color: var(--text);
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 6px;
}

.sub-heading {
    color: var(--muted);
    font-size: 1.15rem;
}

/* ---------- Metric cards ---------- */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 20px;
    margin-bottom: 26px;
}

.metric-card {
    background: var(--surface);
    padding: 22px 24px;
    border-radius: 16px;
    border: 1px solid var(--border);
    border-top: 5px solid var(--accent, var(--primary));
    box-shadow: var(--shadow);
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
}

.metric-label {
    color: var(--muted);
    font-size: 1.15rem;
    font-weight: 600;
}

.metric-value {
    color: var(--text);
    font-size: 2.6rem;
    font-weight: 700;
    margin-top: 8px;
    word-break: break-word;
}

/* ---------- Content cards ---------- */
.content-card {
    background: var(--surface);
    padding: 26px 28px;
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: var(--shadow);
    margin-bottom: 22px;
    transition: all 0.25s ease;
}

.content-card:hover {
    box-shadow: var(--shadow-hover);
}

.card-title {
    color: var(--text);
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 8px;
}

.card-text {
    color: var(--muted);
    font-size: 1.15rem;
    line-height: 1.75;
}

/* Information grid (About page and result explanations) */
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
    gap: 20px;
    margin-bottom: 26px;
}

.info-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: var(--shadow);
    transition: all 0.25s ease;
}

.info-card:hover {
    transform: translateY(-5px);
    border-color: #B5CFF5;
    box-shadow: var(--shadow-hover);
}

/* Category and technology badges */
.pill {
    display: inline-block;
    padding: 9px 20px;
    margin: 5px 8px 5px 0;
    border-radius: 999px;
    background: var(--primary-soft);
    border: 1px solid #C4D9F7;
    color: var(--primary-dark);
    font-size: 1.05rem;
    font-weight: 600;
    transition: all 0.25s ease;
}

.pill:hover {
    background: var(--primary);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(47, 111, 222, 0.25);
}

/* ---------- Form ---------- */
[data-testid="stForm"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: var(--shadow);
}

.stTextInput input,
.stTextArea textarea {
    font-size: 1.1rem;
    border-radius: 10px;
    background-color: white;
}

[data-baseweb="input"],
[data-baseweb="textarea"] {
    border-radius: 10px;
    border: 1px solid #CBD9EB;
    transition: all 0.2s ease;
}

[data-baseweb="input"]:hover,
[data-baseweb="textarea"]:hover {
    border-color: #9DBFEF;
}

[data-baseweb="input"]:focus-within,
[data-baseweb="textarea"]:focus-within {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(47, 111, 222, 0.15);
}

/* ---------- Buttons ---------- */
.stButton > button,
.stFormSubmitButton > button {
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 12px;
    min-height: 3.2rem;
    padding: 10px 22px;
    transition: all 0.25s ease;
}

.stButton > button p,
.stFormSubmitButton > button p {
    font-size: 1.12rem;
    font-weight: 600;
    color: white;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: var(--primary-dark);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(47, 111, 222, 0.28);
}

.stButton > button:active,
.stFormSubmitButton > button:active {
    transform: translateY(0);
}

/* ---------- Alerts and tables ---------- */
[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stAlert"] p {
    font-size: 1.1rem;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

hr {
    border-color: var(--border);
}

/* ---------- Responsive design ---------- */
@media (max-width: 992px) {
    .block-container {
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }
    .main-heading { font-size: 1.9rem; }
}

@media (max-width: 768px) {
    html { font-size: 16px; }

    .block-container {
        padding: 1.2rem 1rem 2.5rem 1rem;
    }

    .page-header {
        padding: 18px 20px;
        margin-bottom: 20px;
    }

    .main-heading { font-size: 1.6rem; }
    .sub-heading { font-size: 1.05rem; }

    .metric-value { font-size: 2.1rem; }

    .content-card,
    .info-card {
        padding: 18px 20px;
    }

    [data-testid="stForm"] {
        padding: 1rem;
    }

    /* Stack Streamlit columns on small screens */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap;
    }

    [data-testid="stColumn"],
    [data-testid="column"] {
        min-width: 100% !important;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS FOR THE INTERFACE
# --------------------------------------------------

PRIORITY_COLORS = {
    "High": "#E5484D",
    "Medium": "#F5A524",
    "Low": "#2FB36D",
}


def flatten_html(markup):
    """Remove indentation and line breaks so Streamlit never shows HTML as a code block."""
    return re.sub(r"\s*\n\s*", " ", markup.strip())


def show_html(markup):
    """Display an HTML block safely."""
    st.markdown(flatten_html(markup), unsafe_allow_html=True)


def page_header(title, subtitle):
    """Display the heading banner at the top of every page."""
    show_html(
        f"""
        <div class="page-header">
            <div class="main-heading">{html.escape(title)}</div>
            <div class="sub-heading">{html.escape(subtitle)}</div>
        </div>
        """
    )


def metric_card(label, value, accent="#2F6FDE"):
    """Return the HTML of one dashboard card."""
    return flatten_html(
        f"""
        <div class="metric-card" style="--accent: {accent};">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="metric-value">{html.escape(str(value))}</div>
        </div>
        """
    )


def info_card(title, text):
    """Return the HTML of one information card."""
    return flatten_html(
        f"""
        <div class="info-card">
            <div class="card-title">{html.escape(title)}</div>
            <div class="card-text">{html.escape(text)}</div>
        </div>
        """
    )


def history_table(rows):
    """Convert database rows to a table. Uses HISTORY_COLUMNS when the length matches."""
    table = pd.DataFrame(rows)
    if HISTORY_COLUMNS and len(HISTORY_COLUMNS) == table.shape[1]:
        table.columns = HISTORY_COLUMNS
    return table


# --------------------------------------------------
# AGENT INITIALIZATION
# --------------------------------------------------

@st.cache_resource
def load_agent():
    return EmailAgent()


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:

    show_html(
        """
        <div class="brand">
            <div class="brand-logo">EA</div>
            <div>
                <div class="brand-title">Email Agent</div>
                <div class="brand-sub">Intelligent Email Management</div>
            </div>
        </div>
        """
    )

    st.markdown("---")

    selected_page = st.radio(
        "Main Menu",
        [PAGE_DASHBOARD, PAGE_PROCESS, PAGE_HISTORY, PAGE_ABOUT],
        label_visibility="visible"
    )

    st.markdown("---")

    st.caption("Email Classifier and Auto-Reply Agent")
    st.caption("Version 1.0 | Local Application")


# --------------------------------------------------
# LOAD EMAIL HISTORY
# --------------------------------------------------

history = get_email_history()


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

if selected_page == PAGE_DASHBOARD:

    page_header(
        "Dashboard Overview",
        "Monitor your intelligent email management system."
    )

    total_emails = len(history)

    high_priority = sum(
        1 for email in history if email[3] == "High"
    )

    draft_count = sum(
        1 for email in history if email[4] == "draft_reply"
    )

    show_html(
        '<div class="metric-grid">'
        + metric_card("Total Emails Processed", total_emails, "#2F6FDE")
        + metric_card("High Priority Emails", high_priority, "#E5484D")
        + metric_card("Reply Drafts Created", draft_count, "#2FB36D")
        + '</div>'
    )

    show_html(
        """
        <div class="content-card">
            <div class="card-title">Welcome to Your Email Agent</div>
            <div class="card-text">
                This system uses machine learning and rule-based
                decision-making to classify emails, identify priority,
                and prepare suggested replies.
            </div>
        </div>
        """
    )

    st.info(
        "Select 'Process Email' from the left menu to analyse "
        "a new email."
    )

    st.subheader("Recent Email Activity")

    if history:
        st.dataframe(
            history_table(history[:5]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No emails have been processed yet.")


# --------------------------------------------------
# PROCESS EMAIL PAGE
# --------------------------------------------------

elif selected_page == PAGE_PROCESS:

    page_header(
        "Process New Email",
        "Enter the email details to let the agent analyse them."
    )

    with st.form("email_form"):

        subject = st.text_input(
            "Email Subject",
            placeholder="Enter the email subject..."
        )

        body = st.text_area(
            "Email Body",
            height=200,
            placeholder="Paste or type the email content here..."
        )

        submitted = st.form_submit_button(
            "Analyse Email",
            use_container_width=True
        )

        if submitted:

            if not subject.strip() or not body.strip():

                st.warning(
                    "Please enter both the subject and email body."
                )

            else:

                try:
                    with st.spinner("Analysing email..."):

                        agent = load_agent()

                        result = agent.process_email(
                            subject,
                            body
                        )

                        st.session_state["result"] = result
                        st.session_state["feedback_status"] = None

                except Exception as error:
                    st.error(f"Unable to process email: {error}")

    # Display results
    if st.session_state.get("result"):

        result = st.session_state["result"]

        st.divider()

        st.subheader("Email Analysis Results")

        priority_color = PRIORITY_COLORS.get(result["priority"], "#2F6FDE")

        show_html(
            '<div class="metric-grid">'
            + metric_card("Priority", result["priority"], priority_color)
            + metric_card("Agent Action", result["action"], "#2F6FDE")
            + metric_card("Email ID", result["email_id"], "#7C9CD6")
            + '</div>'
        )

        st.markdown("#### Predicted Categories")

        if result["categories"]:

            pills = "".join(
                f'<span class="pill">{html.escape(str(category))}</span>'
                for category in result["categories"]
            )
            show_html(pills)

        else:
            st.warning("No category was identified.")

        st.write("")

        show_html(
            '<div class="info-grid">'
            + info_card("Priority Explanation", str(result["priority_reason"]))
            + info_card("Agent Decision", str(result["action_reason"]))
            + '</div>'
        )

        st.markdown("#### Suggested Reply")

        if result["suggested_reply"]:

            edited_reply = st.text_area(
                "Review or edit the suggested reply",
                value=result["suggested_reply"],
                height=160,
                key=f"reply_{result['email_id']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Approve Draft",
                    use_container_width=True
                ):

                    save_feedback(
                        result["email_id"],
                        "approved",
                        "Human approved the suggested draft."
                    )

                    st.session_state["feedback_status"] = "approved"

            with col2:

                if st.button(
                    "Reject Draft",
                    use_container_width=True
                ):

                    save_feedback(
                        result["email_id"],
                        "rejected",
                        "Human rejected the suggested draft."
                    )

                    st.session_state["feedback_status"] = "rejected"

            if st.session_state.get("feedback_status"):

                st.success(
                    "Feedback recorded: "
                    + st.session_state["feedback_status"]
                )

            st.info(
                "Human approval is required. "
                "This application does not send emails."
            )

        else:

            st.warning(
                "No reply was generated. Human review is required."
            )


# --------------------------------------------------
# EMAIL HISTORY PAGE
# --------------------------------------------------

elif selected_page == PAGE_HISTORY:

    page_header(
        "Email History",
        "View previously processed emails and agent decisions."
    )

    if history:

        st.dataframe(
            history_table(history),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "The records are retrieved from your local SQLite database."
        )

    else:

        st.info("No email history is available yet.")


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif selected_page == PAGE_ABOUT:

    page_header(
        "About the Project",
        "Intelligent Email Classifier and Auto-Reply Agent"
    )

    show_html(
        """
        <div class="content-card">
            <div class="card-title">Project Overview</div>
            <div class="card-text">
                This project demonstrates an intelligent agent that
                uses machine learning and rule-based reasoning to
                process and manage emails.
            </div>
        </div>
        """
    )

    st.markdown("### Main Components")

    components = [
        ("Email Classification", "Predicts email categories using TF-IDF and Logistic Regression."),
        ("Priority Detection", "Identifies High, Medium, and Low priority using keyword rules."),
        ("Decision Engine", "Selects the appropriate action for each email."),
        ("Reply Generator", "Creates suggested replies using local CSV templates."),
        ("Agent Memory", "Stores email history and human feedback using SQLite.")
    ]

    cards = "".join(info_card(name, description) for name, description in components)
    show_html('<div class="info-grid">' + cards + '</div>')

    st.markdown("### Technologies Used")

    technologies = ["Python", "Scikit-learn", "Pandas", "SQLite",
                    "Streamlit", "TF-IDF", "Logistic Regression"]

    badges = "".join(f'<span class="pill">{html.escape(t)}</span>' for t in technologies)
    show_html(badges)

    st.write("")
    st.success(
        "The application requires human review before any reply "
        "is sent. Automatic email sending is not enabled."
    )