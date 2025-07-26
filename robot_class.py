from nlp_parser import parse_command

class Robot:
    def __init__(self):
        self.location = "Lab 0"
        self.battery = 100
        self.speed = 1.0
        self.status = "Idle"
        self.task_queue = []  # ✅ Unified task storage
        self.history = [self.location]

    def goto(self, location_name):
        self.location = location_name.strip()
        self.status = f"Moved to {location_name}"
        self.history.append(self.location)

    def add_task(self, task):
        self.task_queue.append(task)

    def run_auto_mode(self, callback=None):
        for task in self.task_queue.copy():
            intent, location = parse_command(task)
            if intent == "move" and location:
                self.goto(location)
                if callback:
                    callback(location)
        self.task_queue.clear()
