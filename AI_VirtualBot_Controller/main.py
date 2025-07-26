# ========== IMPORTS ==========
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json

# External modules for bot logic and command parsing
from controllers.bot_controller import VirtualBotController
from ai_module.command_parser import parse_command_ai

# ========== MAIN WINDOW SETUP ==========
root = tk.Tk()
root.geometry("800x900")  # Adjust window size
root.resizable(False, False)  # Prevent resizing if you want it fixed
window_width = 800
window_height = 1000

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2) - 50  # ⬆️ move window 60px higher

root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.title("Delivery Robot Controller")
root.configure(bg="#f0f4f8")

# Title + Instructions
tk.Label(root, text="Delivery Robot Controller", font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
tk.Label(root, text="Navigate the delivery robot on different floors. Each floor has its own navigation area.", font=("Arial", 11), bg="#f0f4f8", fg="#555").pack(pady=5)

# ========== FLOOR SELECTION AREA ==========
floor_frame = tk.Frame(root, bg="#f0f4f8")
floor_frame.pack(pady=10)

tk.Label(floor_frame, text="Current Floor:", font=("Arial", 12, "bold"), bg="#f0f4f8", fg="#333").pack(side=tk.LEFT, padx=5)

current_floor = tk.IntVar(value=1)
floor_display = tk.Label(floor_frame, text="Floor 1", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=10, pady=2, relief="raised")
floor_display.pack(side=tk.LEFT, padx=5)

# Buttons to switch floors
floor_btn_frame = tk.Frame(floor_frame, bg="#f0f4f8")
floor_btn_frame.pack(side=tk.LEFT, padx=20)
tk.Label(floor_btn_frame, text="Go to Floor:", font=("Arial", 10), bg="#f0f4f8").pack()
floor_buttons_frame = tk.Frame(floor_btn_frame, bg="#f0f4f8")
floor_buttons_frame.pack()

# ========== CANVAS AREA FOR EACH FLOOR ==========
canvas_frame = tk.Frame(root, bg="#f0f4f8")
canvas_frame.pack()

# Store canvases, bots, and data for all floors
floor_canvases = {}
floor_bots = {}
floor_data = {}
floor_obstacles = {}

# Define each floor with background and label
floor_configs = {
    1: {"bg": "#ffffff", "name": "Ground Floor - Lobby"},
    2: {"bg": "#f8f8ff", "name": "Floor 2 - Offices"},
    3: {"bg": "#f0f8ff", "name": "Floor 3 - Conference Rooms"},
    4: {"bg": "#f5f5dc", "name": "Floor 4 - Cafeteria"},
    5: {"bg": "#fff8dc", "name": "Floor 5 - Labs"},
    6: {"bg": "#ffefd5", "name": "Floor 6 - R&D"},
    7: {"bg": "#ffe4e1", "name": "Floor 7 - Management"},
    8: {"bg": "#f0e68c", "name": "Floor 8 - Server Room"}
}
# ========== HELPER: ADD FLOOR LAYOUT (ROOMS, OBSTACLES) ==========
# Replace the add_floor_layout function with this updated version

def add_floor_layout(canvas, floor_num):
    obstacles = []

    if floor_num == 1:  # Lobby
        canvas.create_rectangle(50, 50, 150, 150, fill="#e0e0e0", outline="#999", width=2)
        canvas.create_text(100, 100, text="Reception", font=("Arial", 10, "bold"))
        obstacles.append((50, 50, 150, 150))

        canvas.create_rectangle(400, 200, 450, 300, fill="#d0d0d0", outline="#666", width=2)
        canvas.create_text(425, 250, text="Elevator", font=("Arial", 8))
        obstacles.append((400, 200, 450, 300))

        canvas.create_rectangle(200, 450, 300, 480, fill="#8bc34a", outline="#4caf50", width=3)
        canvas.create_text(250, 465, text="Entrance", font=("Arial", 9))

    elif floor_num == 2:  # Offices
        for i, (x, y) in enumerate([(50, 50), (250, 50), (50, 250), (250, 250)]):
            canvas.create_rectangle(x, y, x + 100, y + 100, fill="#f5f5f5", outline="#999", width=1)
            canvas.create_text(x + 50, y + 50, text=f"Office {i + 1}", font=("Arial", 9))
            obstacles.append((x, y, x + 100, y + 100))

        canvas.create_rectangle(180, 180, 320, 220, fill="#e8f4fd", outline="#2196f3", width=1)
        canvas.create_text(250, 200, text="Corridor", font=("Arial", 9))

    elif floor_num == 3:  # Conference Rooms
        canvas.create_rectangle(100, 100, 400, 250, fill="#fff9c4", outline="#ffc107", width=2)
        canvas.create_text(250, 175, text="Main Conference Room", font=("Arial", 12, "bold"))
        obstacles.append((100, 100, 400, 250))

        canvas.create_rectangle(50, 300, 150, 400, fill="#e8f5e8", outline="#4caf50", width=1)
        canvas.create_text(100, 350, text="Meeting\nRoom A", font=("Arial", 9))
        obstacles.append((50, 300, 150, 400))

        canvas.create_rectangle(350, 300, 450, 400, fill="#e8f5e8", outline="#4caf50", width=1)
        canvas.create_text(400, 350, text="Meeting\nRoom B", font=("Arial", 9))
        obstacles.append((350, 300, 450, 400))

    elif floor_num == 4:  # Cafeteria
        # Main dining area (smaller, more space around)
        canvas.create_rectangle(100, 100, 300, 200, fill="#fff8dc", outline="#daa520", width=2)
        canvas.create_text(200, 150, text="Main Dining Area", font=("Arial", 10, "bold"))
        obstacles.append((100, 100, 300, 200))

        # Kitchen
        canvas.create_rectangle(50, 350, 150, 450, fill="#ffe4b5", outline="#d2691e", width=2)
        canvas.create_text(100, 400, text="Kitchen", font=("Arial", 9, "bold"))
        obstacles.append((50, 350, 150, 450))

        # Serving counter
        canvas.create_rectangle(320, 120, 450, 150, fill="#f0e68c", outline="#b8860b", width=2)
        canvas.create_text(385, 135, text="Serving Counter", font=("Arial", 8))
        obstacles.append((320, 120, 450, 150))

        # Vending machines
        canvas.create_rectangle(350, 350, 400, 450, fill="#dcdcdc", outline="#696969", width=2)
        canvas.create_text(375, 400, text="Vending", font=("Arial", 8))
        obstacles.append((350, 350, 400, 450))

    elif floor_num == 5:  # Labs
        # Main laboratory
        canvas.create_rectangle(70, 70, 250, 200, fill="#f0ffff", outline="#4682b4", width=2)
        canvas.create_text(160, 135, text="Main Laboratory", font=("Arial", 10, "bold"))
        obstacles.append((70, 70, 250, 200))

        # Chemical storage
        canvas.create_rectangle(300, 50, 450, 150, fill="#ffe4e1", outline="#dc143c", width=2)
        canvas.create_text(375, 100, text="Chemical\nStorage", font=("Arial", 9))
        obstacles.append((300, 50, 450, 150))

        # Equipment room
        canvas.create_rectangle(50, 250, 180, 380, fill="#f5f5dc", outline="#8b4513", width=2)
        canvas.create_text(115, 315, text="Equipment\nRoom", font=("Arial", 9))
        obstacles.append((50, 250, 180, 380))

        # Research station
        canvas.create_rectangle(220, 280, 370, 410, fill="#e6e6fa", outline="#9370db", width=2)
        canvas.create_text(295, 345, text="Research\nStation", font=("Arial", 9))
        obstacles.append((220, 280, 370, 410))

        # Safety shower
        canvas.create_rectangle(400, 200, 450, 250, fill="#98fb98", outline="#228b22", width=2)
        canvas.create_text(425, 225, text="Safety", font=("Arial", 8))
        obstacles.append((400, 200, 450, 250))

    elif floor_num == 6:  # R&D
        # Main R&D lab
        canvas.create_rectangle(60, 60, 300, 220, fill="#f0f8ff", outline="#4169e1", width=2)
        canvas.create_text(180, 140, text="R&D Laboratory", font=("Arial", 11, "bold"))
        obstacles.append((60, 60, 300, 220))

        # Prototype workshop
        canvas.create_rectangle(330, 80, 470, 200, fill="#ffefd5", outline="#ff8c00", width=2)
        canvas.create_text(400, 140, text="Prototype\nWorkshop", font=("Arial", 9))
        obstacles.append((330, 80, 470, 200))

        # Design studio
        canvas.create_rectangle(80, 260, 220, 400, fill="#f5fffa", outline="#00fa9a", width=2)
        canvas.create_text(150, 330, text="Design\nStudio", font=("Arial", 9))
        obstacles.append((80, 260, 220, 400))

        # Testing chamber
        canvas.create_rectangle(260, 280, 400, 420, fill="#fffaf0", outline="#ffd700", width=2)
        canvas.create_text(330, 350, text="Testing\nChamber", font=("Arial", 9))
        obstacles.append((260, 280, 400, 420))

        # 3D printer station
        canvas.create_rectangle(50, 430, 150, 480, fill="#e0e0e0", outline="#778899", width=2)
        canvas.create_text(100, 455, text="3D Printers", font=("Arial", 8))
        obstacles.append((50, 430, 150, 480))

    elif floor_num == 7:  # Management
        # CEO office
        canvas.create_rectangle(80, 80, 200, 180, fill="#fff0f5", outline="#db7093", width=2)
        canvas.create_text(140, 130, text="CEO Office", font=("Arial", 10, "bold"))
        obstacles.append((80, 80, 200, 180))

        # Board room
        canvas.create_rectangle(320, 60, 450, 160, fill="#f8f8ff", outline="#6a5acd", width=2)
        canvas.create_text(385, 110, text="Board Room", font=("Arial", 9, "bold"))
        obstacles.append((320, 60, 450, 160))

        # HR department
        canvas.create_rectangle(50, 250, 150, 350, fill="#ffe4e1", outline="#fa8072", width=2)
        canvas.create_text(100, 300, text="HR Dept", font=("Arial", 9))
        obstacles.append((50, 250, 150, 350))

        # Finance office
        canvas.create_rectangle(300, 250, 420, 350, fill="#f0fff0", outline="#32cd32", width=2)
        canvas.create_text(360, 300, text="Finance\nOffice", font=("Arial", 9))
        obstacles.append((300, 250, 420, 350))

        # Reception area
        canvas.create_rectangle(170, 400, 330, 450, fill="#fafafa", outline="#c0c0c0", width=2)
        canvas.create_text(250, 425, text="Reception", font=("Arial", 9))
        obstacles.append((170, 400, 330, 450))

    elif floor_num == 8:  # Server Room
        # Main server rack area (much smaller to allow movement)
        canvas.create_rectangle(100, 100, 300, 220, fill="#f5f5f5", outline="#2f4f4f", width=3)
        canvas.create_text(200, 160, text="Server Racks", font=("Arial", 11, "bold"))
        obstacles.append((100, 100, 300, 220))

        # UPS room
        canvas.create_rectangle(50, 350, 130, 450, fill="#fffacd", outline="#bdb76b", width=2)
        canvas.create_text(90, 400, text="UPS Room", font=("Arial", 9))
        obstacles.append((50, 350, 130, 450))

        # Cooling system
        canvas.create_rectangle(350, 350, 450, 450, fill="#e0ffff", outline="#00ced1", width=2)
        canvas.create_text(400, 400, text="Cooling\nSystem", font=("Arial", 9))
        obstacles.append((350, 350, 450, 450))

        # Network equipment
        canvas.create_rectangle(350, 80, 450, 150, fill="#f0f0f0", outline="#708090", width=2)
        canvas.create_text(400, 115, text="Network\nEquip", font=("Arial", 8))
        obstacles.append((350, 80, 450, 150))

        # Monitoring station
        canvas.create_rectangle(50, 280, 120, 330, fill="#ffe4b5", outline="#daa520", width=2)
        canvas.create_text(85, 305, text="Monitor", font=("Arial", 8))
        obstacles.append((50, 280, 120, 330))

    floor_obstacles[floor_num] = obstacles


# ========== COLLISION CHECK ==========
def check_collision(x, y, floor_num, radius=10):
    if floor_num not in floor_obstacles:
        return False

    for x1, y1, x2, y2 in floor_obstacles[floor_num]:
        if (x - radius < x2 and x + radius > x1 and
            y - radius < y2 and y + radius > y1):
            return True

    # Check canvas boundaries
    if x - radius < 0 or x + radius > 500 or y - radius < 0 or y + radius > 500:
        return True

    return False


# ========== OVERRIDE BOT MOVEMENT WITH COLLISION CHECK ==========
original_move_methods = {}

def override_bot_with_collision(bot, floor_num):
    if hasattr(bot, '_collision_added'):
        return

    original_move_methods[bot] = {
        'move_bot': bot.move_bot,
        'move_bot_diagonal': bot.move_bot_diagonal,
        'move_bot_bezier': bot.move_bot_bezier
    }

    def safe_move(direction, distance):
        old_x, old_y = bot.x, bot.y
        original_move_methods[bot]['move_bot'](direction, distance)
        if check_collision(bot.x, bot.y, floor_num):
            bot.x, bot.y = old_x, old_y
            bot.update_position()
            error_label.config(text="Movement blocked by obstacle!")
            add_history("Movement blocked by obstacle!")
            return False
        return True

    def safe_move_diagonal(direction, distance):
        old_x, old_y = bot.x, bot.y
        original_move_methods[bot]['move_bot_diagonal'](direction, distance)
        if check_collision(bot.x, bot.y, floor_num):
            bot.x, bot.y = old_x, old_y
            bot.update_position()
            error_label.config(text="Diagonal movement blocked!")
            add_history("Diagonal movement blocked by obstacle!")
            return False
        return True

    def safe_bezier(x1, y1, x2, y2, x3, y3):
        old_x, old_y = bot.x, bot.y
        original_move_methods[bot]['move_bot_bezier'](x1, y1, x2, y2, x3, y3)
        if check_collision(bot.x, bot.y, floor_num):
            bot.x, bot.y = old_x, old_y
            bot.update_position()
            error_label.config(text="Bezier movement blocked!")
            add_history("Bezier movement blocked by obstacle!")
            return False
        return True

    bot.move_bot = safe_move
    bot.move_bot_diagonal = safe_move_diagonal
    bot.move_bot_bezier = safe_bezier
    bot._collision_added = True


# ========== INITIALIZE EACH FLOOR (Canvas, Bot, Obstacles) ==========
for floor_num in range(1, 9):
    canvas = tk.Canvas(canvas_frame, width=500, height=500,
                       bg=floor_configs[floor_num]["bg"],
                       highlightthickness=2, highlightbackground="#aaa")

    add_floor_layout(canvas, floor_num)
    floor_canvases[floor_num] = canvas

    bot = VirtualBotController(canvas)
    floor_bots[floor_num] = bot

    override_bot_with_collision(bot, floor_num)

    floor_data[floor_num] = {
        "x": 250,
        "y": 250,
        "path": [],
        "color": "blue"
    }

    # Show floor 1 initially
    if floor_num == 1:
        canvas.pack()
    else:
        canvas.pack_forget()

current_canvas = floor_canvases[1]
current_bot = floor_bots[1]
# ========== UPDATE FLOOR INFO ==========
floor_info = tk.Label(root, text=floor_configs[1]["name"], font=("Arial", 11), bg="#f0f4f8", fg="#666")
floor_info.pack()

def update_floor_info():
    floor_info.config(text=floor_configs[current_floor.get()]["name"])


# ========== FLOOR SWITCH FUNCTION ==========
def change_floor(floor_num):
    global current_canvas, current_bot

    # Save current floor's state
    old_floor = current_floor.get()
    floor_data[old_floor] = {
        "x": current_bot.x,
        "y": current_bot.y,
        "path": current_bot.path.copy(),
        "color": current_bot.color
    }

    # Hide current canvas
    current_canvas.pack_forget()

    # Update and show new canvas
    current_floor.set(floor_num)
    floor_display.config(text=f"Floor {floor_num}")
    current_canvas = floor_canvases[floor_num]
    current_bot = floor_bots[floor_num]
    current_canvas.pack()

    # Restore saved state
    data = floor_data[floor_num]
    current_bot.x = data["x"]
    current_bot.y = data["y"]
    current_bot.path = data["path"].copy()
    current_bot.color = data["color"]
    current_bot.update_position()
    current_bot.change_color(data["color"])

    # Redraw path
    current_canvas.delete("path_line")
    for x0, y0, x1, y1 in current_bot.path:
        current_canvas.create_line(x0, y0, x1, y1, fill="blue", tags="path_line")

    add_history(f"Moved to {floor_configs[floor_num]['name']}")
    update_floor_info()

# Add floor buttons
for i in range(1, 9):
    tk.Button(floor_buttons_frame, text=str(i), width=3, font=("Arial", 10),
              command=lambda f=i: change_floor(f), bg="#e3f2fd", relief="raised").pack(side=tk.LEFT, padx=1)


# ========== DELIVERY STATUS DISPLAY ==========
delivery_frame = tk.Frame(root, bg="#f0f4f8")
delivery_frame.pack(pady=5)

delivery_status = tk.StringVar(value="Ready for delivery")

tk.Label(delivery_frame, text="Status:", font=("Arial", 11, "bold"), bg="#f0f4f8").pack(side=tk.LEFT)
tk.Label(delivery_frame, textvariable=delivery_status, font=("Arial", 11), bg="#f0f4f8", fg="#2196F3").pack(side=tk.LEFT, padx=5)


# ========== COMMAND INPUT ==========
entry_frame = tk.Frame(root, bg="#f0f4f8")
entry_frame.pack(pady=5)

tk.Label(entry_frame, text="Command:", font=("Arial", 12), bg="#f0f4f8").pack(side=tk.LEFT)

entry = tk.Entry(entry_frame, width=40, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)

tk.Button(entry_frame, text="Execute", font=("Arial", 11), command=lambda: execute_command()).pack(side=tk.LEFT)


# ========== MOVEMENT BUTTON GRID ==========
btn_frame = tk.Frame(root, bg="#f0f4f8")
btn_frame.pack(pady=10)

def move_cmd(cmd):
    entry.delete(0, tk.END)
    entry.insert(0, cmd)
    execute_command()

btns = [
    ("↖", "forward-left"), ("↑", "forward"), ("↗", "forward-right"),
    ("←", "left"),         ("🏠", "reset"),  ("→", "right"),
    ("↙", "backward-left"), ("↓", "backward"), ("↘", "backward-right")
]

for i, (label, cmd) in enumerate(btns):
    bg = "#ffcdd2" if cmd == "reset" else "#e8f5e8"
    tk.Button(btn_frame, text=label, width=8, font=("Arial", 11), bg=bg,
              command=lambda c=cmd: move_cmd(c)).grid(row=i//3, column=i%3, padx=2, pady=2)


# ========== DELIVERY ACTION BUTTONS ==========
action_frame = tk.Frame(root, bg="#f0f4f8")
action_frame.pack(pady=5)

def pickup_delivery():
    delivery_status.set(f"Carrying delivery on Floor {current_floor.get()}")
    add_history(f"Picked up delivery on Floor {current_floor.get()}")

def drop_delivery():
    delivery_status.set(f"Delivered on Floor {current_floor.get()}")
    add_history(f"Delivered package on Floor {current_floor.get()}")

def return_base():
    change_floor(1)
    delivery_status.set("Returned to base (Floor 1)")
    current_bot.reset_bot()
    add_history("Robot returned to base station")

tk.Button(action_frame, text="📦 Pickup", font=("Arial", 11), bg="#fff3e0", command=pickup_delivery).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="🚚 Deliver", font=("Arial", 11), bg="#e8f5e8", command=drop_delivery).pack(side=tk.LEFT, padx=5)
tk.Button(action_frame, text="🏠 Return to Base", font=("Arial", 11), bg="#e3f2fd", command=return_base).pack(side=tk.LEFT, padx=5)


# ========== ACTIVITY LOG & ERROR DISPLAY ==========
tk.Label(root, text="Activity Log:", font=("Arial", 12, "bold"), bg="#f0f4f8").pack(pady=(10, 0))
history_listbox = tk.Listbox(root, width=70, height=8, font=("Consolas", 10))
history_listbox.pack()

error_label = tk.Label(root, text="", fg="red", font=("Arial", 11), bg="#f0f4f8")
error_label.pack()

def add_history(msg):
    history_listbox.insert(tk.END, f"[Floor {current_floor.get()}] {msg}")
    history_listbox.yview_moveto(1)


# ========== COMMAND PARSING + EXECUTION ==========
def execute_command():
    command = entry.get()
    result = parse_command_ai(command)
    entry.delete(0, tk.END)

    if delivery_status.get() == "Ready for delivery":
        delivery_status.set(f"Moving on Floor {current_floor.get()}")

    if result["action"] == "move":
        current_bot.move_bot(result["direction"], result["distance"])
        add_history(f"Moved {result['direction']} {result['distance']} units")
        error_label.config(text="")
    elif result["action"] == "diagonal":
        current_bot.move_bot_diagonal(result["direction"], result["distance"])
        add_history(f"Moved diagonally {result['direction']} {result['distance']} units")
        error_label.config(text="")
    elif result["action"] == "bezier":
        current_bot.move_bot_bezier(*result["coords"])
        add_history(f"Bezier curve navigation to {result['coords']}")
        error_label.config(text="")
    elif result["action"] == "reset":
        current_bot.reset_bot()
        delivery_status.set("Ready for delivery")
        add_history("Robot reset to center position")
        error_label.config(text="")
    elif result["action"] == "invalid":
        err = result.get("error", "Invalid command.")
        error_label.config(text=err)
        add_history(f"Error: {err}")

    update_floor_info()


# ========== KEYBOARD ARROW SHORTCUTS ==========
def on_key(event):
    keys = {"Up": "forward", "Down": "backward", "Left": "left", "Right": "right"}
    if event.keysym in keys:
        entry.delete(0, tk.END)
        entry.insert(0, keys[event.keysym])
        execute_command()

root.bind("<Up>", on_key)
root.bind("<Down>", on_key)
root.bind("<Left>", on_key)
root.bind("<Right>", on_key)


# ========== SAVE / LOAD STATE ==========
def save_state():
    floor_data[current_floor.get()] = {
        "x": current_bot.x,
        "y": current_bot.y,
        "path": current_bot.path.copy(),
        "color": current_bot.color
    }

    state = {
        "current_floor": current_floor.get(),
        "delivery_status": delivery_status.get(),
        "floor_data": floor_data
    }

    file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file:
        with open(file, "w") as f:
            json.dump(state, f)
        messagebox.showinfo("Save", "Robot state saved for all floors.")

def load_state():
    global floor_data
    file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file:
        with open(file, "r") as f:
            state = json.load(f)

        floor_data = state.get("floor_data", floor_data)
        delivery_status.set(state.get("delivery_status", "Ready for delivery"))
        saved_floor = state.get("current_floor", 1)
        change_floor(saved_floor)
        add_history("Robot state loaded.")


# ========== SAVE/LOAD BUTTONS ==========
file_frame = tk.Frame(root, bg="#f0f4f8")
file_frame.pack(pady=5)

tk.Button(file_frame, text="💾 Save State", font=("Arial", 11), command=save_state).pack(side=tk.LEFT, padx=5)
tk.Button(file_frame, text="📁 Load State", font=("Arial", 11), command=load_state).pack(side=tk.LEFT, padx=5)


# ========== INITIALIZE ==========
add_history("Delivery robot system initialized - Ready for operations")
update_floor_info()

# Launch window
root.mainloop()
