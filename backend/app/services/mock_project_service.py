from app.models.models import Project
from app import db

mock_projects = [
    {"id": 1, "name": "Mock Project 1", "description": "Description 1", "deadline": "2024-10-01"},
    {"id": 2, "name": "Mock Project 2", "description": "Description 2", "deadline": "2024-11-01"},
]

class MockProjectService:
    def get_project_by_id(self, project_id):
        for project in mock_projects:
            if project['id'] == project_id:
                return project
        return None

    def get_all_projects(self):
        return mock_projects

    def create_project(self, name, description, deadline):
        new_project = {
            "id": len(mock_projects) + 1,
            "name": name,
            "description": description,
            "deadline": deadline
        }
        mock_projects.append(new_project)
        return new_project

    def delete_project(self, project_id):
        for project in mock_projects:
            if project['id'] == project_id:
                mock_projects.remove(project)

       

    def is_name_unique(self, name):
        for project in mock_projects:
            if project['name'] == name:
                return False
        return True
    
mock_project_service = MockProjectService()
