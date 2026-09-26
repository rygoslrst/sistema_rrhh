# Plan de pruebas funcionales — TalentoRH

**Cómo usarlo:** ejecuten cada prueba con la app conectada a Supabase. Anoten el resultado obtenido, marquen ✅ o ❌ y guarden una captura en `docs/evidencias/` con el ID como nombre (ej.: `P05.png`). Si algo falla, anoten qué pasó y cómo lo corrigieron: eso también suma en el informe.

> **Primera ejecución: 26-09-2026**, con Supabase real (proyecto `talentorh`) y el usuario de prueba `rrhh@losandes-demo.cl`. Falta completar la columna *Responsable* y sacar las capturas.

| ID | RF | Acción | Resultado esperado | Resultado obtenido | ✅/❌ | Responsable |
|---|---|---|---|---|---|---|
| P01 | RF03 | Abrir una página interna (`/trabajadores`) sin iniciar sesión | Redirige al login | Redirige a `/login` con el aviso "Debes iniciar sesión para continuar." | ✅ | |
| P02 | RF01 | Enviar el login con los campos vacíos | Aviso de campos obligatorios | Ambos campos en rojo ("Este campo es obligatorio.") y alerta "Faltan datos" | ✅ | |
| P03 | RF01 | Iniciar sesión con una contraseña incorrecta | Mensaje "Correo o contraseña incorrectos" | El login no deja entrar y muestra el error de credenciales | ✅ | |
| P04 | RF01 | Iniciar sesión con datos correctos | Entra al dashboard con un mensaje de bienvenida | Entra al Dashboard con el aviso "¡Bienvenido/a!" | ✅ | |
| P05 | RF04 | Revisar el dashboard | Las tarjetas, el gráfico y los últimos ingresos coinciden con los datos de Supabase | 12 registrados, 8 activos, 3 ausentes, 1 desvinculado, $14.640.000; gráfico 3-3-1-2-2; primer ingreso: Martín Álvarez (02-03-2026) | ✅ | |
| P06 | RF06 | Abrir el listado de trabajadores | Se ven todos los trabajadores con sus datos | 12 resultados; RUT con puntos (15.482.731-5) y sueldo con formato ($2.950.000) | ✅ | |
| P07 | RF09 | Buscar por apellido | Solo aparecen los que coinciden | `rojas` → 1 resultado: Camila Rojas Fuentes | ✅ | |
| P08 | RF09 | Buscar por RUT | Aparece el trabajador de ese RUT | `15482731` → 1 resultado: Camila Rojas Fuentes | ✅ | |
| P09 | RF09 | Filtrar por departamento y por estado | Solo aparecen los que cumplen ambos filtros | Operaciones + Licencia → 1 resultado: Benjamín Reyes Tapia (los filtros se aplican solos) | ✅ | |
| P10 | RF09 | Buscar un texto que no existe | Mensaje "No se encontraron trabajadores" | `zzzz` → "No se encontraron trabajadores." | ✅ | |
| P11 | RF10 | Registrar con el RUT `12.345.678-9` | Error "El RUT no es válido" | Al salir del campo: "El RUT no es válido." | ✅ | |
| P12 | RF10 | Registrar con el correo `correo-malo` | Error de formato de correo | "El correo no tiene un formato válido." | ✅ | |
| P13 | RF10 | Registrar con una fecha de ingreso futura | Error "La fecha de ingreso no puede ser futura" | Con fecha 27-09-2026: "La fecha de ingreso no puede ser futura." | ✅ | |
| P14 | RF10 | Registrar con sueldo `0` o con letras | Error "Ingresa un sueldo válido" | Con sueldo 0: "Ingresa un sueldo válido." | ✅ | |
| P15 | RF05 | Registrar un trabajador con datos válidos | Mensaje de éxito; aparece en el listado y en Supabase | Ana Prueba Ficticia registrada con aviso de éxito; 13 en el listado y en Supabase; dashboard: 13 registrados, 9 activos, $15.740.000 | ✅ | |
| P16 | RF10 | Registrar otro trabajador con el mismo RUT | Error "Ya existe un trabajador con ese RUT" | Con RUT 15.482.731-5: "Ya existe un trabajador con ese RUT."; el formulario conserva los datos | ✅ | |
| P17 | RF07 | Editar un trabajador y cambiar su estado | Mensaje de éxito; el cambio se ve en el listado y en el dashboard | Estado cambiado a Vacaciones: "Los cambios se guardaron correctamente."; dashboard: 8 activos, 4 ausentes | ✅ | |
| P18 | RF08 | Eliminar y presionar "Cancelar" | El trabajador no se elimina | Aparece "¿Eliminar trabajador?"; con Cancelar, Ana sigue en la lista | ✅ | |
| P19 | RF08 | Eliminar y confirmar | Desaparece del listado y de Supabase | "Trabajador eliminado."; vuelve a 12 en el listado y en Supabase | ✅ | |
| P20 | RF02 | Cerrar sesión y volver a `/trabajadores` | Pide iniciar sesión de nuevo | "Sesión cerrada."; al abrir `/trabajadores` pide iniciar sesión | ✅ | |
| P21 | — | Abrir la app en el celular (o en modo responsive) | Se ve ordenada y sin desplazamiento horizontal | Con 375 px de ancho: sin desplazamiento horizontal, menú en dos filas, formulario en una columna | ✅ | |
| P22 | Seguridad | Revisar el repositorio en GitHub | No hay `.env` ni `venv/`; `.env.example` no tiene claves | Solo están los archivos del proyecto; `.env`, `venv/` y `__pycache__/` no se subieron; `.env.example` tiene las variables vacías | ✅ | |
