"""Configuración de la aplicación.

Todas las claves se leen desde variables de entorno (archivo .env), así nunca
quedan escritas en el código ni se suben a GitHub.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # Cookies de sesión más seguras: no accesibles desde JavaScript y no se
    # envían en peticiones POST desde otros sitios (protege contra CSRF básico).
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

    VARIABLES_OBLIGATORIAS = ("SECRET_KEY", "SUPABASE_URL", "SUPABASE_KEY")

    @classmethod
    def verificar(cls):
        """Detiene la aplicación con un mensaje claro si falta alguna variable."""
        faltantes = [nombre for nombre in cls.VARIABLES_OBLIGATORIAS if not getattr(cls, nombre)]
        if faltantes:
            raise RuntimeError(
                "Faltan variables de entorno: " + ", ".join(faltantes)
                + ". Copia .env.example como .env y completa los valores."
            )
