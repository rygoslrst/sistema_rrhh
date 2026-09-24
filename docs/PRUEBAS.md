# Plan de pruebas funcionales — TalentoRH

**Instrucciones:** ejecuten cada prueba con la aplicación conectada al proyecto **real** de Supabase. Completen "Resultado obtenido", marquen ✅ o ❌ y guarden una captura en `docs/evidencias/` con el ID de la prueba como nombre (ej.: `P05.png`). Si una prueba falla, anoten qué pasó, corríjanlo y vuelvan a probar: la rúbrica valora que se documenten también los errores y cómo se resolvieron.

Usuario de prueba: el que crearon en Supabase (Authentication → Users), con correo ficticio.

| ID | RF | Acción | Resultado esperado | Resultado obtenido | ✅/❌ | Responsable |
|---|---|---|---|---|---|---|
| P01 | RF03 | Abrir `/dashboard` sin haber iniciado sesión | Redirige al login y muestra "Debes iniciar sesión para continuar." | | | |
| P02 | RF01 | Enviar el login con los campos vacíos | JS marca ambos campos en rojo y SweetAlert muestra "Formulario incompleto" | | | |
| P03 | RF01 | Login con una contraseña incorrecta | Mensaje "Correo o contraseña incorrectos." | | | |
| P04 | RF01 | Login con credenciales correctas | Entra al dashboard y muestra el aviso "¡Bienvenido/a!" | | | |
| P05 | RF04 | Revisar los indicadores del dashboard | Los totales coinciden con los datos de Supabase (16 trabajadores de prueba, 15 vigentes) | | | |
| P06 | RF06 | Abrir *Trabajadores* | Se listan todos, con el RUT con puntos y el sueldo en formato `$1.250.000` | | | |
| P07 | RF09 | Buscar "rojas" | Aparece solo Camila Andrea Rojas Fuentes | | | |
| P08 | RF09 | Buscar por RUT "15482731" | Aparece la persona con RUT 15.482.731-5 | | | |
| P09 | RF09 | Filtrar por estado "Licencia médica" | Solo aparecen trabajadores con licencia | | | |
| P10 | RF09 | Buscar un texto que no existe ("zzzz") | Mensaje "No hay trabajadores que coincidan…" | | | |
| P11 | RF12 | Registrar un trabajador con el RUT `12.345.678-9` | Error "El RUT no es válido" (en el navegador y en el servidor) | | | |
| P12 | RF12 | Registrar con el correo "correo-malo" | Error de formato de correo | | | |
| P13 | RF12 | Registrar con una fecha de ingreso futura | Error "La fecha de ingreso no puede ser futura." | | | |
| P14 | RF11 | En el formulario, elegir el cargo "Analista" con el sueldo vacío | Se completa el sueldo con 1150000 | | | |
| P15 | RF05 | Registrar un trabajador con datos válidos | Aviso de éxito; aparece en el listado **y en la tabla de Supabase** | | | |
| P16 | RF12 | Registrar otro trabajador con el mismo RUT | Mensaje "Ya existe un registro con ese RUT." | | | |
| P17 | RF07 | Editar un trabajador y cambiar su estado a "Vacaciones" | Aviso de éxito; se ve la nueva etiqueta y el dashboard se actualiza | | | |
| P18 | RF08 | Eliminar un trabajador y presionar "Cancelar" en la confirmación | No se elimina | | | |
| P19 | RF08 | Eliminar un trabajador y confirmar | Desaparece del listado y de Supabase | | | |
| P20 | RF10 | Crear el departamento "Marketing" | Aparece en Departamentos con 0 trabajadores | | | |
| P21 | RF10 | Eliminar el departamento "Ventas" (tiene personal) | Mensaje "No se puede eliminar: hay trabajadores asociados…" | | | |
| P22 | RF12 | Crear un departamento con el nombre "Ca" | Error "entre 3 y 80 caracteres" | | | |
| P23 | RF11 | Crear, editar y eliminar un cargo sin trabajadores | Las tres operaciones funcionan con su mensaje | | | |
| P24 | RF02 | Cerrar sesión y luego volver a `/trabajadores` | Pide iniciar sesión otra vez | | | |
| P25 | — | Abrir `/trabajadores/99999/editar` | Página de error 404 con botón "Volver al inicio" | | | |
| P26 | — | Ver la app en un celular (o en modo responsive del navegador) | El menú se abre con el botón ☰ y no hay desplazamiento horizontal | | | |
| P27 | Seguridad | Abrir en el navegador `https://TU-PROYECTO.supabase.co/rest/v1/trabajadores?apikey=CLAVE_PUBLICA` (sin iniciar sesión) | Devuelve una lista vacía `[]` gracias a RLS | | | |
| P28 | Seguridad | Revisar el repositorio en GitHub | No existen `.env` ni `venv/`; `.env.example` no tiene claves | | | |
