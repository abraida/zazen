from app.models.models import Task
from app import db
from app.models.models import TaskStatus


class SQLAlchemyTaskService:
    def get_tasks_for_project(self, project_id):
        return Task.query.filter_by(project_id=project_id).all()

    def create_task(
        self, name, project_id, duration=None, status=TaskStatus.NOT_COMPLETED
    ):
        if duration:
            duration = duration * 60
        new_task = Task(
            name=name, duration_seconds=duration, project_id=project_id, status=status
        )

        db.session.add(new_task)
        db.session.commit()
        return new_task

    def get_task_by_id(self, id):
        return Task.query.get(id)

    def update_task(self, task_id, name=None, duration=None, status=None):
        task = Task.query.get(task_id)
        if task:
            if name:
                task.name = name
            if duration:
                task.duration_seconds = duration * 60
            if status:
                task.status = status
            db.session.commit()
        return task

    def delete_task(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()

    def calculate_total_expected_duration(self, project_id):
        tasks = self.get_tasks_for_project(project_id)
        total_duration = sum(
            task.duration_seconds for task in tasks if task.duration_seconds != None
        )
        return total_duration


sql_task_service = SQLAlchemyTaskService()
