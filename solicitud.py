"""Clase Solicitud: un pedido de vacaciones, permiso o licencia hecho por un trabajador."""
from datetime import date


class Solicitud:
    TIPOS = {
        "vacaciones": "Vacaciones",
        "permiso": "Permiso administrativo",
        "licencia": "Licencia médica",
    }
    ESTADOS = {
        "pendiente": "Pendiente",
        "aprobada": "Aprobada",
        "rechazada": "Rechazada",
    }

    def __init__(self, trabajador_id=None, tipo="", fecha_inicio=None, fecha_fin=None,
                 motivo="", estado="pendiente", id=None, fecha_solicitud=None,
                 trabajador_nombre=""):
        self.id = id
        self.trabajador_id = trabajador_id
        self.tipo = tipo
        self.fecha_inicio = fecha_inicio        # objeto date
        self.fecha_fin = fecha_fin              # objeto date
        self.motivo = motivo
        self.estado = estado
        self.fecha_solicitud = fecha_solicitud  # cuándo se pidió (la pone Supabase)
        self.trabajador_nombre = trabajador_nombre
        self.errores = {}

    # ---------- Crear una Solicitud a partir de datos ----------
    @classmethod
    def desde_dict(cls, datos):
        """Sirve para una fila de Supabase o para un formulario (request.form)."""
        trabajador = datos.get("trabajador") or {}  # datos del trabajador que vienen en la consulta
        return cls(
            id=datos.get("id"),
            trabajador_id=datos.get("trabajador_id"),
            tipo=str(datos.get("tipo") or "").strip(),
            fecha_inicio=cls._a_fecha(datos.get("fecha_inicio")),
            fecha_fin=cls._a_fecha(datos.get("fecha_fin")),
            motivo=str(datos.get("motivo") or "").strip(),
            estado=str(datos.get("estado") or "pendiente"),
            fecha_solicitud=cls._a_fecha(datos.get("created_at")),
            trabajador_nombre=f"{trabajador.get('nombre', '')} {trabajador.get('apellido', '')}".strip(),
        )

    def a_dict(self):
        """Datos que se guardan en la tabla de Supabase."""
        return {
            "trabajador_id": self.trabajador_id,
            "tipo": self.tipo,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "motivo": self.motivo or None,
            "estado": self.estado,
        }

    # ---------- Propiedades calculadas ----------
    @property
    def tipo_texto(self):
        return self.TIPOS.get(self.tipo, self.tipo)

    @property
    def estado_texto(self):
        return self.ESTADOS.get(self.estado, self.estado)

    @property
    def dias(self):
        """Cantidad de días pedidos, contando el primero y el último."""
        if not self.fecha_inicio or not self.fecha_fin:
            return 0
        return (self.fecha_fin - self.fecha_inicio).days + 1

    @property
    def esta_pendiente(self):
        return self.estado == "pendiente"

    # ---------- Validación ----------
    def validar(self):
        self.errores = {}
        if self.tipo not in self.TIPOS:
            self.errores["tipo"] = "Selecciona el tipo de solicitud."
        if not self.fecha_inicio:
            self.errores["fecha_inicio"] = "Este campo es obligatorio."
        if not self.fecha_fin:
            self.errores["fecha_fin"] = "Este campo es obligatorio."
        elif self.fecha_inicio and self.fecha_fin < self.fecha_inicio:
            self.errores["fecha_fin"] = "La fecha de término no puede ser anterior a la de inicio."
        if len(self.motivo) > 255:
            self.errores["motivo"] = "El motivo no puede superar los 255 caracteres."
        return not self.errores

    @staticmethod
    def _a_fecha(valor):
        try:
            return date.fromisoformat(str(valor)[:10])
        except ValueError:
            return None
