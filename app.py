import streamlit as st
import sqlite3
import time
# import pyttsx3

# Voice
# engine = pyttsx3.init()

st.set_page_config(page_title="Student Tracker", layout="centered")

st.title("📅 Student Task Tracker")

# DB
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    day TEXT,
    status INTEGER,
    last_time REAL,
    PRIMARY KEY (name, day)
)
""")

# Schedule
schedule = {
    "Monday": ["Aman Garg", "Abhay"],
    "Tuesday": ["Arpit Arakh", "Abhinay Suryavanshi"],
    "Wednesday": [],
    "Thursday": ["Manish Ahirwar", "Nishant Maskare"],
    "Friday": ["Pushpendra Baiga"],
    "Saturday": ["Sandeep Kumar", "Sateesh Ahirwar", "Shivam Saket", "Vishal Malviya"],
    "Sunday": ["Test Student"]
}

# UI spacing
st.markdown("### 📌 Select Day")
day = st.selectbox("", list(schedule.keys()))

students = schedule[day]
current_time = time.time()

st.markdown("---")
st.subheader("👨‍🎓 Students")

done_list = []
not_done_list = []

# Columns for better UI
col1, col2 = st.columns(2)

for i, student in enumerate(students):

    # Insert
    cursor.execute(
        "INSERT OR IGNORE INTO students (name, day, status, last_time) VALUES (?, ?, ?, ?)",
        (student, day, 0, 0)
    )
    conn.commit()

    # Fetch
    cursor.execute(
        "SELECT status, last_time FROM students WHERE name=? AND day=?",
        (student, day)
    )
    status, last_time = cursor.fetchone()

    # ⏰ 12 hour reset (change here if needed)
    if status == 1 and (current_time - last_time > 86400):
        status = 0
        cursor.execute(
            "UPDATE students SET status=?, last_time=? WHERE name=? AND day=?",
            (0, 0, student, day)
        )
        conn.commit()

    # Split UI in 2 columns
    with col1 if i % 2 == 0 else col2:
        checked = st.checkbox(f"✅ {student}", value=bool(status))

    # Update DB
    if checked != bool(status):
        new_time = time.time() if checked else 0
        cursor.execute(
            "UPDATE students SET status=?, last_time=? WHERE name=? AND day=?",
            (1 if checked else 0, new_time, student, day)
        )
        conn.commit()

    if checked:
        done_list.append(student)
    else:
        not_done_list.append(student)

st.markdown("---")

# Report Section
st.subheader("📊 Report")

colA, colB = st.columns(2)

with colA:
    st.success(f"✅ Completed: {len(done_list)}")
    st.write(done_list if done_list else "None")

with colB:
    st.error(f"❌ Not Completed: {len(not_done_list)}")
    st.write(not_done_list if not_done_list else "None")

st.markdown("---")

# 🔊 Speaker
if st.button(""):
    text = f"{len(done_list)} students completed and {len(not_done_list)} did not complete."
    # engine.say(text)
    # engine.runAndWait()

# Manual reset button
if st.button("♻️ Reset All"):
    for student in students:
        cursor.execute(
            "UPDATE students SET status=0, last_time=0 WHERE name=? AND day=?",
            (student, day)
        )
    conn.commit()
    st.success("All Reset Done!")














# import streamlit as st
# import sqlite3
# import time

# st.title("🧪 Student Tracker (Auto Fix DB + 1 Min Reset)")

# # DB connect
# conn = sqlite3.connect("students.db", check_same_thread=False)
# cursor = conn.cursor()

# # Create basic table (without last_time first)
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS students (
#     name TEXT,
#     day TEXT,
#     status INTEGER,
#     PRIMARY KEY (name, day)
# )
# """)

# # 🔥 AUTO ADD COLUMN IF NOT EXISTS
# cursor.execute("PRAGMA table_info(students)")
# columns = [col[1] for col in cursor.fetchall()]

# if "last_time" not in columns:
#     cursor.execute("ALTER TABLE students ADD COLUMN last_time REAL DEFAULT 0")
#     conn.commit()

# # Schedule
# schedule = {
#     "Monday": ["Aman Garg"],
#     "Tuesday": ["Arpit Arakh", "Abhinay Suryavanshi"],
#     "Wednesday": [],
#     "Thursday": ["Manish Ahirwar", "Nishant Maskare"],
#     "Friday": ["Pushpendra Baiga"],
#     "Saturday": ["Sandeep Kumar", "Sateesh Ahirwar", "Shivam Saket", "Vishal Malviya"],
#     "Sunday": ["Test Student"]
# }

# # Select day
# day = st.selectbox("Select Day", list(schedule.keys()))
# students = schedule[day]

# current_time = time.time()

# st.subheader("👨‍🎓 Students")

# done_list = []
# not_done_list = []

# for student in students:

#     # Insert if not exist
#     cursor.execute(
#         "INSERT OR IGNORE INTO students (name, day, status) VALUES (?, ?, ?)",
#         (student, day, 0)
#     )
#     conn.commit()

#     # Get data
#     cursor.execute(
#         "SELECT status, last_time FROM students WHERE name=? AND day=?",
#         (student, day)
#     )
#     result = cursor.fetchone()

#     status = result[0]
#     last_time = result[1] if result[1] else 0

#     # ⏰ 1 min reset per student
#     if status == 1 and (current_time - last_time > 60):
#         status = 0
#         cursor.execute(
#             "UPDATE students SET status=?, last_time=? WHERE name=? AND day=?",
#             (0, 0, student, day)
#         )
#         conn.commit()

#     # Checkbox
#     checked = st.checkbox(f"{student} - Done ✅", value=bool(status))

#     # Update DB
#     if checked != bool(status):
#         new_time = time.time() if checked else 0
#         cursor.execute(
#             "UPDATE students SET status=?, last_time=? WHERE name=? AND day=?",
#             (1 if checked else 0, new_time, student, day)
#         )
#         conn.commit()

#     # Report
#     if checked:
#         done_list.append(student)
#     else:
#         not_done_list.append(student)

# # Report UI
# st.subheader("📊 Report")
# st.write("✅ Completed:", done_list if done_list else "None")
# st.write("❌ Not Completed:", not_done_list if not_done_list else "None")









