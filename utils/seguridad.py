"""Sesión del usuario y protección de rutas."""
import time
from functools import wraps

from flask import current_app, flash, g, redirect, request, session, url_for

from services.autenticacion import ErrorAutenticacion, ServicioAutenticacion

MARGEN_REFRESCO = 60  # segundos antes del vencimiento en que se renueva el token


def conexion():
    return current_app.extensions["supabase"]


def servicio_autenticacion():
    return ServicioAutenticacion(conexion())


def guardar_sesion(datos):
    session.clear()
    session.permanent = True
    session.update(datos)


def obtener_db():
    """Cliente de Supabase con el token del usuario (uno por petición)."""
    if "db" not in g:
        g.db = conexion().cliente(session.get("access_token"))
    return g.db


def login_requerido(vista):
    """Decorador: si no hay sesión, redirige al login. Si el token está por
    vencer, lo renueva automáticamente."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("auth.login", siguiente=request.path))

        if session.get("expires_at", 0) - MARGEN_REFRESCO < time.time():
            try:
                guardar_sesion(servicio_autenticacion().refrescar(session.get("refresh_token")))
            except ErrorAutenticacion as error:
                session.clear()
                flash(str(error), "warning")
                return redirect(url_for("auth.login"))

        return vista(*args, **kwargs)
    return envoltura
