from collections import Counter

from models import Trabajador


class ServicioEstadisticas:
    """Calcula los indicadores del dashboard a partir de los trabajadores."""

    def __init__(self, trabajadores, departamentos):
        self._trabajadores = trabajadores
        self._departamentos = departamentos

    @property
    def _vigentes(self):
        return [t for t in self._trabajadores if t.esta_vigente]

    def resumen(self):
        por_estado = self.por_estado()
        vigentes = self._vigentes
        nomina = sum(t.sueldo or 0 for t in vigentes)
        return {
            "total": len(vigentes),
            "activos": por_estado["activo"],
            "ausentes": por_estado["vacaciones"] + por_estado["licencia"],
            "desvinculados": por_estado["desvinculado"],
            "nomina_mensual": nomina,
            "sueldo_promedio": round(nomina / len(vigentes)) if vigentes else 0,
            "departamentos": len(self._departamentos),
        }

    def por_estado(self):
        conteo = Counter(t.estado for t in self._trabajadores)
        return {estado: conteo.get(estado, 0) for estado in Trabajador.ESTADOS}

    def por_departamento(self):
        conteo = Counter(t.departamento_nombre for t in self._vigentes)
        return {d.nombre: conteo.get(d.nombre, 0) for d in self._departamentos}

    def ingresos_recientes(self, cantidad=5):
        con_fecha = [t for t in self._vigentes if t.fecha_ingreso]
        return sorted(con_fecha, key=lambda t: t.fecha_ingreso, reverse=True)[:cantidad]

    def datos_graficos(self):
        """Datos listos para Chart.js (se envían al HTML como JSON)."""
        por_departamento = self.por_departamento()
        por_estado = self.por_estado()
        return {
            "departamentos": {
                "etiquetas": list(por_departamento.keys()),
                "valores": list(por_departamento.values()),
            },
            "estados": {
                "etiquetas": [Trabajador.ESTADOS[e] for e in por_estado],
                "valores": list(por_estado.values()),
            },
        }
