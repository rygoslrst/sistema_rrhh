# Planificación — TalentoRH: control de trabajadores

> Evaluación II y III · Programación Orientada a Objeto · 4º Medio H
> Contexto: **B. Gestión de Recursos Humanos** · Entrega: **martes 29 de septiembre de 2026**
> Estado del plan: **aprobado el 25-09-2026** y **ampliado el 27-09-2026** con roles (Administrador / Asistente de RR.HH. / Empleado) y solicitudes de permisos.

---

## 1. Idea en una frase

Una aplicación web para que el área de RR.HH. **registre y controle a los trabajadores** de la empresa (quiénes son, en qué área y cargo están, desde cuándo, cuánto ganan y en qué estado se encuentran) y para que **cada trabajador pida sus permisos** y vea si se los aprobaron.

## 2. Problema

**Organización (ficticia):** *Comercial Los Andes SpA*, empresa de distribución con unas 60 personas.

**Situación actual:** los datos del personal están en planillas Excel que se copian y modifican por separado, y los permisos se piden por correo o de palabra. Esto provoca que:

- haya trabajadores duplicados o con datos desactualizados;
- no se sepa rápido cuántas personas están activas, de vacaciones o con licencia;
- cualquiera con acceso a la carpeta pueda ver o borrar la información;
- se ingresen RUT o correos mal escritos porque nada los valida;
- las solicitudes de vacaciones o permisos se pierdan y el trabajador no sepa si se las aprobaron.

**Qué resolvemos:** un solo lugar, protegido con contraseña, donde los datos del personal se ingresan validados, se consultan en segundos y donde las solicitudes quedan registradas con su respuesta.

## 3. Usuarios del sistema

| Rol | Descripción | Qué necesita hacer |
|---|---|---|
| **Administrador** | Encargado/a de gestionar la estructura y los expedientes del personal (en los datos de prueba: Catalina Navarro, jefa de RR.HH.). | Crear, editar y eliminar trabajadores, revisar sus fichas, aprobar o rechazar solicitudes y supervisar los indicadores del dashboard. |
| **Asistente de RR.HH.** | Cargo de apoyo dentro de RR.HH. (en los datos de prueba: Sebastián Pérez Lagos). | Ver todos los datos (dashboard, trabajadores, fichas y solicitudes) y **corregir errores de tipeo** en nombre, apellido, correo y teléfono. No puede cambiar datos que afectan a la empresa (RUT, sueldo, cargo, departamento, estado, rol, fecha de ingreso), ni registrar o eliminar trabajadores, ni responder solicitudes. |
| **Empleado** | Trabajador o colaborador de la empresa. | Solicitar vacaciones, permisos o licencias, consultar el estado de sus solicitudes y ver el **directorio de contacto** de sus compañeros (solo nombre, correo y teléfono). |

- Cada usuario entra con **su propio correo y contraseña**. El sistema busca al trabajador con ese correo y, según su **rol**, le muestra un menú distinto.
- Las cuentas se crean a mano en Supabase (Authentication → Users) usando el **mismo correo** registrado en la ficha del trabajador. No hay registro de usuarios desde la app.
- Un trabajador **desvinculado** ya no puede entrar.

## 4. Alcance

**Sí incluye:**
- Login y logout, con tres roles (Administrador, Asistente de RR.HH. y Empleado).
- Dashboard con indicadores (administrador y asistente).
- CRUD de trabajadores, búsqueda, filtros y ficha (el asistente solo ve y corrige datos básicos).
- Solicitudes: el empleado las crea y ve su estado; el administrador las aprueba o rechaza.
- Directorio de contacto para los empleados (nombre, correo y teléfono de los trabajadores vigentes).
- Validaciones y mensajes con SweetAlert2.

**No incluye** (mejoras futuras):
- Marcar entrada y salida (control de asistencia).
- Que al aprobar unas vacaciones cambie solo el estado del trabajador.
- Departamentos o cargos como tablas propias (se usan listas fijas).
- Registro de usuarios desde la app, historial de cambios, exportar a Excel/CSV y paginación.

## 5. Requerimientos funcionales

| ID | Requerimiento |
|---|---|
| **RF01** | El usuario puede iniciar sesión con correo y contraseña (Supabase Auth). |
| **RF02** | El usuario puede cerrar sesión. |
| **RF03** | Sin sesión iniciada, cualquier página interna redirige al login. |
| **RF04** | El dashboard muestra: total de trabajadores, activos, ausentes (vacaciones + licencia), desvinculados, total mensual de sueldos, solicitudes pendientes, un gráfico de trabajadores por departamento y los últimos 5 ingresos. |
| **RF05** | Se puede registrar un trabajador. Su fecha de ingreso es la del día en que se registra. |
| **RF06** | Se puede ver el listado de trabajadores. |
| **RF07** | Se puede editar un trabajador. |
| **RF08** | Se puede eliminar un trabajador, previa confirmación. |
| **RF09** | Se puede buscar por nombre, apellido o RUT, y filtrar por departamento y por estado. |
| **RF10** | Los datos se validan antes de guardarse (ver la [sección 8](#8-validaciones)). |
| **RF11** | Los resultados de las acciones (éxito, error, confirmación) se muestran con SweetAlert2. |
| **RF12** | Se puede ver la ficha de cada trabajador, con sus datos personales y laborales ordenados. |
| **RF13** | Cada usuario tiene un rol. El administrador y el asistente ven todas las secciones; el empleado solo "Mi panel" y el directorio de "Trabajadores". Si alguien intenta abrir una sección o acción que no le corresponde, vuelve a su pantalla de inicio con un aviso. Un trabajador desvinculado no puede iniciar sesión. |
| **RF14** | El empleado puede crear una solicitud de vacaciones, permiso administrativo o licencia médica, con fecha de inicio, fecha de término y motivo. |
| **RF15** | El empleado ve en "Mi panel" sus datos y todas sus solicitudes con su estado (pendiente, aprobada o rechazada). |
| **RF16** | El administrador ve las solicitudes filtradas por estado y puede aprobar o rechazar las pendientes, previa confirmación. Una solicitud ya respondida no se puede volver a responder. El asistente las ve, pero no puede responderlas. |
| **RF17** | El asistente de RR.HH. puede corregir el nombre, apellido, correo y teléfono de un trabajador. Los demás campos le aparecen bloqueados y el servidor ignora cualquier cambio en ellos. No puede registrar ni eliminar trabajadores. |
| **RF18** | El empleado puede abrir "Trabajadores" como directorio de contacto: ve solo el nombre, correo y teléfono de los trabajadores vigentes (no los desvinculados), con búsqueda por nombre o apellido. Al abrir la ficha de alguien ve solo esos mismos datos. El sueldo, el RUT y los demás datos no se le muestran: el servidor ni siquiera los consulta. |

**No funcionales:**
- Las claves van en `.env` y nunca se suben a GitHub.
- Dentro del sistema, todas las páginas exigen haber iniciado sesión y las del administrador exigen el rol correspondiente. La base de datos no tiene protección adicional porque es un proyecto de prueba con datos ficticios.
- La interfaz se adapta al celular.
- Se usan solo datos ficticios.

## 6. Base de datos (Supabase)

Hay **dos tablas**: `trabajadores` y `solicitudes`. Cada solicitud pertenece a un trabajador (relación 1 a N).

### `trabajadores`

| Campo | Tipo | Obligatorio | Reglas |
|---|---|---|---|
| `id` | `bigint` (identity) | auto | Clave primaria |
| `rut` | `varchar(12)` | Sí | Único. Se guarda como `12345678-K` |
| `nombre` | `varchar(60)` | Sí | |
| `apellido` | `varchar(60)` | Sí | |
| `correo` | `varchar(120)` | Sí | Único. Es el mismo correo de su cuenta para entrar |
| `telefono` | `varchar(20)` | No | |
| `departamento` | `varchar(40)` | Sí | Uno de la lista fija |
| `cargo` | `varchar(40)` | Sí | Uno de la lista fija |
| `fecha_ingreso` | `date` | Sí | |
| `sueldo` | `integer` | Sí | Mayor que 0 (en pesos) |
| `estado` | `varchar(20)` | Sí | `activo`, `vacaciones`, `licencia` o `desvinculado`. Por defecto `activo` |
| `rol` | `varchar(20)` | Sí | `admin`, `asistente` o `empleado`. Por defecto `empleado` |
| `created_at` | `timestamptz` | auto | Fecha de creación del registro |

### `solicitudes`

| Campo | Tipo | Obligatorio | Reglas |
|---|---|---|---|
| `id` | `bigint` (identity) | auto | Clave primaria |
| `trabajador_id` | `bigint` | Sí | Clave foránea a `trabajadores.id`. Si se elimina el trabajador, se eliminan sus solicitudes |
| `tipo` | `varchar(20)` | Sí | `vacaciones`, `permiso` o `licencia` |
| `fecha_inicio` | `date` | Sí | |
| `fecha_fin` | `date` | Sí | No puede ser anterior a `fecha_inicio` |
| `motivo` | `varchar(255)` | No | |
| `estado` | `varchar(20)` | Sí | `pendiente`, `aprobada` o `rechazada`. Por defecto `pendiente` |
| `created_at` | `timestamptz` | auto | Cuándo se pidió |

**Acceso:** solo la aplicación Flask usa las tablas, con la clave pública guardada en `.env`. No se usan políticas RLS porque es un proyecto de prueba con datos ficticios.

**Datos de prueba:** 13 trabajadores ficticios (Catalina Navarro es la administradora y Sebastián Pérez el asistente de RR.HH.) y 5 solicitudes de ejemplo, cargados con el mismo script SQL.

### Listas fijas

Están definidas **en el código** (clases `Trabajador` y `Solicitud`). Se usan en los formularios, en los filtros y en la validación.

| Departamentos | Cargos | Estados del trabajador | Tipos de solicitud |
|---|---|---|---|
| Administración | Gerente | Activo | Vacaciones |
| Operaciones | Jefe de área | Vacaciones | Permiso administrativo |
| Ventas | Analista | Licencia | Licencia médica |
| Tecnología | Asistente administrativo | Desvinculado | |
| Recursos Humanos | Ejecutivo de ventas | | |
| | Operario | | |
| | Técnico de soporte | | |

> **Por qué listas fijas y no tablas:** así no hay que construir pantallas extra para administrarlas y se evitan errores de tipeo ("Ventas" / "ventas"). Si más adelante se necesita cambiar una opción, basta con editar la lista en la clase.

## 7. Pantallas

| Ruta | Pantalla | Quién | Qué contiene |
|---|---|---|---|
| `/login` | **Login** | Todos | Correo, contraseña y botón Ingresar. |
| `/dashboard` | **Dashboard** | Admin y asistente | 6 tarjetas (total, activos, ausentes, desvinculados, total de sueldos y solicitudes pendientes), gráfico de barras por departamento y los últimos 5 ingresos. |
| `/trabajadores` | **Listado** | Admin y asistente | Buscador y filtros (departamento, estado). Tabla con RUT, nombre, departamento, cargo, fecha de ingreso, sueldo, estado y botones Ver ficha/Editar/Eliminar. |
| `/trabajadores` | **Directorio** | Empleado | Misma dirección, pero otra plantilla: solo nombre, correo y teléfono de los trabajadores vigentes, con buscador por nombre. Sin filtros ni botones de edición. |
| `/trabajadores/<id>` | **Ficha** | Admin y asistente | Nombre, cargo, departamento y estado arriba; luego *Datos personales* y *Datos laborales* (incluye el rol). Botones Editar y Eliminar. |
| `/trabajadores/<id>` | **Contacto** | Empleado | Solo nombre, correo y teléfono. |
| `/trabajadores/nuevo` | **Formulario** | Administrador | Todos los campos. Departamento, cargo, estado y rol se eligen de un menú. La fecha de ingreso es la de hoy y no se puede cambiar. |
| `/trabajadores/<id>/editar` | **Formulario** | Admin y asistente | El mismo formulario, con los datos cargados. El administrador puede cambiar todo (incluida la fecha de ingreso). El asistente ve el título "Corregir datos del trabajador", un aviso, y solo puede cambiar nombre, apellido, correo y teléfono: el resto aparece bloqueado con un candado. |
| `/solicitudes` | **Solicitudes** | Admin y asistente | Pestañas Pendientes / Aprobadas / Rechazadas / Todas. Tabla con trabajador, tipo, período (y días), motivo, fecha en que se pidió y estado. En las pendientes, botones Aprobar y Rechazar con confirmación (solo el administrador). |
| `/mi-panel` | **Mi panel** | Todos | Saludo, datos del trabajador (cargo, departamento, estado, ingreso, antigüedad, correo) y tabla "Mis solicitudes" con su estado. Botón "Nueva solicitud". |
| `/mi-panel/nueva-solicitud` | **Nueva solicitud** | Todos | Tipo, desde, hasta y motivo. Queda pendiente hasta que el administrador responda. |
| `/logout` | — | Todos | Cierra la sesión y vuelve al login. |

Todas las pantallas, salvo el login, comparten un **menú superior**. El administrador y el asistente ven Dashboard, Trabajadores, Solicitudes y Mi panel (al asistente no le aparecen los botones Nuevo trabajador, Eliminar, Aprobar ni Rechazar); el empleado ve Trabajadores (como directorio) y Mi panel. A la derecha aparecen el nombre y el rol del usuario y el botón para cerrar sesión.

## 8. Validaciones

Se validan **en el navegador** (HTML + JavaScript, para avisar al instante) y **en el servidor** (clases `Trabajador` y `Solicitud`, que es la validación que no se puede saltar).

**Trabajador**

| Campo | Regla | Mensaje |
|---|---|---|
| Todos los obligatorios | No vacíos | "Este campo es obligatorio." |
| RUT | Dígito verificador correcto (módulo 11) | "El RUT no es válido." |
| RUT / correo | No repetidos | "Ya existe un trabajador con ese RUT / correo." |
| Nombre / apellido | Solo letras, 2–60 caracteres | "Solo letras (2 a 60 caracteres)." |
| Correo | Formato `algo@dominio.cl` | "El correo no tiene un formato válido." |
| Teléfono (opcional) | 8–15 dígitos | "El teléfono no es válido." |
| Departamento / cargo / estado / rol | Que sea una opción de la lista | "Selecciona una opción válida." |
| Fecha de ingreso | Al registrar: siempre la fecha de hoy (la fija el servidor). Al editar: que no sea futura | "La fecha de ingreso no puede ser futura." |
| Sueldo | Número entero mayor que 0 | "Ingresa un sueldo válido." |

**Solicitud**

| Campo | Regla | Mensaje |
|---|---|---|
| Tipo | Una opción de la lista | "Selecciona el tipo de solicitud." |
| Desde / hasta | Obligatorias | "Este campo es obligatorio." |
| Hasta | No anterior a "desde" | "La fecha de término no puede ser anterior a la de inicio." |
| Motivo (opcional) | Máximo 255 caracteres | "El motivo no puede superar los 255 caracteres." |

Además, el servidor **siempre** crea la solicitud a nombre de quien inició sesión y como *pendiente*, y cuando edita un asistente solo guarda los datos básicos, aunque alguien intente enviar otros datos desde el navegador. Ocultar o bloquear un campo en la pantalla no basta: la regla importante está en el servidor. Por lo mismo, para un empleado el servidor le pide a Supabase **solo** `id, nombre, apellido, correo, telefono`: el sueldo y los demás datos nunca llegan a su página.

## 9. Arquitectura y estructura

```
Navegador (HTML + CSS + JS)  ⇄  Flask (app.py)  ⇄  Supabase (Auth + tablas trabajadores y solicitudes)
```

```
sistema_rrhh/
├── app.py               # Rutas de Flask y permisos: login_requerido, solo_rrhh y solo_admin
├── trabajador.py        # Clase Trabajador: datos, listas fijas, validar()
├── solicitud.py         # Clase Solicitud: datos, tipos, estados, validar()
├── repositorio.py       # Clases Repositorio (base), RepositorioTrabajadores y RepositorioSolicitudes
├── requirements.txt
├── .env.example         # SECRET_KEY, SUPABASE_URL, SUPABASE_KEY (sin valores)
├── .gitignore           # .env, venv/, __pycache__/
├── README.md
├── supabase/
│   └── esquema.sql      # Tablas, permisos y datos ficticios
├── templates/
│   ├── base.html        # Estructura común + menú según el rol
│   ├── login.html
│   ├── dashboard.html
│   ├── trabajadores.html
│   ├── ficha.html
│   ├── formulario.html
│   ├── solicitudes.html     # Administrador: aprobar / rechazar
│   ├── mi_panel.html        # Empleado: sus datos y sus solicitudes
│   ├── solicitud_form.html  # Empleado: nueva solicitud
│   ├── directorio.html      # Empleado: trabajadores (solo contacto)
│   └── contacto.html        # Empleado: ficha de contacto
├── static/
│   ├── css/styles.css
│   └── js/app.js        # SweetAlert2, validación de RUT, gráfico
└── docs/
```

| Tecnología | Para qué se usa |
|---|---|
| **HTML (Jinja2)** | Las 11 plantillas. Todas heredan de `base.html`. |
| **CSS** | Diseño propio: colores, tarjetas, tablas, pestañas, formularios y versión para celular. |
| **JavaScript** | SweetAlert2 (mensajes y confirmaciones al eliminar, aprobar o rechazar), validación del RUT y gráfico del dashboard (Chart.js). |
| **Flask** | Rutas, sesión del usuario, control de roles y validación en el servidor. |
| **Supabase** | Login (Auth) y base de datos PostgreSQL. |

### Programación Orientada a Objetos

| Clase | Qué representa | Contenido |
|---|---|---|
| `Trabajador` | Un trabajador de la empresa | Atributos (rut, nombre, rol…), listas fijas (incluida `DATOS_BASICOS`, lo que puede corregir el asistente), `validar()`, `a_dict()`, `desde_dict()`, propiedades `nombre_completo`, `antiguedad` y `es_admin` |
| `Solicitud` | Un pedido de vacaciones, permiso o licencia | Atributos, tipos y estados, `validar()`, propiedades `dias` y `esta_pendiente` |
| `Repositorio` | Clase base del acceso a Supabase | `_tabla()` y `_ejecutar()` (traduce los errores a mensajes claros) |
| `RepositorioTrabajadores` | La tabla `trabajadores` (hereda de `Repositorio`) | `listar()`, `buscar()`, `obtener()`, `obtener_por_correo()`, `crear()`, `actualizar()`, `eliminar()`, y para los empleados `directorio()` y `obtener_contacto()`, que piden solo las columnas de contacto |
| `RepositorioSolicitudes` | La tabla `solicitudes` (hereda de `Repositorio`) | `listar()`, `de_trabajador()`, `crear()`, `responder()` |

Conceptos que se pueden mostrar en la presentación:
- **Herencia:** `RepositorioTrabajadores` y `RepositorioSolicitudes` heredan de `Repositorio` y reutilizan `_ejecutar()`.
- **Encapsulamiento:** el cliente de Supabase queda dentro de los repositorios.
- **Constructor, métodos de instancia y de clase, propiedades.**
- **Separación de responsabilidades:** las clases del dominio (`Trabajador`, `Solicitud`) validan y los repositorios guardan.

## 10. Organización del equipo

| # | Responsable de | Archivos |
|---|---|---|
| 1 | Supabase: proyecto, tablas y datos ficticios | `supabase/esquema.sql`, `repositorio.py` |
| 2 | Login, roles y protección de páginas | Rutas de login/logout, `login_requerido`, `solo_rrhh` y `solo_admin` en `app.py`, `.env.example`, `.gitignore` |
| 3 | Clases Trabajador y Solicitud (validaciones) | `trabajador.py`, `solicitud.py` |
| 4 | CRUD, búsqueda, filtros y ficha | Rutas de trabajadores en `app.py`, `trabajadores.html`, `ficha.html`, `formulario.html` |
| 5 | Dashboard, solicitudes y JavaScript | `dashboard.html`, `solicitudes.html`, `mi_panel.html`, `solicitud_form.html`, `static/js/app.js` |
| 6 | Diseño, pruebas e informe | `base.html`, `login.html`, `static/css/styles.css`, `docs/PRUEBAS.md` |

Cada integrante debe poder **explicar su parte** y subirla con **sus propios commits**, que son la evidencia de colaboración que pide la rúbrica. Si el equipo tiene menos de 6 personas, se juntan los roles 5 y 6.

## 11. Cronograma

| Día | Qué se hace |
|---|---|
| **Vie 25/09** | Aprobar este plan. Crear el proyecto en Supabase y la tabla. Repartir los roles. |
| **Sáb 26/09** | Login, clase `Trabajador`, repositorio y CRUD básico funcionando. |
| **Dom 27/09** | Ficha, roles y solicitudes. Dashboard, JavaScript y diseño CSS. |
| **Lun 28/09** | Pruebas (`PRUEBAS.md`), capturas, informe y README. |
| **Mar 29/09** | Entrega y presentación. |

## 12. Lista de entrega (según rúbrica)

- [ ] Login con roles, dashboard, CRUD, ficha, búsqueda/filtros, solicitudes, validaciones y SweetAlert2 funcionando con Supabase.
- [ ] Carpetas `templates/`, `static/css/` y `static/js/` usadas correctamente.
- [ ] `README.md`, `requirements.txt`, `.gitignore` y `.env.example` en el repositorio.
- [ ] Sin `.env` ni `venv/` en GitHub.
- [ ] Commits de todos los integrantes.
- [ ] Informe con las 13 secciones (`docs/GUIA_INFORME.md`) y la tabla de pruebas completa.
- [ ] Capturas de la app (con los tres roles), de Supabase y de GitHub.
- [ ] Cada integrante puede explicar su parte.
