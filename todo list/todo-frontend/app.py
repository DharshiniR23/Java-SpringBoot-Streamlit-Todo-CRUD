"""
Todo Dashboard - Streamlit Frontend for Spring Boot Todo REST API
Backend: Spring Boot + MySQL + JPA/Hibernate running on http://localhost:8087
"""

import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# --------------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------------
API_BASE_URL = "http://localhost:8087/api/todos"
REQUEST_TIMEOUT = 5  # seconds

st.set_page_config(
    page_title="Todo Dashboard",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------------------------
# STYLING
# --------------------------------------------------------------------------------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .sub-title {
            color: #6b7280;
            margin-bottom: 1.5rem;
        }
        .todo-card {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        .todo-title {
            font-size: 1.1rem;
            font-weight: 600;
        }
        .todo-desc {
            color: #4b5563;
            margin-top: 4px;
        }
        .todo-meta {
            color: #9ca3af;
            font-size: 0.8rem;
            margin-top: 6px;
        }
        .badge-done {
            background-color: #dcfce7;
            color: #166534;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-pending {
            background-color: #fef9c3;
            color: #854d0e;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------------
# API HELPER FUNCTIONS
# --------------------------------------------------------------------------------

def api_get_all():
    """GET all todos. Returns (data, error_message)."""
    try:
        resp = requests.get(API_BASE_URL, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json(), None
    except ConnectionError:
        return None, "🔌 Cannot connect to backend. Is Spring Boot running on port 8087?"
    except Timeout:
        return None, "⏳ Backend request timed out. Please try again."
    except RequestException as e:
        return None, f"⚠️ Failed to fetch todos: {e}"


def api_create(title, description, completed):
    payload = {"title": title, "description": description, "completed": completed}
    try:
        resp = requests.post(API_BASE_URL, json=payload, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json(), None
    except ConnectionError:
        return None, "🔌 Cannot connect to backend. Is Spring Boot running on port 8087?"
    except Timeout:
        return None, "⏳ Backend request timed out. Please try again."
    except RequestException as e:
        return None, f"⚠️ Failed to create todo: {e}"


def api_update(todo_id, title, description, completed):
    payload = {"title": title, "description": description, "completed": completed}
    try:
        resp = requests.put(f"{API_BASE_URL}/{todo_id}", json=payload, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 404:
            return None, f"❌ Todo with ID {todo_id} not found."
        resp.raise_for_status()
        return resp.json(), None
    except ConnectionError:
        return None, "🔌 Cannot connect to backend. Is Spring Boot running on port 8087?"
    except Timeout:
        return None, "⏳ Backend request timed out. Please try again."
    except RequestException as e:
        return None, f"⚠️ Failed to update todo: {e}"


def api_delete(todo_id):
    try:
        resp = requests.delete(f"{API_BASE_URL}/{todo_id}", timeout=REQUEST_TIMEOUT)
        if resp.status_code == 404:
            return False, f"❌ Todo with ID {todo_id} not found."
        resp.raise_for_status()
        return True, None
    except ConnectionError:
        return False, "🔌 Cannot connect to backend. Is Spring Boot running on port 8087?"
    except Timeout:
        return False, "⏳ Backend request timed out. Please try again."
    except RequestException as e:
        return False, f"⚠️ Failed to delete todo: {e}"


def refresh_todos():
    """Fetch latest todos and store in session state."""
    data, error = api_get_all()
    st.session_state["todos"] = data if data is not None else []
    st.session_state["fetch_error"] = error


# --------------------------------------------------------------------------------
# SESSION STATE INIT
# --------------------------------------------------------------------------------
if "todos" not in st.session_state:
    refresh_todos()

# --------------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------------
st.markdown('<div class="main-title">✅ Todo Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Connected to Spring Boot backend at '
    f'<code>{API_BASE_URL}</code></div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------------
# SIDEBAR — CREATE TODO
# --------------------------------------------------------------------------------
with st.sidebar:
    st.header("➕ Add New Todo")
    with st.form("create_form", clear_on_submit=True):
        new_title = st.text_input("Title", placeholder="e.g. Learn Spring Boot")
        new_description = st.text_area("Description", placeholder="Add some details...")
        new_completed = st.checkbox("Mark as completed", value=False)
        submitted = st.form_submit_button("Add Todo", use_container_width=True, type="primary")

        if submitted:
            if not new_title.strip():
                st.error("⚠️ Title cannot be empty.")
            else:
                result, error = api_create(new_title.strip(), new_description.strip(), new_completed)
                if error:
                    st.error(error)
                else:
                    st.success(f"✅ Todo '{new_title}' created successfully!")
                    refresh_todos()
                    st.rerun()

    st.divider()
    if st.button("🔄 Refresh Data", use_container_width=True):
        refresh_todos()
        st.rerun()

# --------------------------------------------------------------------------------
# MAIN AREA — ERROR BANNER (BACKEND DOWN, ETC.)
# --------------------------------------------------------------------------------
if st.session_state.get("fetch_error"):
    st.error(st.session_state["fetch_error"])
    st.info(
        "👉 Make sure the Spring Boot application is running on **port 8087** "
        "and MySQL is up, then click **Refresh Data**."
    )
    st.stop()

todos = st.session_state.get("todos", [])

# --------------------------------------------------------------------------------
# METRICS
# --------------------------------------------------------------------------------
total = len(todos)
completed_count = sum(1 for t in todos if t.get("completed"))
pending_count = total - completed_count

col1, col2, col3 = st.columns(3)
col1.metric("📋 Total Todos", total)
col2.metric("✅ Completed", completed_count)
col3.metric("🕗 Pending", pending_count)

st.divider()

# --------------------------------------------------------------------------------
# TABS — VIEW / UPDATE / DELETE
# --------------------------------------------------------------------------------
tab_view, tab_update, tab_delete = st.tabs(["📋 All Todos", "✏️ Update Todo", "🗑️ Delete Todo"])

# ---------- VIEW TAB ----------
with tab_view:
    if not todos:
        st.info("No todos yet. Add one from the sidebar to get started!")
    else:
        view_mode = st.radio("View as:", ["Cards", "Table"], horizontal=True, key="view_mode")

        if view_mode == "Cards":
            for todo in todos:
                badge_class = "badge-done" if todo.get("completed") else "badge-pending"
                badge_text = "Completed" if todo.get("completed") else "Pending"
                st.markdown(
                    f"""
                    <div class="todo-card">
                        <span class="{badge_class}">{badge_text}</span>
                        <div class="todo-title">#{todo.get('id')} — {todo.get('title', '')}</div>
                        <div class="todo-desc">{todo.get('description', '') or '<i>No description</i>'}</div>
                        <div class="todo-meta">Created at: {todo.get('createdAt', 'N/A')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            table_data = [
                {
                    "ID": t.get("id"),
                    "Title": t.get("title"),
                    "Description": t.get("description"),
                    "Completed": "✅" if t.get("completed") else "❌",
                    "Created At": t.get("createdAt"),
                }
                for t in todos
            ]
            st.dataframe(table_data, use_container_width=True, hide_index=True)

# ---------- UPDATE TAB ----------
with tab_update:
    if not todos:
        st.info("No todos available to update.")
    else:
        id_options = [t["id"] for t in todos]
        selected_id = st.selectbox("Select Todo ID to update", id_options, key="update_select")
        selected_todo = next((t for t in todos if t["id"] == selected_id), None)

        if selected_todo:
            with st.form("update_form"):
                upd_title = st.text_input("Title", value=selected_todo.get("title", ""))
                upd_description = st.text_area("Description", value=selected_todo.get("description", ""))
                upd_completed = st.checkbox("Completed", value=bool(selected_todo.get("completed")))
                update_submitted = st.form_submit_button("Update Todo", type="primary", use_container_width=True)

                if update_submitted:
                    if not upd_title.strip():
                        st.error("⚠️ Title cannot be empty.")
                    else:
                        result, error = api_update(
                            selected_id, upd_title.strip(), upd_description.strip(), upd_completed
                        )
                        if error:
                            st.error(error)
                        else:
                            st.success(f"✅ Todo #{selected_id} updated successfully!")
                            refresh_todos()
                            st.rerun()

# ---------- DELETE TAB ----------
with tab_delete:
    if not todos:
        st.info("No todos available to delete.")
    else:
        id_options = [t["id"] for t in todos]
        delete_id = st.selectbox("Select Todo ID to delete", id_options, key="delete_select")
        todo_to_delete = next((t for t in todos if t["id"] == delete_id), None)

        if todo_to_delete:
            st.warning(
                f"You are about to delete: **#{todo_to_delete['id']} — "
                f"{todo_to_delete.get('title', '')}**"
            )
            confirm = st.checkbox("I confirm I want to delete this todo.", key="confirm_delete")
            if st.button("🗑️ Delete Todo", type="primary", disabled=not confirm):
                success, error = api_delete(delete_id)
                if error:
                    st.error(error)
                elif success:
                    st.success(f"✅ Todo #{delete_id} deleted successfully!")
                    refresh_todos()
                    st.rerun()

# --------------------------------------------------------------------------------
# FOOTER
# --------------------------------------------------------------------------------
st.divider()
st.caption(
    "Built with Streamlit • Connected to Spring Boot REST API on port 8087 • "
    "All changes sync live with MySQL, Postman, and browser GET requests."
)
