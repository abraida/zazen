class ProjectDTO:
    def __init__(self, project, total_duration, task_count):
        self.project = project  # Domain model
        self.name = project.name
        self.id = project.id
        self.description = project.description
        self.total_duration = total_duration  # Related value
        self.task_count = task_count  # Related value
        self.deadline = project.deadline
