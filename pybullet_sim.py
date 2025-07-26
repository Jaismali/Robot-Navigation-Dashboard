import pybullet as p
import pybullet_data
import time

# Connect to GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -10)

# Enable mouse & keyboard camera control
p.configureDebugVisualizer(p.COV_ENABLE_MOUSE_PICKING, 1)
p.configureDebugVisualizer(p.COV_ENABLE_KEYBOARD_SHORTCUTS, 1)
p.resetDebugVisualizerCamera(
    cameraDistance=15,
    cameraYaw=45,
    cameraPitch=-30,
    cameraTargetPosition=[0, 0, 8]
)

# Load ground (optional visual floor)
p.loadURDF("plane.urdf")

# Create 9 floor blocks (Lab 0 at top to Lab 8 at bottom)
floor_ids = []
floor_height = 2

for i, floor in enumerate(range(8, -1, -1)):  # Lab 8 → Lab 0 (bottom to top)
    z = i * floor_height
    floor_id = p.loadURDF("cube_small.urdf", basePosition=[0, 0, z])
    floor_ids.append(floor_id)

# Load robot as a URDF (any robot or cube)
robot_id = p.loadURDF("r2d2.urdf", basePosition=[2, 0, 0])

# Highlight marker for robot floor
marker_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.5, 0.5, 0.1],
    rgbaColor=[0, 0, 1, 1]
)
marker_id = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=-1,
    baseVisualShapeIndex=marker_visual,
    basePosition=[0, 0, 0]
)

# Move robot to a floor (Lab 0 = top = index 0)
def move_robot_to_floor(floor):
    if not (0 <= floor <= 8):
        print("❌ Invalid floor.")
        return
    visual_index = 8 - floor  # Reverse: Lab 0 = topmost
    z_pos = visual_index * floor_height + 1  # center of block
    p.resetBasePositionAndOrientation(robot_id, [2, 0, z_pos], [0, 0, 0, 1])
    p.resetBasePositionAndOrientation(marker_id, [0, 0, z_pos - 1], [0, 0, 0, 1])
    print(f"✅ Robot moved to Lab {floor}")

# Start at Lab 0
move_robot_to_floor(0)

# Accept user input for commands
print("\n🗣️ Type a command like 'go to lab 3' or 'exit'\n")

while True:
    command = input("Command: ").strip().lower()

    if "exit" in command:
        print("👋 Exiting simulation.")
        break

    if "lab" in command:
        try:
            floor = int(command.split("lab")[-1].strip())
            move_robot_to_floor(floor)
        except:
            print("⚠️ Could not parse lab number.")

    for _ in range(30):
        p.stepSimulation()
        time.sleep(1 / 240.0)

p.disconnect()