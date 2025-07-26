import difflib

def parse_command(text):
    text = text.lower().strip()

    allowed_commands = {
        "go to lab 0": "lab 0",
        "go to lab 1": "lab 1",
        "go to lab 2": "lab 2",
        "go to lab 3": "lab 3",
        "go to lab 4": "lab 4",
        "go to lab 5": "lab 5",
        "go to lab 6": "lab 6",
        "go to lab 7": "lab 7",
        "go to lab 8": "lab 8",
        "deliver to lab 0": "lab 0",
        "deliver to lab 1": "lab 1",
        "deliver to lab 2": "lab 2",
        "deliver to lab 3": "lab 3",
        "deliver to lab 4": "lab 4",
        "deliver to lab 5": "lab 5",
        "deliver to lab 6": "lab 6",
        "deliver to lab 7": "lab 7",
        "deliver to lab 8": "lab 8"
    }

    matches = difflib.get_close_matches(text, allowed_commands.keys(), n=1, cutoff=0.6)

    if matches:
        best_match = matches[0]
        return "move", allowed_commands[best_match]

    return "unknown", None