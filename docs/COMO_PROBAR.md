# Cómo probar TalentoRH (guía para el equipo)

Tiempo total: unos 20 minutos la primera vez. Todos usamos **la misma base de datos en Supabase**, así que no hay que crear nada en Supabase.

## 0. Antes de empezar

- **Python 3.10 o superior.** Revisa tu versión con `python --version`. Si no lo tienes, instálalo desde python.org y marca *"Add Python to PATH"*.
- **Git.** Revisa con `git --version`.
- **Pídele por privado al dueño del repositorio** (WhatsApp, no por GitHub):
  1. la **clave de Supabase** (`SUPABASE_KEY`);
  2. la **contraseña** de las cuentas de prueba.

  Estos datos **nunca** se escriben en el código ni se suben a GitHub.

## 1. Descargar el proyecto (solo la primera vez)

Abre una terminal (PowerShell en Windows) y ejecuta:

```bash
git clone https://github.com/rygoslrst/sistema_rrhh.git
cd sistema_rrhh
```

## 2. Instalar lo necesario (solo la primera vez)

```bash
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
```

> En macOS / Linux usa `python3 -m venv venv` y `venv/bin/python -m pip install -r requirements.txt`.

## 3. Crear tu archivo `.env` (solo la primera vez)

```bash
copy .env.example .env
venv\Scripts\python -c "import secrets; print(secrets.token_hex(32))"
notepad .env
```

El segundo comando imprime un texto largo: esa es tu `SECRET_KEY`. En el Bloc de notas deja el archivo así y guarda con `Ctrl + S`:

```env
SECRET_KEY=el_texto_largo_que_imprimió_el_comando
SUPABASE_URL=https://gjylylfemxqvesjkkdxm.supabase.co
SUPABASE_KEY=la_clave_que_te_pasaron_por_privado
```

> En macOS / Linux: `cp .env.example .env` y ábrelo con cualquier editor.

## 4. Iniciar el sistema (cada vez que quieras usarlo)

```bash
venv\Scripts\python app.py
```

> En macOS / Linux: `venv/bin/python app.py`.

Abre **http://127.0.0.1:5000** en el navegador. Para detenerlo, vuelve a la terminal y presiona `Ctrl + C`.

Si ya tenías el proyecto descargado, antes de iniciarlo trae los últimos cambios con `git pull`.

## 5. Cuentas de prueba

La contraseña es la misma para las tres (pídela por privado).

| Correo | Quién es | Rol | Qué puede hacer |
|---|---|---|---|
| `rrhh@losandes-demo.cl` | Catalina Navarro | **Administradora** | Todo: dashboard, registrar/editar/eliminar trabajadores, aprobar o rechazar solicitudes |
| `sebastian.perez@losandes-demo.cl` | Sebastián Pérez | **Asistente de RR.HH.** | Ve todo, pero solo corrige nombre, apellido, correo y teléfono. No registra, no elimina y no responde solicitudes |
| `matias.soto@losandes-demo.cl` | Matías Soto | **Empleado** | Mi panel (sus datos y solicitudes) y un directorio de trabajadores con solo nombre, correo y teléfono |

Para cambiar de cuenta, cierra sesión (ícono arriba a la derecha) o usa una **ventana de incógnito** para cada cuenta.

## 6. Qué probar (unos 15 minutos)

Los números (P24, P31…) corresponden a [PRUEBAS.md](PRUEBAS.md), que tiene el resultado esperado de cada prueba.

**A. Como Matías (empleado)**
1. Entra y comprueba que llegas a **Mi panel** y que el menú solo tiene *Trabajadores* y *Mi panel* (P24).
2. Abre **Trabajadores**: solo debe mostrar nombre, correo y teléfono. Busca `rojas` y abre la ficha de alguien (P39, P40).
3. Presiona **Nueva solicitud**, pon "Hasta" antes de "Desde" y revisa el error (P29). Luego pide vacaciones con fechas correctas (P30).
4. Escribe `http://127.0.0.1:5000/dashboard` en la barra de direcciones: debe devolverte a tu panel con un aviso (P25).

**B. Como Sebastián (asistente)**
1. Entra al Dashboard y revisa que **no** aparezca el botón "Nuevo trabajador" (P35).
2. Abre la ficha de alguien y presiona **Corregir datos**: el sueldo, el RUT, el cargo y los demás datos importantes deben aparecer bloqueados. Cambia solo el teléfono y guarda (P36, P37).
3. Entra a **Solicitudes**: ves la de Matías, pero sin botones para aprobar o rechazar (P38).

**C. Como Catalina (administradora)**
1. Revisa el **Dashboard**: las tarjetas, el gráfico y "Solicitudes pendientes" (P04, P05).
2. En **Solicitudes** aprueba la solicitud de Matías (P32) y rechaza otra (P33).
3. Registra un trabajador de prueba con datos inventados: la fecha de ingreso se pone sola con la de hoy (P15). Pruébale un RUT inválido como `12.345.678-9` (P11). Después **elimínalo** (P19).
4. Vuelve a entrar como Matías y confirma que su solicitud aparece **Aprobada** (P32).

## 7. Reglas para no romper los datos

Como la base de datos es compartida, lo que cambias lo ven todos:

- **No elimines ni cambies el correo ni el rol** de Catalina, Sebastián o Matías: sus cuentas dejarían de funcionar.
- Usa **solo datos inventados**. Si registras trabajadores de prueba, bórralos al terminar.
- Si algo se desordena, avísale al equipo antes de arreglarlo "a mano" en Supabase.

## 8. Anotar resultados y subirlos

1. En `docs/PRUEBAS.md` completa en tus pruebas el **resultado obtenido**, ✅ o ❌ y tu nombre en **Responsable**.
2. Guarda tus capturas en `docs/evidencias/` con el número de la prueba (ej.: `P37.png`). En Windows se sacan con `Win + Shift + S`.
3. Súbelo desde **tu cuenta**, en una rama propia:

```bash
git checkout -b pruebas-tu-nombre
git add docs/PRUEBAS.md docs/evidencias
git commit -m "Agrega resultados y capturas de las pruebas P35 a P38"
git push -u origin pruebas-tu-nombre
```

Después entra al repositorio en GitHub, presiona **"Compare & pull request"** y pide que otro integrante lo revise antes de unirlo.

> Antes de tu primer commit, configura tu nombre y **el correo de tu cuenta de GitHub**, así los commits aparecen a tu nombre:
> `git config user.name "Tu Nombre"` y `git config user.email "tu-correo-de-github@ejemplo.com"`

## Problemas comunes

| Mensaje o síntoma | Solución |
|---|---|
| `python` no se reconoce | Reinstala Python marcando *"Add Python to PATH"*, o prueba con `py` en vez de `python`. |
| `supabase_url is required` al iniciar | El `.env` no está guardado, tiene otro nombre (por ejemplo `.env.txt`) o le faltan valores. |
| "Correo o contraseña incorrectos" | Revisa que el correo esté bien escrito y pide de nuevo la contraseña. |
| "Tu cuenta no está asociada a ningún trabajador" | Alguien cambió el correo de ese trabajador en su ficha. Avísale al administrador. |
| "No se pudo conectar con Supabase" | Revisa tu internet y que `SUPABASE_URL` y `SUPABASE_KEY` estén bien copiadas. |
| `Address already in use` / puerto 5000 ocupado | Ya tienes el sistema abierto en otra terminal: ciérralo con `Ctrl + C`. |
