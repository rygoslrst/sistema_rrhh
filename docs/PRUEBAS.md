# Plan de pruebas funcionales — TalentoRH

**Cómo usarlo:** ejecuten cada prueba con la app conectada a Supabase. Anoten el resultado obtenido, marquen ✅ o ❌ y guarden una captura en `docs/evidencias/` con el ID como nombre (ej.: `P05.png`). Si algo falla, anoten qué pasó y cómo lo corrigieron: eso también suma en el informe.

| ID | RF | Acción | Resultado esperado | Resultado obtenido | ✅/❌ | Responsable |
|---|---|---|---|---|---|---|
| P01 | RF03 | Abrir `/dashboard` sin iniciar sesión | Redirige al login | | | |
| P02 | RF01 | Enviar el login con los campos vacíos | Aviso de campos obligatorios | | | |
| P03 | RF01 | Iniciar sesión con una contraseña incorrecta | Mensaje "Correo o contraseña incorrectos" | | | |
| P04 | RF01 | Iniciar sesión con datos correctos | Entra al dashboard con un mensaje de bienvenida | | | |
| P05 | RF04 | Revisar el dashboard | Las tarjetas, el gráfico y los últimos ingresos coinciden con los datos de Supabase | | | |
| P06 | RF06 | Abrir el listado de trabajadores | Se ven todos los trabajadores con sus datos | | | |
| P07 | RF09 | Buscar por apellido | Solo aparecen los que coinciden | | | |
| P08 | RF09 | Buscar por RUT | Aparece el trabajador de ese RUT | | | |
| P09 | RF09 | Filtrar por departamento y por estado | Solo aparecen los que cumplen ambos filtros | | | |
| P10 | RF09 | Buscar un texto que no existe | Mensaje "No se encontraron trabajadores" | | | |
| P11 | RF10 | Registrar con el RUT `12.345.678-9` | Error "El RUT no es válido" | | | |
| P12 | RF10 | Registrar con el correo `correo-malo` | Error de formato de correo | | | |
| P13 | RF10 | Registrar con una fecha de ingreso futura | Error "La fecha de ingreso no puede ser futura" | | | |
| P14 | RF10 | Registrar con sueldo `0` o con letras | Error "Ingresa un sueldo válido" | | | |
| P15 | RF05 | Registrar un trabajador con datos válidos | Mensaje de éxito; aparece en el listado y en Supabase | | | |
| P16 | RF10 | Registrar otro trabajador con el mismo RUT | Error "Ya existe un trabajador con ese RUT" | | | |
| P17 | RF07 | Editar un trabajador y cambiar su estado | Mensaje de éxito; el cambio se ve en el listado y en el dashboard | | | |
| P18 | RF08 | Eliminar y presionar "Cancelar" | El trabajador no se elimina | | | |
| P19 | RF08 | Eliminar y confirmar | Desaparece del listado y de Supabase | | | |
| P20 | RF02 | Cerrar sesión y volver a `/trabajadores` | Pide iniciar sesión de nuevo | | | |
| P21 | — | Abrir la app en el celular (o en modo responsive) | Se ve ordenada y sin desplazamiento horizontal | | | |
| P22 | Seguridad | Abrir `https://TU-PROYECTO.supabase.co/rest/v1/trabajadores?apikey=CLAVE_PUBLICA` sin sesión | Devuelve `[]` gracias a RLS | | | |
| P23 | Seguridad | Revisar el repositorio en GitHub | No hay `.env` ni `venv/`; `.env.example` no tiene claves | | | |
