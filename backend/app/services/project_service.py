from app.models.models import Project
from app import db
from .projectDTO import ProjectDTO
from .task_service import sql_task_service

class SQLAlchemyProjectService():
    def __init__(self, task_service):
        self.task_service = task_service

    def get_project(self, project_id):

        return self.domain_to_DTO(Project.query.get_or_404(project_id))
        
    def create_project(self, name, description=None, deadline=None):
        new_project = Project(name=name, description=description, deadline=deadline)
        db.session.add(new_project)
        db.session.commit()
        return new_project

    def get_all_projects(self):
        return [self.domain_to_DTO(p) for p in Project.query.all()]


    def update_project(self, project_id, name=None, description=None, deadline=None):
        project = Project.query.get(project_id)
        if project:
            if name:
                project.name = name
            if description:
                project.description = description
            if deadline:
                project.deadline = deadline
            db.session.commit()
        return project

    def delete_project(self, project_id):
        project = Project.query.get(project_id)
        if project:
            tasks = sql_task_service.get_tasks_for_project(project_id)
            for t in tasks:
                sql_task_service.delete_task(t.id)
                
            db.session.delete(project)
            db.session.commit()

    def is_name_unique(self, name):
        project = Project.query.filter_by(name=name.data).first()
        return project is None
    
    def domain_to_DTO(self, project):
        tasks = self.task_service.get_tasks_for_project(project.id)
        
        total_duration = self.task_service.calculate_total_expected_duration(project.id)
        task_count = len(tasks)
        return ProjectDTO(project, total_duration, task_count)



sql_project_service = SQLAlchemyProjectService(sql_task_service)
