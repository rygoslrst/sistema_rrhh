from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from models import Cargo
from services.repositorios import ErrorDatos, RepositorioCargos
from utils.seguridad import login_requerido, obtener_db

bp = Blueprint("cargos", __name__, url_prefix="/cargos")


@bp.route("/")
@login_requerido
def lista():
    try:
        cargos = RepositorioCargos(obtener_db()).listar()
    except ErrorDatos as error:
        flash(str(error), "error")
        cargos = []
    return render_template("cargos/lista.html", cargos=cargos)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    cargo = Cargo()
    if request.method == "POST":
        cargo = Cargo.desde_formulario(request.form)
        if cargo.validar():
            try:
                RepositorioCargos(obtener_db()).crear(cargo)
                flash(f"Cargo «{cargo.nombre}» creado.", "success")
                return redirect(url_for("cargos.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")
    return render_template("cargos/formulario.html", cargo=cargo)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    repositorio = RepositorioCargos(obtener_db())
    cargo = repositorio.obtener(id)
    if cargo is None:
        abort(404)

    if request.method == "POST":
        cargo = Cargo.desde_formulario(request.form)
        cargo.id = id
        if cargo.validar():
            try:
                repositorio.actualizar(id, cargo)
                flash("Cargo actualizado.", "success")
                return redirect(url_for("cargos.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")
    return render_template("cargos/formulario.html", cargo=cargo)


@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    try:
        RepositorioCargos(obtener_db()).eliminar(id)
        flash("Cargo eliminado.", "success")
    except ErrorDatos as error:
        flash(str(error), "error")
    return redirect(url_for("cargos.lista"))
