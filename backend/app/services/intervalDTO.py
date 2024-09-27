class IntervalDTO:
    def __init__(self, id, tasks_list, websites_list, duration, project_id, status):
        self.tasks = tasks_list
        self.id = id
        self.websites = websites_list
        self.duration = duration
        self.project_id = project_id
        self.status = status
