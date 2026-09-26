# TalentoRH — Control de trabajadores

Aplicación web para que el área de Recursos Humanos registre y controle a los trabajadores de una empresa. Está hecha con **Python + Flask** y usa **Supabase** para el inicio de sesión y la base de datos.

> Proyecto académico — Evaluación II y III de Programación Orientada a Objeto, 4º Medio H.
> **Todos los datos son ficticios.**

## Funcionalidades

- Inicio de sesión con correo y contraseña (Supabase Auth). Sin sesión no se puede entrar a ninguna página interna.
- **Dashboard:** total de trabajadores, activos, ausentes, desvinculados, total de sueldos, gráfico por departamento y últimos ingresos.
- **Trabajadores:** registrar, listar, editar y eliminar (con confirmación).
- **Búsqueda** por nombre, apellido o RUT, y **filtros** por departamento y estado.
- **Validaciones** en el navegador y en el servidor: RUT con dígito verificador, correo, fecha de ingreso, sueldo y datos repetidos.
- Mensajes con **SweetAlert2** y diseño adaptado a celulares.

## Tecnologías

Python 3.10+, Flask 3, Supabase (PostgreSQL + Auth), HTML con Jinja2, CSS propio y JavaScript con SweetAlert2 y Chart.js.

## Estructura

```
sistema_rrhh/
├── app.py               # Rutas de Flask y protección de páginas (login_requerido)
├── trabajador.py        # Clase Trabajador: datos, listas fijas y validaciones
├── repositorio.py       # Login y clase RepositorioTrabajadores (consultas a Supabase)
├── requirements.txt
├── .env.example         # Variables necesarias (sin valores reales)
├── supabase/
│   └── esquema.sql      # Tabla, permisos y datos ficticios
├── templates/           # base, login, dashboard, trabajadores, formulario
├── static/
│   ├── css/styles.css
│   ├── js/app.js
│   └── img/favicon.svg
└── docs/                # Planificación, pruebas y guía del informe
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
3. Ir a **Authentication → Users → Add user → Create new user**, ingresar un correo ficticio (ej.: `rrhh@losandes-demo.cl`) y una contraseña, y marcar **Auto Confirm User**.
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

Abrir <http://127.0.0.1:5000> e ingresar con el usuario creado en Supabase.

## Seguridad dentro del sistema

- Para usar cualquier página hay que iniciar sesión; si no, el sistema redirige al login.
- Los formularios validan los datos antes de guardarlos y se pide confirmación antes de eliminar.
- Las claves solo están en `.env`. En GitHub se sube únicamente `.env.example`.
- Como es un proyecto de prueba con datos ficticios, la base de datos no tiene protección adicional (sin políticas RLS).

## Documentación

- [Planificación del proyecto](docs/PLANIFICACION.md)
- [Plan de pruebas](docs/PRUEBAS.md)
- [Guía del informe](docs/GUIA_INFORME.md)

## Equipo

| Integrante | Responsable de |
|---|---|
| *Nombre 1* | Supabase y repositorio |
| *Nombre 2* | Login y protección de páginas |
| *Nombre 3* | Clase Trabajador y validaciones |
| *Nombre 4* | CRUD, búsqueda y filtros |
| *Nombre 5* | Dashboard y JavaScript |
| *Nombre 6* | Diseño, pruebas e informe |

Docente: *Nombre del docente* · 4º Medio H · Septiembre 2026
