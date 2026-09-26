"""Conexión con Supabase: inicio de sesión y tabla trabajadores."""
import os
import re

from dotenv import load_dotenv
from postgrest import APIError
from supabase import AuthApiError, create_client

from trabajador import Trabajador

load_dotenv()  # lee las variables del archivo .env
URL = os.getenv("SUPABASE_URL")
CLAVE = os.getenv("SUPABASE_KEY")

supabase = create_client(URL, CLAVE)


class ErrorSupabase(Exception):
    """Error con un mensaje que se le puede mostrar al usuario."""


def iniciar_sesion(correo, password):
    """Revisa el correo y la contraseña con Supabase Auth."""
    try:
        # Se usa un cliente aparte para que el login no afecte al cliente principal
        create_client(URL, CLAVE).auth.sign_in_with_password({"email": correo, "password": password})
    except AuthApiError:
        raise ErrorSupabase("Correo o contraseña incorrectos.")
    except Exception:
        raise ErrorSupabase("No se pudo conectar con Supabase.")


class RepositorioTrabajadores:
    """Operaciones sobre la tabla 'trabajadores': listar, buscar, crear, editar y eliminar."""

    def _tabla(self):
        return supabase.table("trabajadores")

    def _ejecutar(self, consulta):
        """Ejecuta la consulta y cambia los errores técnicos por mensajes claros."""
        try:
            return consulta.execute().data
        except APIError as error:
            if error.code == "23505":  # 23505 = valor repetido en una columna única
                campo = "correo" if "correo" in f"{error.message} {error.details}" else "RUT"
                raise ErrorSupabase(f"Ya existe un trabajador con ese {campo}.")
            raise ErrorSupabase("Ocurrió un error en la base de datos.")
        except Exception:
            raise ErrorSupabase("No se pudo conectar con Supabase.")

    def _a_trabajadores(self, filas):
        return [Trabajador.desde_dict(fila) for fila in filas]

    def listar(self):
        return self._a_trabajadores(self._ejecutar(self._tabla().select("*").order("apellido")))

    def buscar(self, texto="", departamento="", estado=""):
        consulta = self._tabla().select("*")

        # Se quitan caracteres que Supabase usa en sus filtros (comas, paréntesis, etc.)
        texto = re.sub(r"[,()*%\\\"']", "", texto).strip()
        if texto:
            sin_puntos = texto.replace(".", "")  # el RUT se guarda sin puntos
            consulta = consulta.or_(
                f"nombre.ilike.*{texto}*,apellido.ilike.*{texto}*,rut.ilike.*{sin_puntos}*"
            )
        if departamento:
            consulta = consulta.eq("departamento", departamento)
        if estado:
            consulta = consulta.eq("estado", estado)

        return self._a_trabajadores(self._ejecutar(consulta.order("apellido")))

    def obtener(self, id):
        filas = self._ejecutar(self._tabla().select("*").eq("id", id))
        return Trabajador.desde_dict(filas[0]) if filas else None

    def crear(self, trabajador):
        self._ejecutar(self._tabla().insert(trabajador.a_dict()))

    def actualizar(self, id, trabajador):
        self._ejecutar(self._tabla().update(trabajador.a_dict()).eq("id", id))

    def eliminar(self, id):
        self._ejecutar(self._tabla().delete().eq("id", id))
