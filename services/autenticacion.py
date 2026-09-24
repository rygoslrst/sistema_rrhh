import httpx
from supabase import AuthApiError, AuthError


class ErrorAutenticacion(Exception):
    """Error de inicio de sesión con un mensaje apto para mostrar al usuario."""


class ServicioAutenticacion:
    """Inicio de sesión y renovación de tokens usando Supabase Auth."""

    def __init__(self, conexion):
        self._conexion = conexion

    def iniciar_sesion(self, email, password):
        try:
            respuesta = self._conexion.cliente().auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except AuthApiError as error:
            if error.code == "email_not_confirmed":
                raise ErrorAutenticacion("Debes confirmar tu correo antes de ingresar.") from error
            if error.code == "invalid_credentials" or error.status == 400:
                raise ErrorAutenticacion("Correo o contraseña incorrectos.") from error
            raise ErrorAutenticacion("No fue posible iniciar sesión. Intenta nuevamente.") from error
        except (AuthError, httpx.HTTPError) as error:
            raise ErrorAutenticacion("No hay conexión con el servidor de autenticación.") from error
        return self._datos_sesion(respuesta)

    def refrescar(self, refresh_token):
        """Obtiene un token nuevo cuando el actual está por vencer."""
        try:
            respuesta = self._conexion.cliente().auth.refresh_session(refresh_token)
        except (AuthError, httpx.HTTPError) as error:
            raise ErrorAutenticacion("Tu sesión expiró. Vuelve a iniciar sesión.") from error
        return self._datos_sesion(respuesta)

    @staticmethod
    def _datos_sesion(respuesta):
        """Solo guardamos en la cookie de Flask lo estrictamente necesario."""
        sesion, usuario = respuesta.session, respuesta.user
        return {
            "access_token": sesion.access_token,
            "refresh_token": sesion.refresh_token,
            "expires_at": sesion.expires_at,
            "usuario": {"id": usuario.id, "email": usuario.email},
        }
