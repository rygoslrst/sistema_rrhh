from datetime import date

from models.entidad import Entidad
from utils.validadores import (
    a_entero, a_fecha, normalizar_rut, texto,
    validar_email, validar_nombre, validar_rut, validar_telefono,
)


class Trabajador(Entidad):
    """Persona contratada por la empresa (siempre con datos ficticios)."""

    ESTADOS = {
        "activo": "Activo",
        "vacaciones": "Vacaciones",
        "licencia": "Licencia médica",
        "desvinculado": "Desvinculado",
    }

    def __init__(self, rut="", nombres="", apellidos="", email="", telefono="",
                 fecha_ingreso=None, sueldo=None, estado="activo",
                 departamento_id=None, cargo_id=None, id=None,
                 departamento_nombre="", cargo_nombre=""):
        super().__init__(id)
        self.rut = rut
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.telefono = telefono
        self.fecha_ingreso = fecha_ingreso
        self.sueldo = sueldo
        self.estado = estado
        self.departamento_id = departamento_id
        self.cargo_id = cargo_id
        # Datos de solo lectura que vienen de las tablas relacionadas
        self.departamento_nombre = departamento_nombre
        self.cargo_nombre = cargo_nombre

    # ----- Propiedades calculadas -----
    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    @property
    def iniciales(self):
        return (self.nombres[:1] + self.apellidos[:1]).upper()

    @property
    def estado_etiqueta(self):
        return self.ESTADOS.get(self.estado, self.estado)

    @property
    def esta_vigente(self):
        """Sigue formando parte de la empresa (aunque esté ausente)."""
        return self.estado != "desvinculado"

    @property
    def antiguedad_anios(self):
        if not self.fecha_ingreso:
            return 0
        hoy = date.today()
        anios = hoy.year - self.fecha_ingreso.year
        if (hoy.month, hoy.day) < (self.fecha_ingreso.month, self.fecha_ingreso.day):
            anios -= 1
        return max(anios, 0)

    # ----- Validación -----
    def _reglas(self):
        if not self.rut:
            self._agregar_error("rut", "El RUT es obligatorio.")
        elif not validar_rut(self.rut):
            self._agregar_error("rut", "El RUT no es válido (revisa el dígito verificador).")

        for campo, etiqueta in (("nombres", "Los nombres"), ("apellidos", "Los apellidos")):
            valor = getattr(self, campo)
            if not valor:
                self._agregar_error(campo, f"{etiqueta} son obligatorios.")
            elif not 2 <= len(valor) <= 60 or not validar_nombre(valor):
                self._agregar_error(campo, f"{etiqueta} solo pueden tener letras (2 a 60 caracteres).")

        if not self.email:
            self._agregar_error("email", "El correo es obligatorio.")
        elif not validar_email(self.email):
            self._agregar_error("email", "El correo no tiene un formato válido.")

        if self.telefono and not validar_telefono(self.telefono):
            self._agregar_error("telefono", "El teléfono debe tener entre 8 y 15 dígitos.")

        if not self.fecha_ingreso:
            self._agregar_error("fecha_ingreso", "Ingresa una fecha de ingreso válida.")
        elif self.fecha_ingreso > date.today():
            self._agregar_error("fecha_ingreso", "La fecha de ingreso no puede ser futura.")
        elif self.fecha_ingreso.year < 1950:
            self._agregar_error("fecha_ingreso", "La fecha de ingreso no es realista.")

        if self.sueldo is None:
            self._agregar_error("sueldo", "Ingresa un sueldo numérico.")
        elif not 1 <= self.sueldo <= 50_000_000:
            self._agregar_error("sueldo", "El sueldo debe estar entre $1 y $50.000.000.")

        if self.estado not in self.ESTADOS:
            self._agregar_error("estado", "Selecciona un estado válido.")
        if not self.departamento_id:
            self._agregar_error("departamento_id", "Selecciona un departamento.")
        if not self.cargo_id:
            self._agregar_error("cargo_id", "Selecciona un cargo.")

    # ----- Conversión -----
    def a_dict(self):
        return {
            "rut": normalizar_rut(self.rut),
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "email": self.email.lower(),
            "telefono": self.telefono or None,
            "fecha_ingreso": self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            "sueldo": self.sueldo,
            "estado": self.estado,
            "departamento_id": self.departamento_id,
            "cargo_id": self.cargo_id,
        }

    @classmethod
    def desde_dict(cls, datos):
        departamento = datos.get("departamento") or {}
        cargo = datos.get("cargo") or {}
        return cls(
            id=datos.get("id"),
            rut=texto(datos.get("rut")),
            nombres=texto(datos.get("nombres")),
            apellidos=texto(datos.get("apellidos")),
            email=texto(datos.get("email")),
            telefono=texto(datos.get("telefono")),
            fecha_ingreso=a_fecha(datos.get("fecha_ingreso")),
            sueldo=a_entero(datos.get("sueldo")),
            estado=texto(datos.get("estado")) or "activo",
            departamento_id=a_entero(datos.get("departamento_id")),
            cargo_id=a_entero(datos.get("cargo_id")),
            departamento_nombre=departamento.get("nombre", ""),
            cargo_nombre=cargo.get("nombre", ""),
        )
