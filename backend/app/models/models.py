from datetime import datetime, timezone, timedelta
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from enum import Enum
from sqlalchemy import Enum as SQLAEnum


class Project(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    description: so.Mapped[Optional[str]] = so.mapped_column(sa.String(512))
    deadline: so.Mapped[Optional[datetime]] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )

    tasks: so.Mapped["Task"] = so.relationship(back_populates="parent_project")
    intervals: so.Mapped["Interval"] = so.relationship(back_populates="parent_project")

    def __repr__(self):
        return f"<Project {self.name} : {self.description}>"


class TaskStatus(Enum):
    NOT_COMPLETED = "Not Completed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    duration_seconds: so.Mapped[Optional[int]] = so.mapped_column(index=True)
    duration_worked_seconds: so.Mapped[Optional[int]] = so.mapped_column(
        index=True, default=0
    )
    status: so.Mapped[TaskStatus] = so.mapped_column(
        SQLAEnum(TaskStatus), index=True, default=TaskStatus.NOT_COMPLETED
    )
    project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id))
    parent_project: so.Mapped[Project] = so.relationship(back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.name} of parent with id {self.project_id}>"


class WebSite(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    url: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)

    def __repr__(self):
        return f"<Website: {self.url} allowed for task with id>"


class IntervalStatus(Enum):
    CREATED = 0
    INITIATED = 1
    FINISHED = 2


class Interval(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    task_ids: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    allowed_websites: so.Mapped[str] = so.mapped_column(sa.String(1024), index=True)
    duration_seconds: so.Mapped[Optional[int]] = so.mapped_column()

    project_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Project.id))
    parent_project: so.Mapped[Project] = so.relationship(back_populates="intervals")

    status: so.Mapped[IntervalStatus] = so.mapped_column(
        SQLAEnum(IntervalStatus), index=True, default=IntervalStatus.CREATED
    )

    start_time: so.Mapped[Optional[datetime]] = so.mapped_column(index=True)

    def __repr__(self):
        return f"<Interval of tasks.:{self.task_ids}>"
