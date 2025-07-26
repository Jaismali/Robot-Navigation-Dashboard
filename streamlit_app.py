
import streamlit as st
import plotly.graph_objects as go
from robot_class import Robot
from nlp_parser import parse_command
import speech_recognition as sr
import subprocess
import os
import time

st.set_page_config(page_title="Robot Floor Navigation", layout="wide")

# Initialize session state---------------------------------------------------------------------------------------------

if 'robot' not in st.session_state:
    st.session_state.robot = Robot()
if 'movement_history' not in st.session_state:
    st.session_state.movement_history = [st.session_state.robot.location]
if 'last_voice_result' not in st.session_state:
    st.session_state.last_voice_result = ""
if 'last_chat_voice_result' not in st.session_state:
    st.session_state.last_chat_voice_result = ""
if 'auto_tasks' not in st.session_state:
    st.session_state.auto_tasks = []
if 'auto_step' not in st.session_state:
    st.session_state.auto_step = 0
if 'auto_running' not in st.session_state:
    st.session_state.auto_running = False

robot = st.session_state.robot
history = st.session_state.movement_history

# --- Header -----------------------------------------------------------------------------------------------------------

st.title("🤖 Robot Navigation & Control Dashboard")
col1, col2 = st.columns([2, 1])

# --- Floor Tracker ----------------------------------------------------------------------------------------------------

with col1:
    st.subheader("📍 Robot Floor Tracker")
    floors = [f"Lab {i}" for i in range(8, -1, -1)]
    current_location = robot.location.strip().lower()
    floor_colors = [
        "deepskyblue" if f.strip().lower() == current_location else "lightgray"
        for f in floors
    ]
    fig = go.Figure(go.Bar(
        x=[1]*len(floors),
        y=floors,
        orientation='h',
        marker_color=floor_colors,
        hovertext=floors,
        showlegend=False
    ))
    fig.update_layout(
        height=500,
        width=400,
        xaxis_visible=False,
        yaxis=dict(autorange='reversed'),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    st.plotly_chart(fig)

# --- Telemetry --------------------------------------------------------------------------------------------------------

with col2:
    st.subheader("⚙️ Robot Telemetry")
    st.metric(label="Battery Level", value=f"{robot.battery}%")
    st.metric(label="Speed", value=f"{robot.speed} m/s")
    st.metric(label="Status", value=robot.status)

# --- Task Management --------------------------------------------------------------------------------------------------

st.subheader("📦 Task Queue Management")
task_input = st.text_input("Enter a delivery task (e.g., Deliver to Lab 2):")

c1, c2 = st.columns([1, 1])
with c1:
    if st.button("➕ Add Task", use_container_width=True):
        if task_input:
            robot.add_task(task_input)
            st.success(f"✅ Task added: {task_input}")

with c2:
    if st.button("📋 Queue & Auto Deliver", use_container_width=True):
        if task_input:
            robot.add_task(task_input)
            st.success(f"✅ Task added: {task_input}")
        if robot.task_queue:
            st.session_state.auto_tasks = robot.task_queue.copy()
            st.session_state.auto_step = 0
            st.session_state.auto_running = True
            robot.task_queue.clear()
            st.rerun()

# --- Auto Task Execution ----------------------------------------------------------------------------------------------

if st.session_state.auto_running:
    tasks = st.session_state.auto_tasks
    step = st.session_state.auto_step

    if step < len(tasks):
        task = tasks[step]
        intent, location = parse_command(task)
        if intent == "move" and location:
            robot.goto(location)
            history.append(location)
            st.session_state.robot = robot
            st.info(f"🚚 Delivering to {location}...")
            st.session_state.auto_step += 1
            time.sleep(1.2)
            st.rerun()
    else:
        st.success("🎉 All deliveries completed via Auto Mode!")
        st.session_state.auto_running = False

# --- Voice Command Input ----------------------------------------------------------------------------------------------

st.subheader("🎙️ Voice Command Input")
voice_cmd = st.text_input("Type or speak a command like 'go to lab 4':", key="voice_input")
col_exec, col_mic, _ = st.columns([1, 1, 6])
execute_pressed = col_exec.button("▶️ Execute Command", key="btn_execute")
mic_pressed = col_mic.button("🎤 Speak", key="btn_mic")

if execute_pressed:
    intent, location = parse_command(voice_cmd)
    st.success(f"Intent: {intent}, Location: {location}")
    if intent == "move" and location:
        robot.goto(location)
        history.append(robot.location)
        st.success(f"✅ Robot moved to {location}")
        st.rerun()
    elif intent == "move":
        st.warning("⚠️ Could not parse target lab.")

if mic_pressed:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5)
            result = recognizer.recognize_google(audio)
            st.session_state.last_voice_result = result
            intent, location = parse_command(result)
            if intent == "move" and location:
                robot.goto(location)
                history.append(robot.location)
                st.success(f"✅ Robot moved to {location}")
                st.rerun()
            elif intent == "move":
                st.warning("⚠️ Could not parse target lab.")
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError:
            st.error("🚫 Voice recognition API unavailable.")

# --- Chat Assistant --------------------------------------------------------------------------------------------------

st.subheader("💬 Robot Chat Assistant")
chat_query = st.text_input("Ask something about the robot:", key="chat_input")
col_chat_ask, col_chat_speak, _ = st.columns([1, 1, 6])
ask_btn = col_chat_ask.button("Ask Assistant", key="chat_ask_btn")
speak_btn = col_chat_speak.button("🎤 Speak", key="chat_speak_btn")

def get_intent_from_query(query):
    query = query.lower()
    if any(k in query for k in ["battery", "charge", "power", "percentage"]):
        return "battery"
    if any(k in query for k in ["location", "where", "position", "floor"]):
        return "location"
    if any(k in query for k in ["status", "idle", "working", "moving", "condition"]):
        return "status"
    return "unknown"

def handle_chat_query(query):
    intent = get_intent_from_query(query)
    if intent == "battery":
        st.write(f"🔋 Battery: {robot.battery}%")
    elif intent == "location":
        st.write(f"📍 Location: {robot.location}")
    elif intent == "status":
        st.write(f"⚙️ Status: {robot.status}")
    else:
        st.info("🤖 Sorry, I’m still learning to understand that.")

if ask_btn and chat_query:
    handle_chat_query(chat_query)

if speak_btn:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            with st.spinner("🎤 Listening to your chat query..."):
                audio = recognizer.listen(source, timeout=5)

            result = recognizer.recognize_google(audio)
            st.session_state.last_chat_voice_result = result
            handle_chat_query(result)

        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError:
            st.error("🚫 Voice recognition API unavailable.")

# --- Voice Recap ------------------------------------------------------------------------------------------------------

with st.expander("🗣️ View Voice Input Recap"):
    if st.session_state.last_voice_result:
        st.success(f"Command You Said: '{st.session_state.last_voice_result}'")
    if st.session_state.last_chat_voice_result:
        st.success(f"Chat You Said: '{st.session_state.last_chat_voice_result}'")

# --- Movement History -------------------------------------------------------------------------------------------------

with st.expander("🕒 View Movement History"):
    for i, loc in enumerate(robot.history[::-1]):
        st.write(f"{len(robot.history) - i}. {loc}")

# --- Simulations ------------------------------------------------------------------------------------------------------

st.subheader("🎮 Launch Simulations")
colsim1, colsim2, colsim3 = st.columns(3)

if colsim1.button("🔹 Launch 2D PyGame Sim"):
    subprocess.Popen(["python", "pygame_sim.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    st.success("✅ 2D Simulator launched in new window!")

if colsim2.button("🧲 Launch 3D PyBullet Sim"):
    subprocess.Popen(["python", "pybullet_sim.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    st.success("✅ 3D Simulator launched in new window!")

if colsim3.button("🧮 Launch Floor Simulation"):
    subprocess.Popen(["python", "AI_VirtualBot_Controller/main.py"], creationflags=subprocess.CREATE_NO_WINDOW)
    st.success("✅ Floor Simulation launched in new window!")

# --- Footer -----------------------------------------------------------------------------------------------------------

st.caption("Enhanced by Jai | AIML Internship Project")
