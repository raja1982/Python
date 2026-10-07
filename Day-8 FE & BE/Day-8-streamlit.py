# to install : pip install streamlit
# to run the streamlit code : streamlit run Day-8-streamlit.py
# ================================================================================

import time
from datetime import datetime, date

import numpy as np
import pandas as pd
import streamlit as st

# =====================================================================
# 1. PAGE CONFIGURATION
# =====================================================================
# Must be the FIRST Streamlit command in the script, called only once.
st.set_page_config(
    page_title="Streamlit Cheat Sheet",   # Browser tab title
    page_icon="📘",                        # Emoji or image path shown in tab
    layout="wide",                         # "centered" (default) or "wide"
    initial_sidebar_state="expanded",      # "auto", "expanded", "collapsed"
)

# =====================================================================
# 2. TEXT & MARKDOWN ELEMENTS
# =====================================================================
st.title("📘 Streamlit Command Reference")          # Biggest heading, once per page
st.header("2. Text & Markdown Elements")             # Section-level heading
st.subheader("A smaller heading under the header")   # Sub-section heading

st.markdown(
    "st.markdown() — supports **bold**, *italics*, `code`, "
    "[links](https://streamlit.io), and even :blue[colored text]."
)

st.caption("st.caption() — small, greyed-out text. Great for footnotes/hints.")

st.write(
    "st.write() is the SWISS-ARMY KNIFE — it accepts almost anything "
    "(strings, numbers, dataframes, charts, dicts) and renders the "
    "right thing automatically. When in doubt, use st.write()."
)
st.write("Hello World")
st.write(100)
st.write(["Python", "Streamlit", "FastAPI"])
student = {
    "name": "John",
    "age": 25,
    "course": "Python"
}

st.write(student)
st.write("**Hello**")
st.write("# Employee Details")
st.divider()  # Horizontal rule to visually separate sections

# =====================================================================
# 3. BASIC INPUT WIDGETS
# =====================================================================
st.header("3. Basic Input Widgets")
# Every widget RETURNS its current value — assign it to a variable.

name = st.text_input(
    "st.text_input() — single-line text",
    value="Learner",             # default value
    placeholder="Type your name",
    max_chars=50,
)
st.write(name)

bio = st.text_area(
    "st.text_area() — multi-line text",
    height=100,
)
st.write(bio)

age = st.number_input(
    "st.number_input() — numeric entry with +/- steppers",
    min_value=0, max_value=120, value=25, step=1,
)
st.write(age)

score = st.slider(
    "st.slider() — pick a value (or a range) with a slider",
    min_value=0, max_value=100, value=50,
)
st.write(score)

price_range = st.slider(
    "st.slider() — RANGE version (pass a tuple as default)",
    0, 1000, (200, 800),
)
st.write(price_range)

# =====================================================================
# 4. SELECTION WIDGETS
# =====================================================================
st.header("4. Selection Widgets")

language = st.selectbox(
    "st.selectbox() — pick ONE option from a dropdown",
    options=["Python", "JavaScript", "Java", "Go"],
)
st.write(language) # this is eqvivalent to dropdown

skills = st.multiselect(
    "st.multiselect() — pick MULTIPLE options",
    options=["ML", "DL", "GenAI", "RAG", "Agents"],
    default=["ML", "GenAI"],
)
st.write(skills)

experience = st.radio(
    "st.radio() — pick ONE option, all visible at once",
    options=["Beginner", "Intermediate", "Advanced"],
    horizontal=True,   # lay the options out side-by-side
)
st.write(experience)

agree = st.checkbox("st.checkbox() — simple True/False toggle")
st.write(agree)

notify = st.toggle("st.toggle() — modern on/off switch (same idea as checkbox)")
st.write(notify)

rating = st.select_slider(
    "st.select_slider() — slider over discrete, non-numeric options",
    options=["Poor", "Fair", "Good", "Great", "Excellent"],
    value="Good",
)
st.write(rating)

# =====================================================================
# 5. BUTTON-LIKE WIDGETS
# =====================================================================
st.header("5. Button-like Widgets")

if st.button("st.button() — a simple click button", type="primary"):
    st.write("Button was clicked! (This only shows right after a click)")

st.link_button("st.link_button() — button that opens a URL", "https://docs.streamlit.io")

st.download_button(
    "st.download_button() — download some in-memory data as a file",
    data="Hello from Streamlit!",
    file_name="sample.txt",
    mime="text/plain",
)

# =====================================================================
# 6. DATE & TIME WIDGETS
# =====================================================================
st.header("6. Date & Time Widgets")

dob = st.date_input(
    "st.date_input() — pick a date",
    value=date(2000, 1, 1),
)
st.write(dob)

wake_time = st.time_input(
    "st.time_input() — pick a time",
    value=datetime.now().time(),
)
st.write(wake_time)

# =====================================================================
# 7. LAYOUT ELEMENTS
# =====================================================================
st.header("7. Layout Elements")

# --- Sidebar: put controls/filters out of the main flow ---
st.sidebar.header("Sidebar controls")
sidebar_choice = st.sidebar.selectbox("Pick a view", ["Overview", "Details"])

# =====================================================================
# 8. DISPLAYING DATA
# =====================================================================
st.header("8. Displaying Data")

sample_df = pd.DataFrame(
    {"Name": ["Asha", "Ravi", "Meera"], "Score": [88, 92, 79]}
)

# st.dataframe(sample_df, use_container_width=True)   # Interactive, scrollable, sortable
st.table(sample_df)                                  # Static, non-interactive table

# Metrics — great for KPIs / stat callouts, with an optional delta indicator
m1, m2 = st.columns(2)
m1.metric(label="Average Score", value="86.3", delta="+2.1")
m2.metric(label="Pass Rate", value="94%", delta="-1%")

# =====================================================================
# 9. CHARTS & VISUALIZATIONS
# =====================================================================
st.header("9. Charts & Visualizations")

chart_data = pd.DataFrame(
    np.random.randn(10, 3), columns=["A", "B", "C"]
)

# Quick line chart directly from a DataFrame
if sidebar_choice == "Overview":
    st.line_chart(chart_data)
else:
    st.table(chart_data)
        
st.bar_chart(chart_data)      # Quick bar chart
st.area_chart(chart_data)     # Quick area chart
st.scatter_chart(chart_data, x="A", y="B")  # Quick scatter plot

# For anything more custom, pass a Matplotlib/Plotly figure:
# st.pyplot(fig)          # Matplotlib figure
# st.plotly_chart(fig)    # Plotly figure
st.map(pd.DataFrame({
    "lat": [18.5204, 28.6139],
    "lon": [73.8567, 77.2090],
}))  # Plots points on a map given lat/lon columns

# =====================================================================
# 11. FILE UPLOAD & DOWNLOAD
# =====================================================================
st.header("11. File Upload & Download")

uploaded_file = st.file_uploader(
    "st.file_uploader() — upload a file",
    type=["csv", "txt"],       # restrict allowed extensions
    accept_multiple_files=False,
)
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        st.dataframe(pd.read_csv(uploaded_file))
    else:
        st.text(uploaded_file.read().decode("utf-8"))

# =====================================================================
# 13. FORMS — batch multiple inputs, submit together
# =====================================================================
st.header("13. Forms")
st.caption(
    "Normally EVERY widget triggers an immediate rerun. Wrapping "
    "widgets in st.form() batches them — the script only reruns "
    "when the form's submit button is pressed."
)

with st.form("registration_form"):
    f_name = st.text_input("Full name")
    st.write(f_name)
    f_email = st.text_input("Email")
    st.write(f_email)
    f_submit = st.form_submit_button("Submit")
    st.write(f_submit)

if f_submit == True:
    # add conditions according to the requirement
    st.success(f"Registered: {f_name} ({f_email})")

# =====================================================================
# 14. Progress Bar
# =====================================================================
st.header("14. Progress Bar")
import time

st.title("Progress Bar Demo")

progress_bar = st.progress(0)

for i in range(101):
    time.sleep(0.03)
    progress_bar.progress(i)

st.success("Process completed!")
















