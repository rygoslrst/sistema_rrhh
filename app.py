"""TalentoRH — Control de trabajadores (Flask + Supabase).

Ejecutar con:  python app.py
"""
import os
from datetime import date
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from repositorio import ErrorSupabase, RepositorioTrabajadores, iniciar_sesion
from trabajador import Trabajador

load_dotenv()  # lee las variables del archivo .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Flask la necesita para guardar la sesión
repositorio = RepositorioTrabajadores()


# ---------- Funciones auxiliares ----------
def login_requerido(vista):
    """Decorador: si el usuario no ha iniciado sesión, lo manda al login."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "correo" not in session:
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura


@app.template_filter("pesos")
def formato_pesos(valor):
    """1250000 -> $1.250.000"""
    return "$" + f"{valor or 0:,}".replace(",", ".")


@app.template_filter("fecha")
def formato_fecha(valor):
    """date(2024, 3, 5) -> 05-03-2024"""
    return valor.strftime("%d-%m-%Y") if valor else ""


# ---------- Inicio de sesión ----------
@app.route("/")
def inicio():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "correo" in session:
        return redirect(url_for("dashboard"))

    correo = ""
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        if not correo or not password:
            flash("Ingresa tu correo y tu contraseña.", "error")
        else:
            try:
                iniciar_sesion(correo, password)
                session["correo"] = correo  # guardar el correo marca que la sesión está iniciada
                flash("¡Bienvenido/a!", "success")
                return redirect(url_for("dashboard"))
            except ErrorSupabase as error:
                flash(str(error), "error")

    return render_template("login.html", correo=correo)


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("login"))


# ---------- Dashboard ----------
@app.route("/dashboard")
@login_requerido
def dashboard():
    try:
        trabajadores = repositorio.listar()
    except ErrorSupabase as error:
        flash(str(error), "error")
        trabajadores = []

    vigentes = [t for t in trabajadores if t.estado != "desvinculado"]
    resumen = {
        "total": len(trabajadores),
        "activos": sum(1 for t in trabajadores if t.estado == "activo"),
        "ausentes": sum(1 for t in trabajadores if t.estado in ("vacaciones", "licencia")),
        "desvinculados": len(trabajadores) - len(vigentes),
        "sueldos": sum(t.sueldo for t in vigentes),
    }
    por_departamento = {d: sum(1 for t in vigentes if t.departamento == d)
                        for d in Trabajador.DEPARTAMENTOS}
    ultimos = sorted(trabajadores, key=lambda t: t.fecha_ingreso, reverse=True)[:5]

    return render_template("dashboard.html", resumen=resumen,
                           por_departamento=por_departamento, ultimos=ultimos)


# ---------- CRUD de trabajadores ----------
@app.route("/trabajadores")
@login_requerido
def lista_trabajadores():
    filtros = {
        "texto": request.args.get("texto", "").strip(),
        "departamento": request.args.get("departamento", ""),
        "estado": request.args.get("estado", ""),
    }
    try:
        trabajadores = repositorio.buscar(**filtros)
    except ErrorSupabase as error:
        flash(str(error), "error")
        trabajadores = []

    return render_template("trabajadores.html", trabajadores=trabajadores,
                           filtros=filtros, Trabajador=Trabajador)


def mostrar_formulario(trabajador):
    return render_template("formulario.html", trabajador=trabajador,
                           Trabajador=Trabajador, hoy=date.today().isoformat())


@app.route("/trabajadores/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo_trabajador():
    if request.method == "GET":
        return mostrar_formulario(Trabajador())

    trabajador = Trabajador.desde_dict(request.form)
    if not trabajador.validar():
        flash("Revisa los campos marcados en rojo.", "error")
        return mostrar_formulario(trabajador)
    try:
        repositorio.crear(trabajador)
    except ErrorSupabase as error:
        flash(str(error), "error")
        return mostrar_formulario(trabajador)

    flash(f"{trabajador.nombre_completo} fue registrado/a correctamente.", "success")
    return redirect(url_for("lista_trabajadores"))


@app.route("/trabajadores/<int:id>/editar", methods=["GET", "POST"])
@login_requerido
def editar_trabajador(id):
    if request.method == "GET":
        try:
            trabajador = repositorio.obtener(id)
        except ErrorSupabase as error:
            flash(str(error), "error")
            return redirect(url_for("lista_trabajadores"))
        if trabajador is None:
            flash("El trabajador que buscas no existe.", "error")
            return redirect(url_for("lista_trabajadores"))
        return mostrar_formulario(trabajador)

    trabajador = Trabajador.desde_dict(request.form)
    trabajador.id = id
    if not trabajador.validar():
        flash("Revisa los campos marcados en rojo.", "error")
        return mostrar_formulario(trabajador)
    try:
        repositorio.actualizar(id, trabajador)
    except ErrorSupabase as error:
        flash(str(error), "error")
        return mostrar_formulario(trabajador)

    flash("Los cambios se guardaron correctamente.", "success")
    return redirect(url_for("lista_trabajadores"))


@app.route("/trabajadores/<int:id>/eliminar", methods=["POST"])
@login_requerido
def eliminar_trabajador(id):
    try:
        repositorio.eliminar(id)
        flash("Trabajador eliminado.", "success")
    except ErrorSupabase as error:
        flash(str(error), "error")
    return redirect(url_for("lista_trabajadores"))


if __name__ == "__main__":
    app.run(debug=True)
