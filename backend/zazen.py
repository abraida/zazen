import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.api.routes import api_bp
from app.models.models import Project, Task, WebSite

app.register_blueprint(api_bp)


@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Project': Project, 'Task': Task, 'WebSite': WebSite, 'api_bp': api_bp}


