"""
command to execute the FE Streamlit prg:

streamlit run streamlit_app.py

============================================================
 Streamlit Frontend for the FastAPI User Registration API
============================================================

WHAT THIS DOES:
- Shows a simple form to add a new user (name, age, email)
- Sends that data to your FastAPI backend's POST /register/ endpoint
- Shows a table of all existing users, fetched from GET /users/

BEFORE RUNNING THIS FILE:
1. Make sure your FastAPI backend (app.py) is already running:
       uvicorn app:app --reload
   It should be reachable at http://127.0.0.1:8000

2. Install streamlit + requests (only once):
       pip install streamlit requests

RUN THIS FILE WITH:
    streamlit run streamlit_app.py
"""

import streamlit as st
import requests

# ------------------------------------------------------------------
# Config: where your FastAPI backend is running
# ------------------------------------------------------------------
# this is also called endpoint
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="User Registration", page_icon="🧑‍💼")
st.title("🧑‍💼 User Registration")
st.caption("Frontend built with Streamlit, talking to your FastAPI backend.")

# ------------------------------------------------------------------
# SECTION 1: Registration form
# ------------------------------------------------------------------
st.header("Add a New User")

with st.form("register_form", clear_on_submit=True):
    name = st.text_input("Name", placeholder="e.g. Priya")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    email = st.text_input("Email", placeholder="e.g. priya@example.com")

    submitted = st.form_submit_button("Register User")

    if submitted:
        # Basic client-side check before even calling the API.
        # (The API will still validate everything again via Pydantic.)
        if not name or not email:
            st.error("Please fill in both name and email.")
        else:
            payload = {
                "name": name,
                "age": int(age),
                "email": email,
            }
            try:
                response = requests.post(f"{API_BASE_URL}/register/", json=payload)

                if response.status_code == 200:
                    st.success("✅ User registered successfully!")
                    st.json(response.json())
                else:
                    # FastAPI/Pydantic validation errors and duplicate-email
                    # errors both land here, with details in the response body.
                    st.error(f"❌ Registration failed: {response.json().get('detail')}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Is it running at "
                    f"{API_BASE_URL}? (Start it with: uvicorn app:app --reload)"
                )

# ------------------------------------------------------------------
# SECTION 2: Show all registered users
# ------------------------------------------------------------------
st.header("All Registered Users")

if st.button("🔄 Refresh User List"):
    st.rerun()

users = []  # keep this available for the Update/Delete sections below

try:
    response = requests.get(f"{API_BASE_URL}/users/")

    if response.status_code == 200:
        users = response.json().get("users", [])

        if users:
            # Each row from the API looks like: [id, name, age, email]
            # Convert to a list of dicts so Streamlit can show a nice table.
            table_data = [
                {"ID": u[0], "Name": u[1], "Age": u[2], "Email": u[3]}
                for u in users
            ]
            st.table(table_data)
        else:
            st.info("No users found yet. Register one above!")
    else:
        st.error("Failed to fetch users from the API.")

except requests.exceptions.ConnectionError:
    st.error(
        "Could not connect to the API. Is it running at "
        f"{API_BASE_URL}? (Start it with: uvicorn app:app --reload)"
    )

# ------------------------------------------------------------------
# SECTION 3: Update an existing user (calls PUT /users/{id})
# ------------------------------------------------------------------
st.header("Update a User")

if not users:
    st.info("No users available to update yet.")
else:
    # Build a dropdown like "3 - Priya" so the user can pick by name,
    # but we still send the numeric ID to the API.
    user_options = {f"{u[0]} - {u[1]}": u[0] for u in users}
    selected_label = st.selectbox("Select a user to update", list(user_options.keys()), key="update_select")
    selected_id = user_options[selected_label]

    # Find the full record for the selected user so we can pre-fill the form
    selected_user = next(u for u in users if u[0] == selected_id)

    with st.form("update_form"):
        new_name = st.text_input("Name", value=selected_user[1])
        new_age = st.number_input("Age", min_value=1, max_value=120, step=1, value=selected_user[2])
        new_email = st.text_input("Email", value=selected_user[3])

        update_submitted = st.form_submit_button("Update User")

        if update_submitted:
            payload = {
                "name": new_name,
                "age": int(new_age),
                "email": new_email,
            }
            try:
                response = requests.put(f"{API_BASE_URL}/users/{selected_id}", json=payload)

                if response.status_code == 200:
                    st.success("✅ User updated successfully!")
                    st.json(response.json())
                    st.rerun()
                else:
                    # FastAPI/Pydantic validation errors, 404 (not found), and
                    # duplicate-email errors all land here.
                    st.error(f"❌ Update failed: {response.json().get('detail')}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Is it running at "
                    f"{API_BASE_URL}? (Start it with: uvicorn app:app --reload)"
                )

# ------------------------------------------------------------------
# SECTION 4: Delete a user (calls DELETE /users/{id})
# ------------------------------------------------------------------
st.header("Delete a User")

if not users:
    st.info("No users available to delete yet.")
else:
    user_options_delete = {f"{u[0]} - {u[1]}": u[0] for u in users}
    selected_label_delete = st.selectbox("Select a user to delete", list(user_options_delete.keys()), key="delete_select")
    selected_id_delete = user_options_delete[selected_label_delete]

    # Simple confirmation checkbox so a user can't delete by mis-click
    confirm_delete = st.checkbox(f"I confirm I want to delete user ID {selected_id_delete}")

    if st.button("🗑️ Delete User"):
        if not confirm_delete:
            st.warning("Please check the confirmation box before deleting.")
        else:
            try:
                response = requests.delete(f"{API_BASE_URL}/users/{selected_id_delete}")

                if response.status_code == 200:
                    st.success("✅ User deleted successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ Delete failed: {response.json().get('detail')}")

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the API. Is it running at "
                    f"{API_BASE_URL}? (Start it with: uvicorn app:app --reload)"
                )
