"""Punto de entrada de TalentoRH (sistema de gestión de Recursos Humanos).

Ejecutar con:  python app.py
"""
from datetime import date

from flask import Flask, render_template, session

from config import Config
from routes import BLUEPRINTS
from services.conexion import ConexionSupabase
from services.repositorios import ErrorDatos
from utils.validadores import formatear_rut


def formato_clp(valor):
    """1250000 -> '$1.250.000'"""
    return "$" + f"{int(valor or 0):,}".replace(",", ".")


def formato_fecha(valor):
    """date(2024, 3, 5) -> '05-03-2024'"""
    return valor.strftime("%d-%m-%Y") if valor else "—"


def crear_app(config=Config):
    config.verificar()

    app = Flask(__name__)
    app.config.from_object(config)
    app.extensions["supabase"] = ConexionSupabase(config.SUPABASE_URL, config.SUPABASE_KEY)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    # Filtros para usar en las plantillas: {{ trabajador.sueldo | clp }}
    app.add_template_filter(formato_clp, "clp")
    app.add_template_filter(formato_fecha, "fecha")
    app.add_template_filter(formatear_rut, "rut")

    @app.context_processor
    def datos_globales():
        return {"usuario_actual": session.get("usuario"), "hoy": date.today()}

    @app.errorhandler(ErrorDatos)
    def error_datos(error):
        return render_template("error.html", codigo=503, titulo="Problema con la base de datos",
                               mensaje=str(error)), 503

    @app.errorhandler(404)
    def no_encontrado(error):
        return render_template("error.html", codigo=404, titulo="Página no encontrada",
                               mensaje="La página o el registro que buscas no existe."), 404

    @app.errorhandler(500)
    def error_interno(error):
        return render_template("error.html", codigo=500, titulo="Error interno",
                               mensaje="Algo salió mal. Intenta nuevamente en unos segundos."), 500

    return app


app = crear_app()

if __name__ == "__main__":
    app.run(debug=True)
