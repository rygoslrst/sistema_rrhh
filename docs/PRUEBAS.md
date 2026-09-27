# Plan de pruebas funcionales — TalentoRH

**Cómo usarlo:** ejecuten cada prueba con la app conectada a Supabase. Anoten el resultado obtenido, marquen ✅ o ❌ y guarden una captura en `docs/evidencias/` con el ID como nombre (ej.: `P05.png`). Si algo falla, anoten qué pasó y cómo lo corrigieron: eso también suma en el informe.

> **Primera ejecución: 26-09-2026**, con Supabase real (proyecto `talentorh`) y el usuario de prueba `rrhh@losandes-demo.cl`.
> **27-09-2026:** se agregaron la fecha de ingreso automática, la ficha, los roles y las solicitudes. Las pruebas marcadas como *Pendiente* hay que (re)hacerlas con Supabase real.
> Cuentas de prueba: `rrhh@losandes-demo.cl` (administradora, Catalina Navarro), `sebastian.perez@losandes-demo.cl` (asistente de RR.HH.) y una cuenta de empleado, por ejemplo `matias.soto@losandes-demo.cl`.
> Falta completar la columna *Responsable* y sacar las capturas.

| ID | RF | Acción | Resultado esperado | Resultado obtenido | ✅/❌ | Responsable |
|---|---|---|---|---|---|---|
| P01 | RF03 | Abrir una página interna (`/trabajadores`) sin iniciar sesión | Redirige al login | Redirige a `/login` con el aviso "Debes iniciar sesión para continuar." | ✅ | |
| P02 | RF01 | Enviar el login con los campos vacíos | Aviso de campos obligatorios | Ambos campos en rojo ("Este campo es obligatorio.") y alerta "Faltan datos" | ✅ | |
| P03 | RF01 | Iniciar sesión con una contraseña incorrecta | Mensaje "Correo o contraseña incorrectos" | El login no deja entrar y muestra el error de credenciales | ✅ | |
| P04 | RF01, RF13 | Iniciar sesión como administradora (`rrhh@losandes-demo.cl`) | Entra al Dashboard con el aviso "¡Hola, Catalina!"; el menú muestra Dashboard, Trabajadores, Solicitudes y Mi panel | Pendiente: repetir (el 26-09 entró bien con el aviso anterior "¡Bienvenido/a!") | | |
| P05 | RF04 | Revisar el dashboard | Las tarjetas, el gráfico y los últimos ingresos coinciden con Supabase. Desde el 27-09 (Catalina pasó a activa): 12 registrados, 9 activos, 2 ausentes, 1 desvinculado, $14.640.000 y 3 solicitudes pendientes | Pendiente: repetir con los datos nuevos (el 26-09 coincidía todo con los datos de ese día) | | |
| P06 | RF06 | Abrir el listado de trabajadores | Se ven todos los trabajadores con sus datos | 12 resultados; RUT con puntos (15.482.731-5) y sueldo con formato ($2.950.000) | ✅ | |
| P07 | RF09 | Buscar por apellido | Solo aparecen los que coinciden | `rojas` → 1 resultado: Camila Rojas Fuentes | ✅ | |
| P08 | RF09 | Buscar por RUT | Aparece el trabajador de ese RUT | `15482731` → 1 resultado: Camila Rojas Fuentes | ✅ | |
| P09 | RF09 | Filtrar por departamento y por estado | Solo aparecen los que cumplen ambos filtros | Operaciones + Licencia → 1 resultado: Benjamín Reyes Tapia (los filtros se aplican solos) | ✅ | |
| P10 | RF09 | Buscar un texto que no existe | Mensaje "No se encontraron trabajadores" | `zzzz` → "No se encontraron trabajadores." | ✅ | |
| P11 | RF10 | Registrar con el RUT `12.345.678-9` | Error "El RUT no es válido" | Al salir del campo: "El RUT no es válido." | ✅ | |
| P12 | RF10 | Registrar con el correo `correo-malo` | Error de formato de correo | "El correo no tiene un formato válido." | ✅ | |
| P13 | RF10 | Editar un trabajador y ponerle una fecha de ingreso futura | Error "La fecha de ingreso no puede ser futura" | Pendiente: repetir (desde el 27-09 la fecha solo se puede cambiar al editar) | | |
| P14 | RF10 | Registrar con sueldo `0` o con letras | Error "Ingresa un sueldo válido" | Con sueldo 0: "Ingresa un sueldo válido." | ✅ | |
| P15 | RF05 | Registrar un trabajador con datos válidos | Mensaje de éxito; aparece en el listado y en Supabase **con la fecha de ingreso de hoy** (el campo no se puede cambiar) | Pendiente: repetir para comprobar la fecha de hoy. En la primera ejecución (26-09) Ana Prueba Ficticia se registró bien: 13 en el listado y en Supabase | | |
| P16 | RF10 | Registrar otro trabajador con el mismo RUT | Error "Ya existe un trabajador con ese RUT" | Con RUT 15.482.731-5: "Ya existe un trabajador con ese RUT."; el formulario conserva los datos | ✅ | |
| P17 | RF07 | Editar un trabajador y cambiar su estado | Mensaje de éxito; el cambio se ve en el listado y en el dashboard | Estado cambiado a Vacaciones: "Los cambios se guardaron correctamente."; dashboard: 8 activos, 4 ausentes | ✅ | |
| P18 | RF08 | Eliminar y presionar "Cancelar" | El trabajador no se elimina | Aparece "¿Eliminar trabajador?"; con Cancelar, Ana sigue en la lista | ✅ | |
| P19 | RF08 | Eliminar y confirmar | Desaparece del listado y de Supabase | "Trabajador eliminado."; vuelve a 12 en el listado y en Supabase | ✅ | |
| P20 | RF02 | Cerrar sesión y volver a `/trabajadores` | Pide iniciar sesión de nuevo | "Sesión cerrada."; al abrir `/trabajadores` pide iniciar sesión | ✅ | |
| P21 | — | Abrir la app en el celular (o en modo responsive) | Se ve ordenada y sin desplazamiento horizontal | Con 375 px de ancho: sin desplazamiento horizontal, menú en dos filas, formulario en una columna | ✅ | |
| P22 | Seguridad | Revisar el repositorio en GitHub | No hay `.env` ni `venv/`; `.env.example` no tiene claves | Solo están los archivos del proyecto; `.env`, `venv/` y `__pycache__/` no se subieron; `.env.example` tiene las variables vacías | ✅ | |
| P23 | RF12 | En el listado, hacer clic en el nombre de un trabajador (o en el ícono del ojo) | Se abre su ficha con nombre, cargo, departamento, estado, RUT, correo, teléfono, fecha de ingreso, antigüedad y sueldo; los botones Editar y Eliminar funcionan | Pendiente: probar con Supabase | | |
| P24 | RF13 | Iniciar sesión con una cuenta de empleado (ej.: `matias.soto@losandes-demo.cl`) | Entra a "Mi panel" con el aviso "¡Hola, Matías!"; el menú muestra Trabajadores y Mi panel | Pendiente | | |
| P25 | RF13 | Como empleado, escribir en la barra de direcciones `/dashboard`, `/solicitudes` y `/trabajadores/nuevo` | Vuelve a "Mi panel" con el aviso "Esa sección es solo para el personal de RR.HH." | Pendiente | | |
| P26 | RF13 | Crear en Supabase una cuenta para `paula.espinoza@losandes-demo.cl` (desvinculada) e intentar entrar | "Tu cuenta está desactivada porque ya no trabajas en la empresa." | Pendiente | | |
| P27 | RF15 | Como empleado, revisar "Mi panel" | Se ven sus datos y la tabla "Mis solicitudes" con el estado de cada una | Pendiente | | |
| P28 | RF14 | Como empleado, crear una solicitud sin elegir tipo ni fechas | Errores "Selecciona el tipo de solicitud." y "Este campo es obligatorio." | Pendiente | | |
| P29 | RF14 | Como empleado, pedir una solicitud con "Hasta" anterior a "Desde" | "La fecha de término no puede ser anterior a la de inicio." | Pendiente | | |
| P30 | RF14 | Como empleado, pedir vacaciones con datos válidos | "Solicitud enviada…"; aparece en "Mis solicitudes" como Pendiente y en Supabase (tabla `solicitudes`) | Pendiente | | |
| P31 | RF16 | Como administradora, abrir Solicitudes | La pestaña Pendientes muestra la solicitud recién creada, con botones Aprobar y Rechazar; el dashboard cuenta las pendientes | Pendiente | | |
| P32 | RF16 | Aprobar una solicitud (confirmando en la alerta) | "Solicitud aprobada."; pasa a la pestaña Aprobadas y el empleado la ve como Aprobada | Pendiente | | |
| P33 | RF16 | Rechazar otra solicitud (confirmando en la alerta) | "Solicitud rechazada."; pasa a la pestaña Rechazadas | Pendiente | | |
| P34 | — | Como administradora, intentar eliminar su propio registro (Catalina Navarro) | "No puedes eliminar tu propio registro." y el registro no se borra | Pendiente | | |
| P35 | RF13 | Iniciar sesión como asistente (`sebastian.perez@losandes-demo.cl`) | Llega al Dashboard; el menú muestra Dashboard, Trabajadores, Solicitudes y Mi panel; no aparece el botón "Nuevo trabajador" | Pendiente | | |
| P36 | RF17 | Como asistente, abrir el listado y una ficha | Se ven todos los datos (incluido el sueldo); hay botón "Corregir datos" pero no "Eliminar" | Pendiente | | |
| P37 | RF17 | Como asistente, corregir el teléfono de un trabajador | Solo nombre, apellido, correo y teléfono se pueden editar; RUT, sueldo, cargo, departamento, estado, rol y fecha aparecen bloqueados con candado; se guarda el cambio | Pendiente | | |
| P38 | RF16, RF17 | Como asistente, abrir Solicitudes y escribir `/trabajadores/nuevo` en la barra de direcciones | Ve las solicitudes sin botones Aprobar/Rechazar; en `/trabajadores/nuevo` vuelve al Dashboard con "Esa acción es solo para el administrador." | Pendiente | | |
| P39 | RF18 | Como empleado, abrir "Trabajadores" y buscar `rojas` | Directorio con solo nombre, correo y teléfono (sin RUT, sueldo, cargo ni estado, y sin desvinculados); la búsqueda encuentra a Camila Rojas; buscar un RUT no encuentra nada | Pendiente | | |
| P40 | RF18 | Como empleado, abrir la ficha de un compañero | Página "Contacto" con solo nombre, correo y teléfono; sin botones Editar ni Eliminar | Pendiente | | |
