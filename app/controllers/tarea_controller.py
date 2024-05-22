from flask import Blueprint, request, jsonify
from models.tarea_model import Tarea
from views.tarea_view import render_tarea_list, render_tarea_detail
from utils.decorators import jwt_required, roles_required

# Crear un blueprint para el controlador de tareaes
tarea_bp = Blueprint("tarea", __name__)


# Ruta para obtener la lista de tareaes
@tarea_bp.route("/tareas", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_tareas():
    tareas = Tarea.get_all()
    return jsonify(render_tarea_list(tareas))


# Ruta para obtener un tarea específico por su ID
@tarea_bp.route("/tareas/<int:id>", methods=["GET"])
@jwt_required
@roles_required(roles=["admin", "user"])
def get_tarea(id):
    tarea = Tarea.get_by_id(id)
    if tarea:
        return jsonify(render_tarea_detail(tarea))
    return jsonify({"error": "Tarea no encontrado"}), 404


# Ruta para crear un nuevo tarea
@tarea_bp.route("/tareas", methods=["POST"])
@jwt_required
@roles_required(roles=["admin"])
def create_tarea():
    data = request.json
    name = data.get("name")
    species = data.get("species")
    age = data.get("age")

    # Validación simple de datos de entrada
    if not name or not species or age is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    # Crear un nuevo tarea y guardarlo en la base de datos
    tarea = Tarea(name=name, species=species, age=age)
    tarea.save()

    return jsonify(render_tarea_detail(tarea)), 201


# Ruta para actualizar un tarea existente
@tarea_bp.route("/tareas/<int:id>", methods=["PUT"])
@jwt_required
@roles_required(roles=["admin"])
def update_tarea(id):
    tarea = Tarea.get_by_id(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrado"}), 404

    data = request.json
    name = data.get("name")
    species = data.get("species")
    age = data.get("age")

    # Actualizar los datos del tarea
    tarea.update(name=name, species=species, age=age)

    return jsonify(render_tarea_detail(tarea))


# Ruta para eliminar un tarea existente
@tarea_bp.route("/tareas/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required(roles=["admin"])
def delete_tarea(id):
    tarea = Tarea.get_by_id(id)

    if not tarea:
        return jsonify({"error": "Tarea no encontrado"}), 404

    # Eliminar el tarea de la base de datos
    tarea.delete()

    # Respuesta vacía con código de estado 204 (sin contenido)
    return "", 204