"""Funciones de validación y conversión reutilizables por los modelos."""
import re
from datetime import date

PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
PATRON_NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$")
PATRON_TELEFONO = re.compile(r"^\+?[\d ]{8,15}$")


def limpiar_rut(rut):
    """Quita puntos, guion y espacios: ' 12.345.678-k ' -> '12345678K'."""
    return re.sub(r"[^0-9kK]", "", rut or "").upper()


def calcular_dv(cuerpo):
    """Dígito verificador de un RUT chileno (algoritmo módulo 11)."""
    suma, multiplicador = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    if resto == 11:
        return "0"
    if resto == 10:
        return "K"
    return str(resto)


def validar_rut(rut):
    limpio = limpiar_rut(rut)
    if len(limpio) < 8:
        return False
    cuerpo, dv = limpio[:-1], limpio[-1]
    return cuerpo.isdigit() and calcular_dv(cuerpo) == dv


def normalizar_rut(rut):
    """Formato en que se guarda en la base de datos: '12.345.678-k' -> '12345678-K'."""
    limpio = limpiar_rut(rut)
    return f"{limpio[:-1]}-{limpio[-1]}" if len(limpio) >= 2 else limpio


def formatear_rut(rut):
    """Formato para mostrar en pantalla: '12345678K' -> '12.345.678-K'."""
    limpio = limpiar_rut(rut)
    if len(limpio) < 2:
        return rut
    cuerpo, dv = limpio[:-1], limpio[-1]
    return f"{int(cuerpo):,}".replace(",", ".") + f"-{dv}"


def validar_email(email):
    return bool(PATRON_EMAIL.match(email or ""))


def validar_nombre(texto):
    return bool(PATRON_NOMBRE.match(texto or ""))


def validar_telefono(telefono):
    return bool(PATRON_TELEFONO.match(telefono or ""))


def a_entero(valor):
    """Convierte texto a entero; devuelve None si no es un número válido."""
    if valor is None or valor == "":
        return None
    try:
        return int(str(valor).replace(".", "").strip())
    except ValueError:
        return None


def a_fecha(valor):
    """Convierte 'AAAA-MM-DD' a date; devuelve None si no es válida."""
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor)[:10])
    except (TypeError, ValueError):
        return None


def texto(valor):
    """Normaliza un valor de formulario: None -> '' y sin espacios extremos."""
    return (valor or "").strip()
