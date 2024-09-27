from app.models.models import Interval, Task, IntervalStatus
from app import db
from .intervalDTO import IntervalDTO
from .task_service import sql_task_service

class SQLAlchemyIntervalService():


    def create_interval(self, tasks, websites, duration, project_id):
        
        duration = duration * 60
        self.clean_intervals()
        new_interval = Interval(task_ids = ','.join(tasks), allowed_websites = ','.join(websites), duration_seconds = duration, project_id=project_id)

        db.session.add(new_interval)
        db.session.commit()
        return new_interval

    def get_interval_by_id(self, id):
        return self.domain_to_DTO(Interval.query.get_or_404(id))
    
    def get_tasks_for_interval(self, project_id):
        return Task.query.filter_by(project_id=project_id).all()

    def domain_to_DTO(self, interval):
        tasks_ids = interval.task_ids.split(',')
        tasks = [sql_task_service.get_task_by_id(id) for id in tasks_ids]
        tasks = [t for t in tasks if t != None]

        websites = interval.allowed_websites.split(',')
        
        return IntervalDTO(interval.id, tasks, websites, interval.duration_seconds, interval.project_id, interval.status)
    
    def clean_intervals(self):    
        intervals = Interval.query.filter_by(status=IntervalStatus.CREATED).all()
        for i in intervals:
            db.session.delete(i)
        db.session.commit()
                
sql_interval_service = SQLAlchemyIntervalService()
