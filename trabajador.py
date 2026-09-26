"""Clase Trabajador: guarda los datos de un trabajador y los valida."""
import re
from datetime import date


class Trabajador:
    # Listas fijas: se usan en el formulario, en los filtros y en la validación
    DEPARTAMENTOS = ["Administración", "Operaciones", "Ventas", "Tecnología", "Recursos Humanos"]
    CARGOS = ["Gerente", "Jefe de área", "Analista", "Asistente administrativo",
              "Ejecutivo de ventas", "Operario", "Técnico de soporte"]
    ESTADOS = {
        "activo": "Activo",
        "vacaciones": "Vacaciones",
        "licencia": "Licencia",
        "desvinculado": "Desvinculado",
    }

    def __init__(self, rut="", nombre="", apellido="", correo="", telefono="",
                 departamento="", cargo="", fecha_ingreso=None, sueldo=None,
                 estado="activo", id=None):
        self.id = id
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.departamento = departamento
        self.cargo = cargo
        self.fecha_ingreso = fecha_ingreso  # objeto date
        self.sueldo = sueldo                # número entero (pesos)
        self.estado = estado
        self.errores = {}                   # campo -> mensaje de error

    # ---------- Crear un Trabajador a partir de datos ----------
    @classmethod
    def desde_dict(cls, datos):
        """Sirve tanto para una fila de Supabase como para un formulario (request.form)."""
        return cls(
            id=datos.get("id"),
            rut=cls._texto(datos.get("rut")),
            nombre=cls._texto(datos.get("nombre")),
            apellido=cls._texto(datos.get("apellido")),
            correo=cls._texto(datos.get("correo")).lower(),
            telefono=cls._texto(datos.get("telefono")),
            departamento=cls._texto(datos.get("departamento")),
            cargo=cls._texto(datos.get("cargo")),
            fecha_ingreso=cls._a_fecha(datos.get("fecha_ingreso")),
            sueldo=cls._a_entero(datos.get("sueldo")),
            estado=cls._texto(datos.get("estado")) or "activo",
        )

    def a_dict(self):
        """Datos que se guardan en la tabla de Supabase."""
        return {
            "rut": self.rut_normalizado(self.rut),
            "nombre": self.nombre,
            "apellido": self.apellido,
            "correo": self.correo,
            "telefono": self.telefono or None,
            "departamento": self.departamento,
            "cargo": self.cargo,
            "fecha_ingreso": self.fecha_ingreso.isoformat(),
            "sueldo": self.sueldo,
            "estado": self.estado,
        }

    # ---------- Propiedades calculadas ----------
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @property
    def iniciales(self):
        return (self.nombre[:1] + self.apellido[:1]).upper()

    @property
    def estado_texto(self):
        return self.ESTADOS.get(self.estado, self.estado)

    @property
    def rut_formateado(self):
        """'12345678-5' -> '12.345.678-5'"""
        limpio = self.limpiar_rut(self.rut)
        if len(limpio) < 2:
            return self.rut
        return f"{int(limpio[:-1]):,}".replace(",", ".") + "-" + limpio[-1]

    @property
    def antiguedad(self):
        """Años completos desde la fecha de ingreso."""
        if not self.fecha_ingreso:
            return 0
        hoy = date.today()
        anios = hoy.year - self.fecha_ingreso.year
        if (hoy.month, hoy.day) < (self.fecha_ingreso.month, self.fecha_ingreso.day):
            anios -= 1
        return max(anios, 0)

    # ---------- Validación ----------
    def validar(self):
        """Revisa todos los campos. Devuelve True si no hay errores."""
        self.errores = {}
        obligatorio = "Este campo es obligatorio."

        if not self.rut:
            self.errores["rut"] = obligatorio
        elif not self.rut_valido(self.rut):
            self.errores["rut"] = "El RUT no es válido."

        for campo in ("nombre", "apellido"):
            valor = getattr(self, campo)
            if not valor:
                self.errores[campo] = obligatorio
            elif not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' ]{2,60}", valor):
                self.errores[campo] = "Solo letras (2 a 60 caracteres)."

        if not self.correo:
            self.errores["correo"] = obligatorio
        elif not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", self.correo):
            self.errores["correo"] = "El correo no tiene un formato válido."

        if self.telefono and not re.fullmatch(r"\+?[\d ]{8,15}", self.telefono):
            self.errores["telefono"] = "El teléfono no es válido."

        if self.departamento not in self.DEPARTAMENTOS:
            self.errores["departamento"] = "Selecciona una opción válida."
        if self.cargo not in self.CARGOS:
            self.errores["cargo"] = "Selecciona una opción válida."
        if self.estado not in self.ESTADOS:
            self.errores["estado"] = "Selecciona una opción válida."

        if not self.fecha_ingreso:
            self.errores["fecha_ingreso"] = obligatorio
        elif self.fecha_ingreso > date.today():
            self.errores["fecha_ingreso"] = "La fecha de ingreso no puede ser futura."

        if self.sueldo is None or self.sueldo <= 0:
            self.errores["sueldo"] = "Ingresa un sueldo válido."

        return not self.errores

    # ---------- RUT chileno ----------
    @staticmethod
    def limpiar_rut(rut):
        """Deja solo números y K: '12.345.678-k' -> '12345678K'."""
        return re.sub(r"[^0-9kK]", "", rut or "").upper()

    @staticmethod
    def calcular_dv(numero):
        """Dígito verificador con el algoritmo módulo 11."""
        suma, multiplicador = 0, 2
        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        resto = 11 - (suma % 11)
        return {11: "0", 10: "K"}.get(resto, str(resto))

    @classmethod
    def rut_valido(cls, rut):
        limpio = cls.limpiar_rut(rut)
        numero, dv = limpio[:-1], limpio[-1:]
        return len(limpio) >= 8 and numero.isdigit() and cls.calcular_dv(numero) == dv

    @classmethod
    def rut_normalizado(cls, rut):
        """Formato en que se guarda: '12.345.678-k' -> '12345678-K'."""
        limpio = cls.limpiar_rut(rut)
        return f"{limpio[:-1]}-{limpio[-1]}"

    # ---------- Conversión de datos de texto ----------
    @staticmethod
    def _texto(valor):
        return str(valor or "").strip()

    @staticmethod
    def _a_entero(valor):
        try:
            return int(str(valor).replace(".", "").strip())
        except ValueError:
            return None

    @staticmethod
    def _a_fecha(valor):
        try:
            return date.fromisoformat(str(valor)[:10])
        except ValueError:
            return None
