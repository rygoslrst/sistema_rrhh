from flask import Blueprint, flash, redirect, render_template, url_for

from services.estadisticas import ServicioEstadisticas
from services.repositorios import ErrorDatos, RepositorioDepartamentos, RepositorioTrabajadores
from utils.seguridad import login_requerido, obtener_db

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def raiz():
    return redirect(url_for("dashboard.inicio"))


@bp.route("/dashboard")
@login_requerido
def inicio():
    db = obtener_db()
    try:
        trabajadores = RepositorioTrabajadores(db).listar()
        departamentos = RepositorioDepartamentos(db).listar()
    except ErrorDatos as error:
        flash(str(error), "error")
        trabajadores, departamentos = [], []

    estadisticas = ServicioEstadisticas(trabajadores, departamentos)
    return render_template(
        "dashboard.html",
        resumen=estadisticas.resumen(),
        recientes=estadisticas.ingresos_recientes(),
        graficos=estadisticas.datos_graficos(),
    )
