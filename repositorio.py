"""Conexión con Supabase: inicio de sesión y tablas trabajadores y solicitudes."""
import os
import re

from dotenv import load_dotenv
from postgrest import APIError
from supabase import AuthApiError, create_client

from solicitud import Solicitud
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


class Repositorio:
    """Clase base: lo que comparten todos los repositorios (la tabla y cómo ejecutar consultas)."""

    tabla = ""  # cada clase hija indica su tabla

    def _tabla(self):
        return supabase.table(self.tabla)

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


class RepositorioTrabajadores(Repositorio):
    """Operaciones sobre la tabla 'trabajadores': listar, buscar, crear, editar y eliminar."""

    tabla = "trabajadores"

    def _a_trabajadores(self, filas):
        return [Trabajador.desde_dict(fila) for fila in filas]

    def listar(self):
        return self._a_trabajadores(self._ejecutar(self._tabla().select("*").order("apellido")))

    @staticmethod
    def _limpiar_busqueda(texto):
        """Quita caracteres que Supabase usa en sus filtros (comas, paréntesis, etc.)."""
        return re.sub(r"[,()*%\\\"']", "", texto or "").strip()

    def buscar(self, texto="", departamento="", cargo="", estado=""):
        consulta = self._tabla().select("*")

        texto = self._limpiar_busqueda(texto)
        if texto:
            sin_puntos = texto.replace(".", "")  # el RUT se guarda sin puntos
            consulta = consulta.or_(
                                f"nombre.ilike.*{texto}*,apellido.ilike.*{texto}*,"
                f"correo.ilike.*{texto}*,rut.ilike.*{sin_puntos}*"
            )
        if departamento:
            consulta = consulta.eq("departamento", departamento)
        if estado:
            consulta = consulta.eq("estado", estado)
        if cargo:
            consulta = consulta.eq("cargo", cargo)

        return self._a_trabajadores(self._ejecutar(consulta.order("apellido")))

    def obtener(self, id):
        filas = self._ejecutar(self._tabla().select("*").eq("id", id))
        return Trabajador.desde_dict(filas[0]) if filas else None

    # ----- Directorio para empleados: solo datos de contacto -----
    # Se piden a Supabase únicamente estas columnas, así el sueldo, el RUT y
    # los demás datos ni siquiera llegan a la página de un empleado.
    COLUMNAS_CONTACTO = "id, nombre, apellido, correo, telefono"

    def directorio(self, texto=""):
        """Trabajadores vigentes con su nombre, correo y teléfono (búsqueda solo por nombre)."""
        consulta = self._tabla().select(self.COLUMNAS_CONTACTO).neq("estado", "desvinculado")
        texto = self._limpiar_busqueda(texto)
        if texto:
            consulta = consulta.or_(f"nombre.ilike.*{texto}*,apellido.ilike.*{texto}*")
        return self._a_trabajadores(self._ejecutar(consulta.order("apellido")))

    def obtener_contacto(self, id):
        """Datos de contacto de un trabajador vigente (para la ficha que ve un empleado)."""
        consulta = self._tabla().select(self.COLUMNAS_CONTACTO).eq("id", id).neq("estado", "desvinculado")
        filas = self._ejecutar(consulta)
        return Trabajador.desde_dict(filas[0]) if filas else None

    def obtener_por_correo(self, correo):
        """Busca al trabajador dueño de una cuenta (se usa al iniciar sesión)."""
        filas = self._ejecutar(self._tabla().select("*").eq("correo", correo.lower()))
        return Trabajador.desde_dict(filas[0]) if filas else None

    def crear(self, trabajador):
        self._ejecutar(self._tabla().insert(trabajador.a_dict()))

    def actualizar(self, id, trabajador):
        self._ejecutar(self._tabla().update(trabajador.a_dict()).eq("id", id))

    def eliminar(self, id):
        self._ejecutar(self._tabla().delete().eq("id", id))


class RepositorioSolicitudes(Repositorio):
    """Operaciones sobre la tabla 'solicitudes' (vacaciones, permisos y licencias)."""

    tabla = "solicitudes"
    # Además de la solicitud, trae el nombre del trabajador que la pidió
    columnas = "*, trabajador:trabajadores(nombre, apellido)"

    def _a_solicitudes(self, filas):
        return [Solicitud.desde_dict(fila) for fila in filas]

    def listar(self, estado=""):
        """Todas las solicitudes (o solo las de un estado), de la más nueva a la más antigua."""
        consulta = self._tabla().select(self.columnas)
        if estado:
            consulta = consulta.eq("estado", estado)
        return self._a_solicitudes(self._ejecutar(consulta.order("created_at", desc=True)))

    def de_trabajador(self, trabajador_id):
        """Solicitudes de un trabajador (para 'Mi panel')."""
        consulta = self._tabla().select(self.columnas).eq("trabajador_id", trabajador_id)
        return self._a_solicitudes(self._ejecutar(consulta.order("created_at", desc=True)))

    def crear(self, solicitud):
        self._ejecutar(self._tabla().insert(solicitud.a_dict()))

    def responder(self, id, estado):
        """Aprueba o rechaza una solicitud. Solo se pueden responder las pendientes."""
        filas = self._ejecutar(
            self._tabla().update({"estado": estado}).eq("id", id).eq("estado", "pendiente")
        )
        if not filas:
            raise ErrorSupabase("Esa solicitud ya fue respondida o no existe.")
