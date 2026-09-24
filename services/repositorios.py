"""Acceso a datos: una clase por tabla de Supabase.

`Repositorio` concentra el CRUD genérico y cada subclase solo indica su tabla,
su modelo y lo que tenga de particular (herencia). Las rutas de Flask nunca
hablan directo con Supabase: siempre pasan por un repositorio.
"""
import re

import httpx
from postgrest import APIError

from models import Cargo, Departamento, Trabajador
from utils.validadores import limpiar_rut


class ErrorDatos(Exception):
    """Error de base de datos traducido a un mensaje entendible."""

    NOMBRES_CAMPOS = {"rut": "RUT", "email": "correo", "nombre": "nombre"}

    @classmethod
    def desde_api(cls, error):
        codigo = error.code or ""
        if codigo == "23505":  # valor único repetido
            campo = re.search(r"Key \((\w+)\)", error.details or "")
            nombre = cls.NOMBRES_CAMPOS.get(campo.group(1), campo.group(1)) if campo else "dato"
            return cls(f"Ya existe un registro con ese {nombre}.")
        if codigo == "23503":  # clave foránea en uso
            return cls("No se puede eliminar: hay trabajadores asociados a este registro.")
        if codigo == "23514":  # restricción CHECK
            return cls("Algún dato no cumple las reglas de la base de datos.")
        if codigo == "42501":  # RLS / permisos
            return cls("No tienes permisos para realizar esta operación.")
        if codigo.startswith("PGRST3"):  # problemas con el token (JWT)
            return cls("Tu sesión expiró. Vuelve a iniciar sesión.")
        return cls("Ocurrió un error al comunicarse con la base de datos.")


class Repositorio:
    """CRUD genérico sobre una tabla de Supabase."""

    tabla = ""
    modelo = None
    columnas = "*"   # qué se trae al listar (puede incluir tablas relacionadas)
    orden = "id"

    def __init__(self, cliente):
        self._cliente = cliente

    def _tabla(self):
        return self._cliente.table(self.tabla)

    @staticmethod
    def _ejecutar(consulta):
        """Ejecuta la consulta y traduce cualquier error a ErrorDatos."""
        try:
            return consulta.execute()
        except APIError as error:
            raise ErrorDatos.desde_api(error) from error
        except httpx.HTTPError as error:
            raise ErrorDatos("No hay conexión con la base de datos.") from error

    def _a_modelos(self, filas):
        return [self.modelo.desde_dict(fila) for fila in filas]

    def listar(self):
        respuesta = self._ejecutar(self._tabla().select(self.columnas).order(self.orden))
        return self._a_modelos(respuesta.data)

    def obtener(self, id):
        respuesta = self._ejecutar(self._tabla().select(self.columnas).eq("id", id).limit(1))
        return self.modelo.desde_dict(respuesta.data[0]) if respuesta.data else None

    def crear(self, entidad):
        respuesta = self._ejecutar(self._tabla().insert(entidad.a_dict()))
        return self.modelo.desde_dict(respuesta.data[0])

    def actualizar(self, id, entidad):
        respuesta = self._ejecutar(self._tabla().update(entidad.a_dict()).eq("id", id))
        if not respuesta.data:
            raise ErrorDatos("El registro que intentas modificar ya no existe.")
        return self.modelo.desde_dict(respuesta.data[0])

    def eliminar(self, id):
        respuesta = self._ejecutar(self._tabla().delete().eq("id", id))
        if not respuesta.data:
            raise ErrorDatos("El registro que intentas eliminar ya no existe.")


class RepositorioDepartamentos(Repositorio):
    tabla = "departamentos"
    modelo = Departamento
    columnas = "*, trabajadores(count)"
    orden = "nombre"


class RepositorioCargos(Repositorio):
    tabla = "cargos"
    modelo = Cargo
    columnas = "*, trabajadores(count)"
    orden = "nombre"


class RepositorioTrabajadores(Repositorio):
    tabla = "trabajadores"
    modelo = Trabajador
    columnas = "*, departamento:departamentos(nombre), cargo:cargos(nombre)"
    orden = "apellidos"

    def buscar(self, texto="", departamento_id=None, estado=""):
        """Búsqueda por nombre, apellido, RUT o correo + filtros opcionales."""
        consulta = self._tabla().select(self.columnas)

        # Se quitan caracteres que tienen significado especial en los filtros de Supabase
        texto = re.sub(r"[,()*%\\\"']", "", texto or "").strip()
        if texto:
            condiciones = [f"{campo}.ilike.*{texto}*" for campo in ("nombres", "apellidos", "email")]
            rut = limpiar_rut(texto)
            if len(rut) >= 3 and rut[:-1].isdigit():
                condiciones.append(f"rut.ilike.*{rut[:-1]}*")
            consulta = consulta.or_(",".join(condiciones))
        if departamento_id:
            consulta = consulta.eq("departamento_id", departamento_id)
        if estado:
            consulta = consulta.eq("estado", estado)

        respuesta = self._ejecutar(consulta.order(self.orden))
        return self._a_modelos(respuesta.data)
