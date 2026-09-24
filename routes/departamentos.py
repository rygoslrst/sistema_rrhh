from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from models import Departamento
from services.repositorios import ErrorDatos, RepositorioDepartamentos
from utils.seguridad import login_requerido, obtener_db

bp = Blueprint("departamentos", __name__, url_prefix="/departamentos")


@bp.route("/")
@login_requerido
def lista():
    try:
        departamentos = RepositorioDepartamentos(obtener_db()).listar()
    except ErrorDatos as error:
        flash(str(error), "error")
        departamentos = []
    return render_template("departamentos/lista.html", departamentos=departamentos)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo():
    departamento = Departamento()
    if request.method == "POST":
        departamento = Departamento.desde_formulario(request.form)
        if departamento.validar():
            try:
                RepositorioDepartamentos(obtener_db()).crear(departamento)
                flash(f"Departamento «{departamento.nombre}» creado.", "success")
                return redirect(url_for("departamentos.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")
    return render_template("departamentos/formulario.html", departamento=departamento)


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar(id):
    repositorio = RepositorioDepartamentos(obtener_db())
    departamento = repositorio.obtener(id)
    if departamento is None:
        abort(404)

    if request.method == "POST":
        departamento = Departamento.desde_formulario(request.form)
        departamento.id = id
        if departamento.validar():
            try:
                repositorio.actualizar(id, departamento)
                flash("Departamento actualizado.", "success")
                return redirect(url_for("departamentos.lista"))
            except ErrorDatos as error:
                flash(str(error), "error")
        else:
            flash("Revisa los campos marcados en rojo.", "error")
    return render_template("departamentos/formulario.html", departamento=departamento)


@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar(id):
    try:
        RepositorioDepartamentos(obtener_db()).eliminar(id)
        flash("Departamento eliminado.", "success")
    except ErrorDatos as error:
        flash(str(error), "error")
    return redirect(url_for("departamentos.lista"))
