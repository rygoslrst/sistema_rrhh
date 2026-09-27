# TalentoRH — Control de trabajadores

Aplicación web para que el área de Recursos Humanos registre y controle a los trabajadores de una empresa, y para que cada trabajador pida sus vacaciones o permisos. Está hecha con **Python + Flask** y usa **Supabase** para el inicio de sesión y la base de datos.

> Proyecto académico — Evaluación II y III de Programación Orientada a Objeto, 4º Medio H.
> **Todos los datos son ficticios.**

## Funcionalidades

- Inicio de sesión con correo y contraseña (Supabase Auth) y **tres roles**:
  - **Administrador:** ve el dashboard, administra a los trabajadores y responde las solicitudes.
  - **Asistente de RR.HH.:** ve todo, pero solo puede corregir nombre, apellido, correo y teléfono. No cambia sueldos ni datos laborales, no registra ni elimina trabajadores y no responde solicitudes.
  - **Empleado:** ve **Mi panel** (sus datos y sus solicitudes) y **Trabajadores** como directorio de contacto: solo nombre, correo y teléfono de sus compañeros.
- **Dashboard:** total de trabajadores, activos, ausentes, desvinculados, total de sueldos, solicitudes pendientes, gráfico por departamento y últimos ingresos.
- **Solicitudes:** el empleado pide vacaciones, un permiso o una licencia y ve si está pendiente, aprobada o rechazada; el administrador las aprueba o rechaza.
- **Trabajadores:** registrar, listar, editar y eliminar (con confirmación).
- **Ficha de cada trabajador** con sus datos personales y laborales ordenados (se abre haciendo clic en su nombre).
- **Búsqueda** por nombre, apellido o RUT, y **filtros** por departamento y estado.
- **Validaciones** en el navegador y en el servidor: RUT con dígito verificador, correo, fecha de ingreso, sueldo y datos repetidos.
- Mensajes con **SweetAlert2** y diseño adaptado a celulares.

## Tecnologías

Python 3.10+, Flask 3, Supabase (PostgreSQL + Auth), HTML con Jinja2, CSS propio y JavaScript con SweetAlert2 y Chart.js.

## Estructura

```
sistema_rrhh/
├── app.py               # Rutas de Flask y permisos (login_requerido, solo_rrhh, solo_admin)
├── trabajador.py        # Clase Trabajador: datos, listas fijas y validaciones
├── solicitud.py         # Clase Solicitud: tipos, estados y validaciones
├── repositorio.py       # Login y clases Repositorio, RepositorioTrabajadores y RepositorioSolicitudes
├── requirements.txt
├── .env.example         # Variables necesarias (sin valores reales)
├── supabase/
│   └── esquema.sql      # Tablas, permisos y datos ficticios
├── templates/           # base, login, dashboard, trabajadores, ficha, formulario,
│                        # solicitudes, mi_panel, solicitud_form, directorio, contacto
└── static/
    ├── css/styles.css
    ├── js/app.js
    └── img/favicon.svg
```

## Instalación

### 1. Descargar el proyecto e instalar las dependencias

```bash
git clone https://github.com/rygoslrst/sistema_rrhh.git
cd sistema_rrhh
python -m venv venv
```

Activar el entorno virtual:
- **Windows:** `venv\Scripts\activate`
- **macOS / Linux:** `source venv/bin/activate`

```bash
pip install -r requirements.txt
```

### 2. Preparar Supabase (lo hace una sola persona del equipo)

1. Crear un proyecto en [supabase.com](https://supabase.com).
2. Ir a **SQL Editor → New query**, pegar el contenido de `supabase/esquema.sql` y presionar **Run**.
3. Ir a **Authentication → Users → Add user → Create new user** y crear las cuentas marcando **Auto Confirm User**. El correo debe ser **el mismo que tiene el trabajador en su ficha**:
   - `rrhh@losandes-demo.cl` → Catalina Navarro, **administradora**.
   - `sebastian.perez@losandes-demo.cl` → Sebastián Pérez, **asistente de RR.HH.**
   - `matias.soto@losandes-demo.cl` (u otro trabajador) → para probar el rol **empleado**.
4. En **Project Settings → API Keys** (o con el botón **Connect**), copiar la **Project URL** y la clave **anon / publishable**.

> ⚠️ Nunca usen la clave `service_role` / `secret`.

### 3. Crear el archivo `.env`

Copiar `.env.example` con el nombre `.env` y completar los valores:

```env
SECRET_KEY=una_clave_larga_y_aleatoria
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=clave_anon_o_publishable
```

Para generar `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`

El archivo `.env` **no se sube a GitHub** porque está en `.gitignore`.

### 4. Ejecutar

```bash
python app.py
```

Abrir <http://127.0.0.1:5000> e ingresar con una de las cuentas creadas en Supabase. El administrador y el asistente llegan al Dashboard; el empleado, a Mi panel.

**Para que un nuevo trabajador pueda entrar:** el administrador lo registra en el sistema (con su rol) y después le crea una cuenta en Supabase con el mismo correo.

## Seguridad dentro del sistema

- Para usar cualquier página hay que iniciar sesión; si no, el sistema redirige al login.
- Cada sección y acción revisa el rol en el servidor: el empleado solo entra a Mi panel y al directorio (el servidor ni siquiera consulta sueldos ni datos laborales para él), y el asistente no puede registrar, eliminar, responder solicitudes ni cambiar datos laborales (aunque manipule el formulario).
- Un trabajador desvinculado ya no puede entrar, y nadie puede eliminar su propio registro.
- Las solicitudes siempre se guardan a nombre de quien inició sesión y como pendientes.
- Los formularios validan los datos antes de guardarlos y se pide confirmación antes de eliminar, aprobar o rechazar.
- Las claves solo están en `.env`. En GitHub se sube únicamente `.env.example`.
- Como es un proyecto de prueba con datos ficticios, la base de datos no tiene protección adicional (sin políticas RLS).

## Equipo

| Integrante | Responsable de |
|---|---|
| *Nombre 1* | Supabase y repositorio |
| *Nombre 2* | Login, roles y protección de páginas |
| *Nombre 3* | Clases Trabajador y Solicitud |
| *Nombre 4* | CRUD, búsqueda, filtros y ficha |
| *Nombre 5* | Dashboard, solicitudes y JavaScript |
| *Nombre 6* | Diseño, pruebas e informe |

Docente: *Nombre del docente* · 4º Medio H · Septiembre 2026
