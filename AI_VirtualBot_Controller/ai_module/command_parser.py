

import re

def parse_command_ai(command):
    """
    Enhanced rule-based parser for bot commands.
    Supports:
    - 'forward', 'backward', 'left', 'right', 'reset'
    - Diagonal: 'forward-left', 'forward-right', 'backward-left', 'backward-right'
    - Custom distance: e.g. 'forward 100', 'left 30'
    - Bezier: 'bezier x1 y1 x2 y2 x3 y3'
    """
    cmd = command.strip().lower()
    # Reset command
    if cmd == "reset":
        return {"action": "reset"}
    # Diagonal movement
    diagonal = ["forward-left", "forward-right", "backward-left", "backward-right"]
    if cmd in diagonal:
        return {"action": "diagonal", "direction": cmd, "distance": 50}
    # Custom distance
    match = re.match(r"(forward|backward|left|right) (\d+)", cmd)
    if match:
        direction, distance = match.groups()
        return {"action": "move", "direction": direction, "distance": int(distance)}
    # Simple movement
    if cmd in ["forward", "backward", "left", "right"]:
        return {"action": "move", "direction": cmd, "distance": 50}
    # Bezier
    if cmd.startswith("bezier"):
        parts = cmd.split()
        if len(parts) == 7:
            try:
                _, x1, y1, x2, y2, x3, y3 = parts
                coords = list(map(float, [x1, y1, x2, y2, x3, y3]))
                return {"action": "bezier", "coords": coords}
            except ValueError:
                return {"action": "invalid", "error": "Invalid bezier coordinates."}
    return {"action": "invalid", "error": "Unknown command."}
