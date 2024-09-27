from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    json,
    jsonify,
)
from app import app
from app.forms import *
from app.models.models import Project, Task, Interval, TaskStatus, IntervalStatus
from app import db
from app.services import project_service, task_service, interval_service
from app.services.projectDTO import ProjectDTO


api_bp = Blueprint("api", __name__)


@api_bp.route("/")
@api_bp.route("/index")
def index():
    return redirect(url_for("api.projects"))  # Redirige a la lista de proyectos


@api_bp.route("/projects", methods=["GET", "POST"])
def projects():
    form = ProjectForm()
    eform = EditProjectForm()
    dform = DeleteProjectForm()

    if form.validate_on_submit():
        project_service.create_project(
            name=form.name.data,
            description=form.description.data,
            deadline=form.deadline.data,
        )

        flash("Project created successfully!", "success")
        return redirect(url_for("api.projects"))  # Redirige a la lista de proyectos

    existing_projects = project_service.get_all_projects()
    return render_template(
        "projects.html",
        form=form,
        edit_form=eform,
        delete_form=dform,
        projects=existing_projects,
    )


@api_bp.route("/projects/<int:project_id>/edit", methods=["POST"])
def edit_project(project_id):
    eform = EditProjectForm(id=project_id)

    if eform.validate_on_submit():
        project_service.update_project(
            project_id, name=eform.new_name.data, deadline=eform.deadline.data
        )
        return redirect(url_for("api.projects"))

    return redirect(url_for("api.projects"))


@api_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def delete_project(project_id):
    dform = DeleteProjectForm()

    if dform.validate_on_submit():
        project_service.delete_project(project_id)
        return redirect(url_for("api.projects"))

    return redirect(url_for("api.projects"))


@api_bp.route("/projects/<int:project_id>", methods=["GET", "POST"])
@api_bp.route("/projects/<int:project_id>/tasks", methods=["GET", "POST"])
def manage_tasks(project_id):
    form = TaskForm()
    eform = EditTaskForm()
    dform = DeleteTaskForm()
    iform = IntervalForm()

    if form.validate_on_submit():

        task_service.create_task(
            name=form.name.data,
            project_id=project_id,
        )

        flash("Task added successfully!", "success")
        return redirect(url_for("api.manage_tasks", project_id=project_id))

    project_dto = project_service.get_project(project_id)
    tasks = task_service.get_tasks_for_project(project_id)

    return render_template(
        "project_detail.html",
        form=form,
        edit_form=eform,
        delete_form=dform,
        interval_form=iform,
        project=project_dto,
        tasks=tasks,
    )


@api_bp.route("/projects/<int:project_id>/tasks/<int:task_id>", methods=["POST"])
def edit_task(project_id, task_id):
    eform = EditTaskForm()

    if eform.validate_on_submit():
        task_service.update_task(
            task_id,
            duration=eform.duration_minutes.data,
            status=TaskStatus[eform.status.data],
        )
        return redirect(url_for("api.manage_tasks", project_id=project_id))

    return redirect(url_for("api.manage_tasks", project_id=project_id))


@api_bp.route("/projects/<int:project_id>/tasks/<int:task_id>", methods=["POST"])
def delete_task(project_id, task_id):
    dform = DeleteTaskForm()

    if dform.validate_on_submit():
        task_service.delete_task(task_id)
        return redirect(url_for("api.manage_tasks", project_id=project_id))

    return redirect(url_for("api.manage_tasks", project_id=project_id))


@api_bp.route("/projects/<int:project_id>/interval", methods=["POST"])
def start_interval(project_id):
    form = IntervalForm()

    if form.validate_on_submit():
        websites = json.loads(form.websites_hidden.data)
        task_ids = json.loads(form.tasks_hidden.data)
        duration_minutes = form.duration.data

        interval = interval_service.create_interval(
            tasks=task_ids,
            websites=websites,
            duration=duration_minutes,
            project_id=project_id,
        )

        return redirect(
            url_for(
                "api.confirm_interval", project_id=project_id, interval_id=interval.id
            )
        )

    flash("Please correct the errors and try again.", "danger")
    return redirect(url_for("api.manage_tasks", project_id=project_id))


@api_bp.route(
    "/projects/<int:project_id>/interval/<int:interval_id>", methods=["GET", "POST"]
)
def confirm_interval(project_id, interval_id):

    interval = interval_service.get_interval_by_id(interval_id)
    project_dto = project_service.get_project(project_id)

    return render_template(
        "interval_confirm.html", interval=interval, project=project_dto
    )

@app.route('/update_interval_status', methods=['POST'])
def update_interval_status():
    interval_id = request.json.get('interval_id')
    new_status = request.json.get('status')

    # Lógica para buscar el intervalo y actualizar su estado
    interval = Interval.query.get(interval_id)
    if interval:
        interval.status = new_status
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Interval status updated'}), 200
    return jsonify({'status': 'error', 'message': 'Interval not found'}), 404

@app.route('/interval/<int:interval_id>/finish/', methods=['POST'])
def finish_interval(interval_id):
    data = request.get_json()

    if 'interval_id' in data and data['interval_id'] == interval_id:
        interval = interval_service.get_interval_by_id(interval_id)

        interval.status = IntervalStatus

        return jsonify({"message": "Intervalo finalizado correctamente", "interval_id": interval_id}), 200

    else:
        return jsonify({"error": "Datos inválidos"}), 400