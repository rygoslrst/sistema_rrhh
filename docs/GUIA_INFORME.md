# Guía para armar el informe

El informe se entrega aparte (Word o PDF). Esta guía indica **qué va en cada sección** y **de dónde sacar el contenido** para no partir de cero. Redáctenlo con sus palabras: cada integrante escribe la parte que le tocó según `PLANIFICACION.md`, sección 10.

| # | Sección | Qué incluir | Fuente |
|---|---|---|---|
| 1 | **Portada** | Nombre del proyecto (TalentoRH), contexto (Gestión de RR.HH.), asignatura, integrantes, curso 4º Medio H, docente y fecha. | — |
| 2 | **Introducción** | Propósito del trabajo y por qué eligieron RR.HH. (media página). | PLANIFICACION §1 y §2 |
| 3 | **Descripción del problema** | Organización ficticia, cómo trabajan hoy (planillas), problemas concretos, a quién afecta y por qué es importante resolverlo. | PLANIFICACION §2 |
| 4 | **Usuarios del sistema** | Tabla de roles (Administrador, Asistente de RR.HH. y Empleado), qué necesita cada uno y cómo se crean sus cuentas. | PLANIFICACION §3 |
| 5 | **Requerimientos** | Tabla RF01–RF18, los no funcionales y el alcance (qué incluye y qué no). | PLANIFICACION §4 y §5 |
| 6 | **Propuesta de solución** | Cómo responde la app a cada problema de la sección 3 (idealmente, una tabla problema → solución) y las pantallas. | PLANIFICACION §2 y §7 |
| 7 | **Diseño de base de datos** | Tablas `trabajadores` y `solicitudes` con campos, tipos, reglas y su relación (1 a N); listas fijas y por qué se eligieron; **captura del Table Editor de Supabase**. | PLANIFICACION §6 y §8 |
| 8 | **Arquitectura** | Diagrama, rol de HTML, CSS, JS, Flask y Supabase, estructura de carpetas y cómo se aplicó la POO. | PLANIFICACION §9, README |
| 9 | **Funcionalidades desarrolladas** | Una subsección por funcionalidad (login, dashboard, CRUD, búsqueda, validaciones, alertas), con una captura y una breve explicación de cómo funciona por dentro. | App + capturas |
| 10 | **Pruebas realizadas** | Tabla de pruebas completa, **incluyendo casos de error**. | PRUEBAS.md |
| 11 | **Evidencias** | Capturas (ver la lista abajo). | `docs/evidencias/` |
| 12 | **Organización del equipo** | Quién hizo qué y enlaces a sus *pull requests* o commits. | PLANIFICACION §10 + GitHub |
| 13 | **Conclusiones** | Qué aprendieron, dificultades reales y cómo las resolvieron, y mejoras futuras (ver "No incluye" en PLANIFICACION §4). **Enlace al repositorio GitHub.** | Equipo |

## Capturas que no pueden faltar

- [ ] Pantalla de login y error de credenciales.
- [ ] Dashboard completo.
- [ ] Listado de trabajadores con una búsqueda y un filtro aplicados.
- [ ] Formulario de registro con errores de validación (RUT inválido, campos vacíos).
- [ ] Alerta de éxito (SweetAlert2) al registrar.
- [ ] Confirmación de eliminación con SweetAlert2.
- [ ] Formulario de edición.
- [ ] Ficha de un trabajador.
- [ ] Menú del administrador, del asistente y del empleado (entrar con cada cuenta).
- [ ] Formulario "Corregir datos del trabajador" del asistente, con los campos bloqueados.
- [ ] Mi panel de un empleado y el formulario de nueva solicitud (con un error de fechas).
- [ ] Directorio de trabajadores y ficha de contacto que ve un empleado (compararlos con los del administrador).
- [ ] Pantalla de Solicitudes con la confirmación de Aprobar y el resultado en Mi panel del empleado.
- [ ] Empleado intentando entrar a `/dashboard` (aviso "solo para el administrador").
- [ ] Supabase: Table Editor con las tablas `trabajadores` y `solicitudes`, y Authentication → Users con las cuentas de prueba.
- [ ] GitHub: página del repositorio (sin `.env` ni `venv`), historial de commits y *pull requests* del equipo.
- [ ] Vista en celular.

## Consejos

- Pongan un título y una explicación de una línea bajo cada captura. No basta con pegar la imagen.
- En "Dificultades", cuenten problemas reales que tuvieron (instalar dependencias, configurar `.env`, conectar con Supabase, conflictos de Git…) y cómo los solucionaron.
- Revisen la ortografía y el uso de términos técnicos, porque la rúbrica también los evalúa.
