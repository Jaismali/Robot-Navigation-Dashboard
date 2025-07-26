# 🤖 Robot Navigation & Control Dashboard

An interactive delivery bot simulation dashboard built using **Python** and **Streamlit**. This project allows users to control a robot for delivery tasks across multiple floors, visualize its location, queue tasks, and simulate movement in 2D, 3D, and multi-floor environments. This was built as an internship project at CDAC 2025.

---

## 🧠 What is This Project?

The Robot Navigation Dashboard is a smart delivery bot controller that lets users:
- Assign delivery tasks by voice or text
- Track the robot's real-time location across 9 labs (floors)
- Run multiple types of visual simulations (2D/3D/Floor layout)
- Manage robot movement history and task queue with automation

---

## 🚀 Features

✅ Real-time robot location tracker (Plotly-based)  
✅ Voice and text-based command parsing  
✅ Task queueing with **Auto Delivery Mode**  
✅ Multi-floor simulation with obstacles  
✅ 2D PyGame and 3D PyBullet launchers  
✅ Chat assistant for querying robot status  
✅ Modern Streamlit UI with collapsible history and recap  
✅ Modular and maintainable code structure

---

## 💻 Technologies Used

- **Python** – Core language  
- **Streamlit** – Front-end web dashboard  
- **Plotly** – Robot floor tracking visual  
- **SpeechRecognition** – Voice command support (local only)  
- **PyGame** – 2D simulation  
- **PyBullet** – 3D simulation  
- **Tkinter** – Multi-floor visual controller  
- **scikit-learn** – (Optional) command classification

---

## 🎮 How to Use

### ▶️ Local (Recommended - Full Features)

```bash
git clone https://github.com/Jaismali/Robot-Navigation-Dashboard.git
cd Robot-Navigation-Dashboard
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Make sure PyAudio is installed for voice commands:
```bash
pip install pyaudio
```
🌐 On Streamlit Cloud
Hosted link: https://jaismali-robot-navigation-dashboard.streamlit.app

> ⚠️ The following features are only available when run **locally**:
> - Voice input via microphone
> - 2D PyGame simulation
> - 3D PyBullet simulation
> - Floor Simulation (Tkinter GUI)
>
> These require desktop environments and cannot be rendered in Streamlit Cloud.

---


## 🗺️ Simulations
You can launch:

🔹 2D PyGame simulation

🧲 3D PyBullet simulation

🧮 Multi-floor GUI simulation with room layouts and collision detection

Each simulation opens in a separate window and runs locally.

---

## 📸 Previews

📋 Task Queue & Auto Mode in Action
---
<img width="2559" height="1327" alt="Screenshot 2025-07-27 001912" src="https://github.com/user-attachments/assets/167ca9fa-8138-4ea7-abf2-d7c88cf148f8" />

💬 Chat Assistant Interaction
---
<img width="1280" height="619" alt="image" src="https://github.com/user-attachments/assets/488dd4ad-ef4c-4b8a-b7b9-01087b193ce5" />

🧮 Floor Simulation (Tkinter)
---
<img width="2559" height="1522" alt="Screenshot 2025-07-27 002923" src="https://github.com/user-attachments/assets/e0326323-13b5-4b1b-aaa2-b7957975b75f" />

---

## 🛠️ Author
Jai Mali – @jaismali

Built as part of an AIML Internship Project at CDAC (2025)


