from supabase import Client, ClientOptions, create_client


class ConexionSupabase:
    """Crea clientes de Supabase a partir de la URL y la clave pública (anon).

    Cada petición usa un cliente nuevo con el token del usuario conectado. Así
    las políticas RLS de la base de datos saben quién está consultando y un
    usuario sin sesión no puede leer ni escribir nada.
    """

    def __init__(self, url, clave):
        self._url = url
        self._clave = clave

    def cliente(self, token_acceso=None) -> Client:
        # En un servidor no queremos que la librería guarde sesiones en memoria
        # ni refresque tokens por su cuenta: eso lo controla Flask.
        opciones = ClientOptions(auto_refresh_token=False, persist_session=False)
        if token_acceso:
            opciones.headers["Authorization"] = f"Bearer {token_acceso}"
        return create_client(self._url, self._clave, opciones)
