import os
from app.config import Config

if Config.USE_MOCK_DATA:
    # Importar los servicios de mock data
    from .mock_project_service import mock_project_service as project_service
    from .task_service import mock_task_service as task_service
else:
    # Importar los servicios reales con SQLAlchemy
    from .project_service import sql_project_service as project_service
    from .task_service import sql_task_service as task_service
    from .interval_service import sql_interval_service as interval_service
