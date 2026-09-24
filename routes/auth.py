from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from services.autenticacion import ErrorAutenticacion
from utils.seguridad import guardar_sesion, servicio_autenticacion
from utils.validadores import texto, validar_email

bp = Blueprint("auth", __name__)


def _destino_seguro(destino):
    """Evita redirigir a otro sitio (solo rutas internas como /trabajadores)."""
    if destino and destino.startswith("/") and not destino.startswith("//"):
        return destino
    return url_for("dashboard.inicio")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("dashboard.inicio"))

    email = ""
    if request.method == "POST":
        email = texto(request.form.get("email")).lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Ingresa tu correo y tu contraseña.", "error")
        elif not validar_email(email):
            flash("El correo no tiene un formato válido.", "error")
        else:
            try:
                guardar_sesion(servicio_autenticacion().iniciar_sesion(email, password))
                flash("¡Bienvenido/a! Sesión iniciada correctamente.", "success")
                return redirect(_destino_seguro(request.args.get("siguiente")))
            except ErrorAutenticacion as error:
                flash(str(error), "error")

    return render_template("login.html", email=email)


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada. ¡Hasta pronto!", "success")
    return redirect(url_for("auth.login"))
