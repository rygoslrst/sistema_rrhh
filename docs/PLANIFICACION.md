# Planificación — TalentoRH: control de trabajadores

> Evaluación II y III · Programación Orientada a Objeto · 4º Medio H
> Contexto: **B. Gestión de Recursos Humanos** · Entrega: **martes 29 de septiembre de 2026**
> Estado del plan: **aprobado el 25-09-2026**. El código se escribió desde cero siguiendo este documento.

---

## 1. Idea en una frase

Una aplicación web sencilla para que el área de RR.HH. **registre y controle a los trabajadores** de la empresa: quiénes son, en qué área y cargo están, desde cuándo, cuánto ganan y en qué estado se encuentran.

## 2. Problema

**Organización (ficticia):** *Comercial Los Andes SpA*, empresa de distribución con unas 60 personas.

**Situación actual:** los datos del personal están en planillas Excel que se copian y modifican por separado. Esto provoca que:

- haya trabajadores duplicados o con datos desactualizados;
- no se sepa rápido cuántas personas están activas, de vacaciones o con licencia;
- cualquiera con acceso a la carpeta pueda ver o borrar la información;
- se ingresen RUT o correos mal escritos porque nada los valida.

**Qué resolvemos:** un solo lugar, protegido con contraseña, donde los datos del personal se ingresan validados y se consultan en segundos.

## 3. Usuarios

| Usuario | Qué hace en el sistema |
|---|---|
| **Encargado/a de RR.HH.** | Registra, edita, busca y elimina trabajadores. |
| **Jefatura** | Revisa el dashboard para ver cuántas personas hay disponibles. |

Ambos usan la misma cuenta y tienen los mismos permisos. Las cuentas se crean a mano en Supabase y **no** hay registro de usuarios desde la app.

## 4. Alcance

**Sí incluye:**
- Login y logout.
- Dashboard.
- CRUD de trabajadores.
- Búsqueda y filtros.
- Validaciones.
- Mensajes con SweetAlert2.

**No incluye** (queda como mejora futura si sobra tiempo):
- Departamentos o cargos como tablas propias. Se usan listas fijas.
- Roles de usuario distintos.
- Registro de usuarios desde la app.
- Historial de cambios.
- Exportar a Excel/CSV.
- Paginación.

## 5. Requerimientos funcionales

| ID | Requerimiento |
|---|---|
| **RF01** | El usuario puede iniciar sesión con correo y contraseña (Supabase Auth). |
| **RF02** | El usuario puede cerrar sesión. |
| **RF03** | Sin sesión iniciada, cualquier página interna redirige al login. |
| **RF04** | El dashboard muestra: total de trabajadores, activos, ausentes (vacaciones + licencia), desvinculados, total mensual de sueldos, un gráfico de trabajadores por departamento y los últimos 5 ingresos. |
| **RF05** | Se puede registrar un trabajador. |
| **RF06** | Se puede ver el listado de trabajadores. |
| **RF07** | Se puede editar un trabajador. |
| **RF08** | Se puede eliminar un trabajador, previa confirmación. |
| **RF09** | Se puede buscar por nombre, apellido o RUT, y filtrar por departamento y por estado. |
| **RF10** | Los datos se validan antes de guardarse (ver la [sección 8](#8-validaciones)). |
| **RF11** | Los resultados de las acciones (éxito, error, confirmación) se muestran con SweetAlert2. |

**No funcionales:**
- Las claves van en `.env` y nunca se suben a GitHub.
- Dentro del sistema, todas las páginas exigen haber iniciado sesión. La base de datos no tiene protección adicional porque es un proyecto de prueba con datos ficticios.
- La interfaz se adapta al celular.
- Se usan solo datos ficticios.

## 6. Base de datos (Supabase)

Hay **una sola tabla**: `trabajadores`.

| Campo | Tipo | Obligatorio | Reglas |
|---|---|---|---|
| `id` | `bigint` (identity) | auto | Clave primaria |
| `rut` | `varchar(12)` | Sí | Único. Se guarda como `12345678-K` |
| `nombre` | `varchar(60)` | Sí | |
| `apellido` | `varchar(60)` | Sí | |
| `correo` | `varchar(120)` | Sí | Único |
| `telefono` | `varchar(20)` | No | |
| `departamento` | `varchar(40)` | Sí | Uno de la lista fija |
| `cargo` | `varchar(40)` | Sí | Uno de la lista fija |
| `fecha_ingreso` | `date` | Sí | |
| `sueldo` | `integer` | Sí | Mayor que 0 (en pesos) |
| `estado` | `varchar(20)` | Sí | `activo`, `vacaciones`, `licencia` o `desvinculado`. Por defecto `activo` |
| `created_at` | `timestamptz` | auto | Fecha de creación del registro |

**Acceso:** solo la aplicación Flask usa la tabla, con la clave pública guardada en `.env`. No se usan políticas RLS porque es un proyecto de prueba con datos ficticios.

**Datos de prueba:** unos 12 trabajadores ficticios cargados con el mismo script SQL.

### Listas fijas

Están definidas **en el código** (en la clase `Trabajador`). Se usan en el formulario, en los filtros y en la validación.

| Departamentos | Cargos | Estados |
|---|---|---|
| Administración | Gerente | Activo |
| Operaciones | Jefe de área | Vacaciones |
| Ventas | Analista | Licencia |
| Tecnología | Asistente administrativo | Desvinculado |
| Recursos Humanos | Ejecutivo de ventas | |
| | Operario | |
| | Técnico de soporte | |

> **Por qué listas fijas y no tablas:** así no hay que construir pantallas extra para administrarlas y se evitan errores de tipeo ("Ventas" / "ventas"). Si más adelante se necesita cambiar una opción, basta con editar la lista en la clase.

## 7. Pantallas

| Ruta | Pantalla | Qué contiene |
|---|---|---|
| `/login` | **Login** | Correo, contraseña y botón Ingresar. |
| `/dashboard` | **Dashboard** | 5 tarjetas (total, activos, ausentes, desvinculados, total de sueldos), gráfico de barras por departamento y tabla con los últimos 5 ingresos. |
| `/trabajadores` | **Listado** | Buscador y filtros (departamento, estado). Tabla con RUT, nombre, departamento, cargo, fecha de ingreso, sueldo, estado y botones Editar/Eliminar. |
| `/trabajadores/nuevo` | **Formulario** | Todos los campos de la tabla. Departamento, cargo y estado se eligen de un menú. |
| `/trabajadores/<id>/editar` | **Formulario** | El mismo formulario, con los datos cargados. |
| `/trabajadores/<id>/eliminar` | — | Solo POST, después de confirmar con SweetAlert2. |
| `/logout` | — | Cierra la sesión y vuelve al login. |

Todas las pantallas, salvo el login, comparten un **menú superior** con el nombre del sistema, los enlaces a Dashboard y Trabajadores, el correo del usuario y el botón para cerrar sesión.

## 8. Validaciones

Se validan **en el navegador** (HTML + JavaScript, para avisar al instante) y **en el servidor** (clase `Trabajador`, que es la validación que no se puede saltar).

| Campo | Regla | Mensaje |
|---|---|---|
| Todos los obligatorios | No vacíos | "Este campo es obligatorio." |
| RUT | Dígito verificador correcto (módulo 11) | "El RUT no es válido." |
| RUT / correo | No repetidos | "Ya existe un trabajador con ese RUT / correo." |
| Nombre / apellido | Solo letras, 2–60 caracteres | "Solo letras (2 a 60 caracteres)." |
| Correo | Formato `algo@dominio.cl` | "El correo no tiene un formato válido." |
| Teléfono (opcional) | 8–15 dígitos | "El teléfono no es válido." |
| Departamento / cargo / estado | Que sea una opción de la lista | "Selecciona una opción válida." |
| Fecha de ingreso | Que no sea futura | "La fecha de ingreso no puede ser futura." |
| Sueldo | Número entero mayor que 0 | "Ingresa un sueldo válido." |

## 9. Arquitectura y estructura

```
Navegador (HTML + CSS + JS)  ⇄  Flask (app.py)  ⇄  Supabase (Auth + tabla trabajadores)
```

```
sistema_rrhh/
├── app.py               # Rutas de Flask, login_requerido
├── trabajador.py        # Clase Trabajador: datos, listas fijas, validar()
├── repositorio.py       # Clase RepositorioTrabajadores: consultas a Supabase
├── requirements.txt
├── .env.example         # SECRET_KEY, SUPABASE_URL, SUPABASE_KEY (sin valores)
├── .gitignore           # .env, venv/, __pycache__/
├── README.md
├── supabase/
│   └── esquema.sql      # Tabla, permisos y datos ficticios
├── templates/
│   ├── base.html        # Estructura común + menú
│   ├── login.html
│   ├── dashboard.html
│   ├── trabajadores.html
│   └── formulario.html
├── static/
│   ├── css/styles.css
│   └── js/app.js        # SweetAlert2, validación de RUT, gráfico
└── docs/
```

| Tecnología | Para qué se usa |
|---|---|
| **HTML (Jinja2)** | Las 5 plantillas. Todas heredan de `base.html`. |
| **CSS** | Diseño propio: colores, tarjetas, tabla, formulario y versión para celular. |
| **JavaScript** | SweetAlert2 (mensajes y confirmación al eliminar), validación del RUT y gráfico del dashboard (Chart.js). |
| **Flask** | Rutas, sesión del usuario y validación en el servidor. |
| **Supabase** | Login (Auth) y base de datos PostgreSQL. |

### Programación Orientada a Objetos

| Clase | Qué representa | Contenido |
|---|---|---|
| `Trabajador` | Un trabajador de la empresa | Atributos (rut, nombre…), constantes con las listas fijas, `validar()`, `a_dict()`, `desde_dict()`, propiedades `nombre_completo` y `antiguedad` |
| `RepositorioTrabajadores` | El acceso a la tabla en Supabase | `listar()`, `buscar()`, `obtener()`, `crear()`, `actualizar()`, `eliminar()` |

Conceptos que se pueden mostrar en la presentación:
- **Encapsulamiento:** el cliente de Supabase queda dentro del repositorio.
- **Constructor:** `__init__`.
- **Métodos de instancia y de clase.**
- **Propiedades.**
- **Separación de responsabilidades:** `Trabajador` valida y `RepositorioTrabajadores` guarda.

## 10. Organización del equipo

| # | Responsable de | Archivos |
|---|---|---|
| 1 | Supabase: proyecto, tabla y datos ficticios | `supabase/esquema.sql`, `repositorio.py` |
| 2 | Login y protección de páginas | Rutas de login/logout en `app.py`, `.env.example`, `.gitignore` |
| 3 | Clase Trabajador y validaciones | `trabajador.py` |
| 4 | CRUD, búsqueda y filtros | Rutas de trabajadores en `app.py`, `trabajadores.html`, `formulario.html` |
| 5 | Dashboard y JavaScript | `dashboard.html`, `static/js/app.js` |
| 6 | Diseño, pruebas e informe | `base.html`, `login.html`, `static/css/styles.css`, `docs/PRUEBAS.md` |

Cada integrante debe poder **explicar su parte** y subirla con **sus propios commits**, que son la evidencia de colaboración que pide la rúbrica. Si el equipo tiene menos de 6 personas, se juntan los roles 5 y 6.

## 11. Cronograma

| Día | Qué se hace |
|---|---|
| **Vie 25/09** | Aprobar este plan. Crear el proyecto en Supabase y la tabla. Repartir los roles. |
| **Sáb 26/09** | Login, clase `Trabajador`, repositorio y CRUD básico funcionando. |
| **Dom 27/09** | Dashboard, búsqueda y filtros, JavaScript y diseño CSS. |
| **Lun 28/09** | Pruebas (`PRUEBAS.md`), capturas, informe y README. |
| **Mar 29/09** | Entrega y presentación. |

## 12. Lista de entrega (según rúbrica)

- [ ] Login, dashboard, CRUD, búsqueda/filtros, validaciones y SweetAlert2 funcionando con Supabase.
- [ ] Carpetas `templates/`, `static/css/` y `static/js/` usadas correctamente.
- [ ] `README.md`, `requirements.txt`, `.gitignore` y `.env.example` en el repositorio.
- [ ] Sin `.env` ni `venv/` en GitHub.
- [ ] Commits de todos los integrantes.
- [ ] Informe con las 13 secciones (`docs/GUIA_INFORME.md`) y la tabla de pruebas completa.
- [ ] Capturas de la app, de Supabase y de GitHub.
- [ ] Cada integrante puede explicar su parte.
