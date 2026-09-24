from models.entidad import Entidad
from utils.validadores import a_entero, texto


class Cargo(Entidad):
    """Puesto de trabajo, con un sueldo base referencial."""

    def __init__(self, nombre="", descripcion="", sueldo_base=None, id=None, total_trabajadores=0):
        super().__init__(id)
        self.nombre = nombre
        self.descripcion = descripcion
        self.sueldo_base = sueldo_base
        self.total_trabajadores = total_trabajadores  # calculado, no se guarda

    def _reglas(self):
        if not self.nombre:
            self._agregar_error("nombre", "El nombre es obligatorio.")
        elif not 3 <= len(self.nombre) <= 80:
            self._agregar_error("nombre", "El nombre debe tener entre 3 y 80 caracteres.")
        if len(self.descripcion) > 255:
            self._agregar_error("descripcion", "La descripción no puede superar los 255 caracteres.")
        if self.sueldo_base is None:
            self._agregar_error("sueldo_base", "Ingresa un sueldo base numérico.")
        elif not 0 <= self.sueldo_base <= 50_000_000:
            self._agregar_error("sueldo_base", "El sueldo base debe estar entre $0 y $50.000.000.")

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion or None,
            "sueldo_base": self.sueldo_base,
        }

    @classmethod
    def desde_dict(cls, datos):
        conteo = datos.get("trabajadores") or [{}]
        return cls(
            id=datos.get("id"),
            nombre=texto(datos.get("nombre")),
            descripcion=texto(datos.get("descripcion")),
            sueldo_base=a_entero(datos.get("sueldo_base")),
            total_trabajadores=conteo[0].get("count", 0),
        )
