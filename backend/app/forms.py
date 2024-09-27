from flask_wtf import FlaskForm
from flask import json
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    DateTimeField,
    SelectField,
    IntegerField,
    HiddenField,
    FormField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from app.services import project_service, task_service
import validators
from app.models.models import TaskStatus


class ProjectForm(FlaskForm):
    name = StringField("Project Name", validators=[DataRequired(), Length(max=64)])
    description = TextAreaField("Description", validators=[Length(max=512)])
    deadline = DateTimeField("Deadline", format="%Y-%m-%d")
    submit = SubmitField("Create Project")

    def validate_name(self, name):
        if not project_service.is_name_unique(name):

            raise ValidationError(
                "This project name already exists. Please choose a different name."
            )


class EditProjectForm(FlaskForm):
    new_name = StringField("Project Name", validators=[DataRequired(), Length(max=64)])
    submit = SubmitField("Edit Name")
    deadline = DateTimeField("Deadline", format="%Y-%m-%d")

    def __init__(self, id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_name = None
        if id:
            self.current_name = project_service.get_project(id).project.name

    def validate_new_name(self, new_name):

        if new_name.data != self.current_name:
            if not project_service.is_name_unique(new_name):
                raise ValidationError(
                    "This project name already exists. Please choose a different name."
                )


class DeleteProjectForm(FlaskForm):
    submit = SubmitField("Delete")


class TaskForm(FlaskForm):
    name = StringField("Título de la Tarea", validators=[DataRequired()])
    submit = SubmitField("Crear Tarea")


class EditTaskForm(FlaskForm):
    task_id = HiddenField("Task ID")
    duration_minutes = IntegerField(
        "Estimated time (minutes)", validators=[NumberRange(min=0)]
    )
    status = SelectField(
        "Status",
        choices=[(status.name, status.value) for status in TaskStatus],
        default=TaskStatus.NOT_COMPLETED.name,
    )

    submit = SubmitField("Edit")


class DeleteTaskForm(FlaskForm):
    task_id = HiddenField("Task ID")
    submit = SubmitField("Delete")


class IntervalForm(FlaskForm):
    websites_hidden = HiddenField("Websites", validators=[DataRequired()])

    duration = IntegerField(
        "Duration (in minutes)", validators=[DataRequired(), NumberRange(min=1)]
    )

    tasks_hidden = HiddenField("Tasks", validators=[DataRequired()])

    submit = SubmitField("Start Interval")

    # Validación personalizada para verificar que haya al menos una tarea seleccionada
    def validate_tasks_hidden(self, tasks):
        if len(tasks.data) < 1:
            raise ValidationError(
                "Please select at least one task."
            )  # Verificar que al menos haya una tarea seleccionada

    # Validación personalizada para verificar que haya al menos un sitio web bloqueado
    def validate_websites_hidden(self, websites):
        if len(websites.data) < 1:
            raise ValidationError(
                "Please add at least one website to block."
            )  # Verificar que al menos haya un sitio web bloqueado
