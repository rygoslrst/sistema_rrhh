# Guía para armar el informe

El informe se entrega aparte (Word o PDF). Esta guía indica **qué va en cada sección** y **de dónde sacar el contenido** para no partir de cero. Redáctenlo con sus palabras: cada integrante escribe la parte que le tocó según `PLANIFICACION.md`, sección 7.

| # | Sección | Qué incluir | Fuente |
|---|---|---|---|
| 1 | **Portada** | Nombre del proyecto (TalentoRH), contexto (Gestión de RR.HH.), asignatura, integrantes, curso 4º Medio H, docente y fecha. | — |
| 2 | **Introducción** | Propósito del trabajo y por qué eligieron RR.HH. (media página). | PLANIFICACION §1 |
| 3 | **Descripción del problema** | Organización ficticia, cómo trabajan hoy (planillas), problemas concretos, a quién afecta y por qué es importante resolverlo. | PLANIFICACION §1 |
| 4 | **Usuarios del sistema** | Tabla de usuarios y qué necesita cada uno. | PLANIFICACION §2 |
| 5 | **Requerimientos** | Tabla RF01–RF13 y los no funcionales. | PLANIFICACION §3 |
| 6 | **Propuesta de solución** | Cómo responde la app a cada problema de la sección 3 (idealmente, una tabla problema → solución). | PLANIFICACION §4 |
| 7 | **Diseño de base de datos** | Diagrama ER, tablas con campos y tipos, relaciones, RLS y **captura del Table Editor de Supabase**. | BASE_DE_DATOS.md |
| 8 | **Arquitectura** | Diagrama, rol de HTML, CSS, JS, Flask y Supabase, estructura de carpetas y cómo se aplicó la POO. | PLANIFICACION §5 y §6, README |
| 9 | **Funcionalidades desarrolladas** | Una subsección por funcionalidad (login, dashboard, CRUD, búsqueda, validaciones, alertas), con una captura y una breve explicación de cómo funciona por dentro. | App + capturas |
| 10 | **Pruebas realizadas** | Tabla de pruebas completa, **incluyendo casos de error**. | PRUEBAS.md |
| 11 | **Evidencias** | Capturas (ver la lista abajo). | `docs/evidencias/` |
| 12 | **Organización del equipo** | Quién hizo qué y enlaces a sus *pull requests* o commits. | PLANIFICACION §7 + GitHub |
| 13 | **Conclusiones** | Qué aprendieron, dificultades reales y cómo las resolvieron, y mejoras futuras (usar el backlog). **Enlace al repositorio GitHub.** | Equipo |

## Capturas que no pueden faltar

- [ ] Pantalla de login y error de credenciales.
- [ ] Dashboard completo.
- [ ] Listado de trabajadores con una búsqueda y un filtro aplicados.
- [ ] Formulario de registro con errores de validación (RUT inválido, campos vacíos).
- [ ] Alerta de éxito (SweetAlert2) al registrar.
- [ ] Confirmación de eliminación y mensaje de "no se puede eliminar" en departamentos.
- [ ] Formulario de edición.
- [ ] Supabase: Table Editor con las 3 tablas, Authentication → Users y las políticas RLS.
- [ ] GitHub: página del repositorio (sin `.env` ni `venv`), historial de commits y *pull requests* del equipo.
- [ ] Vista en celular.

## Consejos

- Pongan un título y una explicación de una línea bajo cada captura. No basta con pegar la imagen.
- En "Dificultades", cuenten problemas reales que tuvieron (instalar dependencias, configurar `.env`, errores de RLS, conflictos de Git…) y cómo los solucionaron.
- Revisen la ortografía y el uso de términos técnicos, porque la rúbrica también los evalúa.
