from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase base abstracta de todas las entidades del sistema.

    Define lo que toda entidad debe saber hacer (abstracción) y deja que cada
    subclase implemente sus propias reglas de validación (polimorfismo).
    """

    def __init__(self, id=None):
        self.id = id
        self._errores = {}  # campo -> mensaje (atributo protegido)

    # ----- Validación (patrón "método plantilla") -----
    def validar(self):
        """Limpia errores anteriores, aplica las reglas de la subclase y
        devuelve True si la entidad quedó sin errores."""
        self._errores = {}
        self._reglas()
        return not self._errores

    @abstractmethod
    def _reglas(self):
        """Cada subclase registra aquí sus errores con _agregar_error()."""

    def _agregar_error(self, campo, mensaje):
        self._errores.setdefault(campo, mensaje)

    @property
    def errores(self):
        return dict(self._errores)

    # ----- Conversión hacia/desde Supabase -----
    @abstractmethod
    def a_dict(self):
        """Datos que se guardan en la tabla (sin id ni campos calculados)."""

    @classmethod
    @abstractmethod
    def desde_dict(cls, datos):
        """Crea la entidad a partir de una fila devuelta por Supabase."""

    @classmethod
    def desde_formulario(cls, formulario):
        """Crea la entidad a partir de un formulario HTML (request.form).
        Por defecto es igual que desde_dict; las subclases pueden cambiarlo."""
        return cls.desde_dict(formulario)

    def __repr__(self):
        return f"<{type(self).__name__} id={self.id}>"
