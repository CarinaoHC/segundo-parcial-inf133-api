from database import db


# Define la clase `Tarea` que hereda de `db.Model`
# `Tarea` representa la tabla `tareas` en la base de datos
class Tarea(db.Model):
    __tablename__ = "tareas"

    # Define las columnas de la tabla `tareas`
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Inicializa la clase `Tarea`
    def __init__(self, title, species, age):
        self.title = title
        self.species = species
        self.age = age

    # Guarda un tarea en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Obtiene todos los tareaes de la base de datos
    @staticmethod
    def get_all():
        return Tarea.query.all()

    # Obtiene un tarea por su ID
    @staticmethod
    def get_by_id(id):
        return Tarea.query.get(id)

    # Actualiza un tarea en la base de datos
    def update(self, title=None, species=None, age=None):
        if title is not None:
            self.title = title
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age
        db.session.commit()

    # Elimina un tarea de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()