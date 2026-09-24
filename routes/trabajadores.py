from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from models import Trabajador
from services.repositorios import (
    ErrorDatos, RepositorioCargos, RepositorioDepartamentos, RepositorioTrabajadores,
)
from utils.seguridad import login_requerido, obtener_db
from utils.validadores import a_entero

bp = Blueprint("trabajadores", __name__, url_prefix="/trabajadores")


def _opciones_formulario():
    """Departamentos y cargos para llenar los <select> del formulario."""
    db = obtener_db()
    return {
        "departamentos": RepositorioDepartamentos(db).listar(),
        "cargos": RepositorioCargos(db).listar(),
        "estados": Trabajador.ESTADOS,
    }


@bp.route("/")
@login_requerido
def lista():
    filtros = {
        "q": request.args.get("q", "").strip(),
        "departamento": a_entero(request.args.get("departamento")),
        "estado": request.args.get("estado", ""),
    }
    db = obtener_db()
    try:
        trabajadores = RepositorioTrabajadores(db).buscar(
            filtros["q"], filtros["departamento"], filtros["estado"]
        )
        departamentos = RepositorioDepartamentos(db).listar()
    except ErrorDatos as error:
        flash(str(error), "error")
        trabajadores, departamentos = [], []

    return render_template(
        "trabajadores/lista.html",
        trabajadores=trabajadores,
        departamentos=departamentos,
        estados=Trabajador.ESTADOS,
        filtros=filtros,
        hay_filtros=any(filtros.values()),
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    trabajador = Trabajador()
    if request.method == "POST":
        trabajador = Trabajador.desde_formulario(request.form)
        if trabajador.validar():
            try:
                RepositorioTrabajadores(obtener_db()).crear(trabajador)
                flash(f"Trabajador {trabajador.nombre_completo} registrado correctamente.", "success")
                return redirect(url_for("trabajadores.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")

    return render_template("trabajadores/formulario.html", trabajador=trabajador,
                           **_opciones_formulario())


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    repositorio = RepositorioTrabajadores(obtener_db())
    trabajador = repositorio.obtener(id)
    if trabajador is None:
        abort(404)

    if request.method == "POST":
        trabajador = Trabajador.desde_formulario(request.form)
        trabajador.id = id
        if trabajador.validar():
            try:
                repositorio.actualizar(id, trabajador)
                flash("Datos del trabajador actualizados.", "success")
                return redirect(url_for("trabajadores.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")

    return render_template("trabajadores/formulario.html", trabajador=trabajador,
                           **_opciones_formulario())


@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    try:
        RepositorioTrabajadores(obtener_db()).eliminar(id)
        flash("Trabajador eliminado.", "success")
    except ErrorDatos as error:
        flash(str(error), "error")
    return redirect(url_for("trabajadores.lista"))
