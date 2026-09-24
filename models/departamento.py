from models.entidad import Entidad
from utils.validadores import texto


class Departamento(Entidad):
    """Área de la empresa a la que pertenecen los trabajadores."""

    def __init__(self, nombre="", descripcion="", id=None, total_trabajadores=0):
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion
        self.total_trabajadores = total_trabajadores  # calculado, no se guarda

    def _reglas(self):
        if not self.nombre:
            self._agregar_error("nombre", "El nombre es obligatorio.")
        elif not 3 <= len(self.nombre) <= 80:
            self._agregar_error("nombre", "El nombre debe tener entre 3 y 80 caracteres.")
        if len(self.descripcion) > 255:
            self._agregar_error("descripcion", "La descripción no puede superar los 255 caracteres.")

    def a_dict(self):
        return {"nombre": self.nombre, "descripcion": self.descripcion or None}

    @classmethod
    def desde_dict(cls, datos):
        # Supabase devuelve el conteo embebido como [{"count": n}]
        conteo = datos.get("trabajadores") or [{}]
        return cls(
            id=datos.get("id"),
            nombre=texto(datos.get("nombre")),
            descripcion=texto(datos.get("descripcion")),
            total_trabajadores=conteo[0].get("count", 0),
        )
