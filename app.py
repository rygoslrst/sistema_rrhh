"""TalentoRH — Control de trabajadores (Flask + Supabase).

Ejecutar con:  python app.py
"""
import os
from datetime import date
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for

from repositorio import ErrorSupabase, RepositorioSolicitudes, RepositorioTrabajadores, iniciar_sesion
from solicitud import Solicitud
from trabajador import Trabajador

load_dotenv()  # lee las variables del archivo .env

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Flask la necesita para guardar la sesión
repositorio = RepositorioTrabajadores()
solicitudes = RepositorioSolicitudes()

PERSONAL_RRHH = ("admin", "asistente")  # roles que pueden ver los datos de todos


# ---------- Funciones auxiliares ----------
def login_requerido(vista):
    """Decorador: si el usuario no ha iniciado sesión, lo manda al login."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "trabajador_id" not in session:
            session.clear()  # por si quedó una sesión antigua a medias
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)
    return envoltura


def solo_rrhh(vista):
    """Decorador: solo el personal de RR.HH. (administrador o asistente) puede entrar."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if session.get("rol") not in PERSONAL_RRHH:
            flash("Esa sección es solo para el personal de RR.HH.", "warning")
            return redirect(url_for("inicio"))
        return vista(*args, **kwargs)
    return envoltura


def solo_admin(vista):
    """Decorador: solo el administrador puede hacer esta acción."""
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if session.get("rol") != "admin":
            flash("Esa acción es solo para el administrador.", "warning")
            return redirect(url_for("inicio"))
        return vista(*args, **kwargs)
    return envoltura


@app.context_processor
def permisos():
    """Variables para que las plantillas muestren u oculten botones según el rol."""
    rol = session.get("rol")
    return {"ROLES": Trabajador.ROLES, "es_admin": rol == "admin", "es_rrhh": rol in PERSONAL_RRHH}


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
    """Cada rol parte en su propia pantalla."""
    if "trabajador_id" not in session:
        return redirect(url_for("login"))
    if session.get("rol") in PERSONAL_RRHH:
        return redirect(url_for("dashboard"))
    return redirect(url_for("mi_panel"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "trabajador_id" in session:
        return redirect(url_for("inicio"))

    correo = ""
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        if not correo or not password:
            flash("Ingresa tu correo y tu contraseña.", "error")
            return render_template("login.html", correo=correo)
        try:
            iniciar_sesion(correo, password)             # 1. Supabase revisa la contraseña
            trabajador = repositorio.obtener_por_correo(correo)  # 2. ¿Quién es y qué rol tiene?
        except ErrorSupabase as error:
            flash(str(error), "error")
            return render_template("login.html", correo=correo)

        if trabajador is None:
            flash("Tu cuenta no está asociada a ningún trabajador.", "error")
        elif trabajador.estado == "desvinculado":
            flash("Tu cuenta está desactivada porque ya no trabajas en la empresa.", "error")
        else:
            session["correo"] = correo
            session["rol"] = trabajador.rol
            session["trabajador_id"] = trabajador.id
            session["nombre"] = trabajador.nombre
            flash(f"¡Hola, {trabajador.nombre}!", "success")
            return redirect(url_for("inicio"))

    return render_template("login.html", correo=correo)


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("login"))


# ---------- Dashboard (administrador) ----------
@app.route("/dashboard")
@login_requerido
@solo_rrhh
def dashboard():
    try:
        trabajadores = repositorio.listar()
        pendientes = len(solicitudes.listar("pendiente"))
    except ErrorSupabase as error:
        flash(str(error), "error")
        trabajadores, pendientes = [], 0

    vigentes = [t for t in trabajadores if t.estado != "desvinculado"]
    resumen = {
        "total": len(trabajadores),
        "activos": sum(1 for t in trabajadores if t.estado == "activo"),
        "ausentes": sum(1 for t in trabajadores if t.estado in ("vacaciones", "licencia")),
        "desvinculados": len(trabajadores) - len(vigentes),
        "sueldos": sum(t.sueldo for t in vigentes),
        "pendientes": pendientes,
    }
    por_departamento = {d: sum(1 for t in vigentes if t.departamento == d)
                        for d in Trabajador.DEPARTAMENTOS}
    ultimos = sorted(trabajadores, key=lambda t: t.fecha_ingreso, reverse=True)[:5]

    return render_template("dashboard.html", resumen=resumen,
                           por_departamento=por_departamento, ultimos=ultimos)


# ---------- CRUD de trabajadores (administrador) ----------
@app.route("/trabajadores")
@login_requerido
def lista_trabajadores():
    # Un empleado ve un directorio de contacto (solo nombre, correo y teléfono)
    if session["rol"] not in PERSONAL_RRHH:
        texto = request.args.get("texto", "").strip()
        try:
            contactos = repositorio.directorio(texto)
        except ErrorSupabase as error:
            flash(str(error), "error")
            contactos = []
        return render_template("directorio.html", trabajadores=contactos, texto=texto)

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


@app.route("/trabajadores/<int:id>")
@login_requerido
def ficha_trabajador(id):
    """Ficha del trabajador: completa para RR.HH., solo datos de contacto para un empleado."""
    es_personal_rrhh = session["rol"] in PERSONAL_RRHH
    try:
        if es_personal_rrhh:
            trabajador = repositorio.obtener(id)
        else:
            trabajador = repositorio.obtener_contacto(id)
    except ErrorSupabase as error:
        flash(str(error), "error")
        return redirect(url_for("lista_trabajadores"))
    if trabajador is None:
        flash("El trabajador que buscas no existe.", "error")
        return redirect(url_for("lista_trabajadores"))
    return render_template("ficha.html" if es_personal_rrhh else "contacto.html", t=trabajador)


def mostrar_formulario(trabajador):
    return render_template("formulario.html", trabajador=trabajador,
                           Trabajador=Trabajador, hoy=date.today().isoformat())


@app.route("/trabajadores/nuevo", methods=["GET", "POST"])
@login_requerido
@solo_admin
def nuevo_trabajador():
    if request.method == "GET":
        return mostrar_formulario(Trabajador(fecha_ingreso=date.today()))

    trabajador = Trabajador.desde_dict(request.form)
    trabajador.fecha_ingreso = date.today()  # un trabajador nuevo ingresa el día en que se registra
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
@solo_rrhh
def editar_trabajador(id):
    try:
        guardado = repositorio.obtener(id)
    except ErrorSupabase as error:
        flash(str(error), "error")
        return redirect(url_for("lista_trabajadores"))
    if guardado is None:
        flash("El trabajador que buscas no existe.", "error")
        return redirect(url_for("lista_trabajadores"))

    if request.method == "GET":
        return mostrar_formulario(guardado)

    if session["rol"] == "admin":
        trabajador = Trabajador.desde_dict(request.form)
        trabajador.id = id
    else:
        # El asistente solo corrige los datos básicos: el resto se mantiene como estaba
        # guardado, aunque alguien modifique el formulario desde el navegador.
        trabajador = guardado
        corregido = Trabajador.desde_dict(request.form)
        for campo in Trabajador.DATOS_BASICOS:
            setattr(trabajador, campo, getattr(corregido, campo))

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
@solo_admin
def eliminar_trabajador(id):
    if id == session.get("trabajador_id"):
        flash("No puedes eliminar tu propio registro.", "error")
        return redirect(url_for("lista_trabajadores"))
    try:
        repositorio.eliminar(id)
        flash("Trabajador eliminado.", "success")
    except ErrorSupabase as error:
        flash(str(error), "error")
    return redirect(url_for("lista_trabajadores"))


# ---------- Solicitudes: el administrador las revisa ----------
@app.route("/solicitudes")
@login_requerido
@solo_rrhh
def lista_solicitudes():
    estado = request.args.get("estado", "pendiente")  # por defecto se muestran las pendientes
    if estado not in Solicitud.ESTADOS:
        estado = ""  # "" = todas
    try:
        lista = solicitudes.listar(estado)
    except ErrorSupabase as error:
        flash(str(error), "error")
        lista = []
    return render_template("solicitudes.html", solicitudes=lista, estado=estado, Solicitud=Solicitud)


@app.route("/solicitudes/<int:id>/responder", methods=["POST"])
@login_requerido
@solo_admin
def responder_solicitud(id):
    respuesta = request.form.get("estado")
    if respuesta not in ("aprobada", "rechazada"):
        flash("Respuesta no válida.", "error")
        return redirect(url_for("lista_solicitudes"))
    try:
        solicitudes.responder(id, respuesta)
        flash(f"Solicitud {respuesta}.", "success")
    except ErrorSupabase as error:
        flash(str(error), "error")
    return redirect(url_for("lista_solicitudes"))


# ---------- Mi panel: lo que ve cada empleado ----------
@app.route("/mi-panel")
@login_requerido
def mi_panel():
    try:
        trabajador = repositorio.obtener(session["trabajador_id"])
        mis_solicitudes = solicitudes.de_trabajador(session["trabajador_id"])
    except ErrorSupabase as error:
        flash(str(error), "error")
        return render_template("mi_panel.html", t=None, solicitudes=[])
    return render_template("mi_panel.html", t=trabajador, solicitudes=mis_solicitudes)


@app.route("/mi-panel/nueva-solicitud", methods=["GET", "POST"])
@login_requerido
def nueva_solicitud():
    if request.method == "GET":
        return render_template("solicitud_form.html", s=Solicitud(), Solicitud=Solicitud)

    solicitud = Solicitud.desde_dict(request.form)
    solicitud.trabajador_id = session["trabajador_id"]  # siempre a nombre de quien inició sesión
    solicitud.estado = "pendiente"                      # la respuesta la da el administrador
    if not solicitud.validar():
        flash("Revisa los campos marcados en rojo.", "error")
        return render_template("solicitud_form.html", s=solicitud, Solicitud=Solicitud)
    try:
        solicitudes.crear(solicitud)
    except ErrorSupabase as error:
        flash(str(error), "error")
        return render_template("solicitud_form.html", s=solicitud, Solicitud=Solicitud)

    flash("Solicitud enviada. Queda pendiente hasta que el administrador la responda.", "success")
    return redirect(url_for("mi_panel"))


if __name__ == "__main__":
    app.run(debug=True)
