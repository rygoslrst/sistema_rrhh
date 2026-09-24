# TalentoRH — Sistema de Gestión de Recursos Humanos

Aplicación web para administrar el personal de una empresa: trabajadores, departamentos y cargos, con un dashboard de indicadores. Está hecha con **Python + Flask** y usa **Supabase** para la autenticación y la base de datos.

> Proyecto académico — Evaluación II y III de Programación Orientada a Objeto, 4º Medio H.
> **Todos los datos son ficticios.**

## Funcionalidades

- 🔐 Inicio de sesión con correo y contraseña (Supabase Auth) y rutas protegidas.
- 📊 Dashboard: trabajadores vigentes, activos, ausentes, nómina mensual, gráficos por departamento y estado, y últimos ingresos.
- 👥 CRUD de **trabajadores** con búsqueda (nombre, RUT, correo) y filtros (departamento, estado).
- 🏢 CRUD de **departamentos** y 💼 **cargos**. No permite borrar un departamento o cargo que tenga personal.
- ✅ Validaciones en el navegador y en el servidor: RUT chileno con dígito verificador, correo, fechas, sueldos y duplicados.
- 💬 Mensajes y confirmaciones con SweetAlert2.
- 📱 Diseño propio y *responsive*.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Backend | Python 3.11+, Flask 3 |
| Base de datos y autenticación | Supabase (PostgreSQL + Auth + RLS), librería `supabase-py` |
| Frontend | HTML (Jinja2), CSS propio, JavaScript |
| Librerías JS (CDN) | SweetAlert2, Chart.js, Bootstrap Icons |

## Estructura del proyecto

```
sistema_rrhh/
├── app.py                  # Crea la app Flask y registra las rutas
├── config.py               # Lee las variables de entorno (.env)
├── requirements.txt
├── .env.example            # Plantilla de variables (sin claves reales)
├── models/                 # Clases de dominio (POO)
│   ├── entidad.py          #   Clase abstracta base
│   ├── trabajador.py
│   ├── departamento.py
│   └── cargo.py
├── services/               # Lógica y acceso a datos
│   ├── conexion.py         #   Cliente de Supabase por usuario
│   ├── autenticacion.py    #   Login y renovación de sesión
│   ├── repositorios.py     #   CRUD genérico + un repositorio por tabla
│   └── estadisticas.py     #   Indicadores del dashboard
├── routes/                 # Blueprints de Flask (una por módulo)
│   ├── auth.py  dashboard.py  trabajadores.py  departamentos.py  cargos.py
├── utils/
│   ├── seguridad.py        #   Decorador login_requerido, sesión
│   └── validadores.py      #   RUT, correo, conversiones
├── templates/              # Vistas HTML (Jinja2)
│   ├── base.html  panel.html  login.html  dashboard.html  error.html  macros.html
│   ├── trabajadores/  departamentos/  cargos/
├── static/
│   ├── css/styles.css
│   ├── js/app.js
│   └── img/favicon.svg
├── supabase/
│   ├── 01_esquema.sql      # Tablas, relaciones, RLS
│   └── 02_datos_ficticios.sql
└── docs/                   # Planificación, BD, pruebas y guía del informe
```

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/sistema_rrhh.git
cd sistema_rrhh
```

### 2. Crear el entorno virtual e instalar las dependencias

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar Supabase (una sola vez, lo hace una persona del equipo)

1. Crear un proyecto en [supabase.com](https://supabase.com) (región sugerida: *South America (São Paulo)*).
2. Ir a **SQL Editor → New query**, pegar el contenido de `supabase/01_esquema.sql` y presionar **Run**.
3. Repetir con `supabase/02_datos_ficticios.sql` para cargar los datos de prueba.
4. Ir a **Authentication → Users → Add user → Create new user**, ingresar un correo ficticio (ej.: `admin@losandes-demo.cl`) y una contraseña, y marcar **Auto Confirm User**.
5. En **Project Settings → API Keys** (o con el botón **Connect**) copiar la **Project URL** y la clave **anon / publishable**.

> ⚠️ Nunca usen la clave `service_role` / `secret` en este proyecto.

### 4. Crear el archivo `.env`

```bash
cp .env.example .env        # En Windows: copy .env.example .env
```

Completar los valores:

```env
SECRET_KEY=una_clave_larga_y_aleatoria
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=clave_anon_o_publishable
```

Para generar `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`

### 5. Ejecutar

```bash
python app.py
```

Abrir <http://127.0.0.1:5000> e iniciar sesión con el usuario creado en el paso 3.4.

## Seguridad

- Las claves solo existen en `.env`, que está en `.gitignore`. En GitHub solo se sube `.env.example`.
- La base de datos tiene **Row Level Security**: sin sesión iniciada no se puede leer ni escribir ningún dato.
- Flask consulta Supabase con el **token del usuario conectado**, no con una clave maestra.
- La cookie de sesión es `HttpOnly` y `SameSite=Lax`. Las acciones que modifican datos se hacen con `POST`.

## Documentación

- [Planificación: problema, requerimientos, arquitectura, POO y reparto del equipo](docs/PLANIFICACION.md)
- [Diseño de la base de datos](docs/BASE_DE_DATOS.md)
- [Plan de pruebas](docs/PRUEBAS.md)
- [Guía del informe](docs/GUIA_INFORME.md)

## Equipo

| Integrante | Rol |
|---|---|
| *Nombre 1* | Base de datos y Supabase |
| *Nombre 2* | Autenticación y seguridad |
| *Nombre 3* | Módulo Trabajadores |
| *Nombre 4* | Departamentos, Cargos y POO |
| *Nombre 5* | Dashboard y JavaScript |
| *Nombre 6* | Diseño, pruebas e informe |

Docente: *Nombre del docente* · Curso: 4º Medio H · Septiembre 2026
