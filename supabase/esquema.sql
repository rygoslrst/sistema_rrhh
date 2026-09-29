-- =====================================================================
-- TalentoRH · Base de datos en Supabase
-- Cómo usarlo: Supabase > SQL Editor > New query > pegar todo > Run
-- Se puede ejecutar más de una vez sin duplicar datos.
-- =====================================================================

-- 1. Tabla trabajadores -------------------------------------------------
create table if not exists public.trabajadores (
  id            bigint generated always as identity primary key,
  rut           varchar(12)  not null unique,       -- formato 12345678-K
  nombre        varchar(60)  not null,
  apellido      varchar(60)  not null,
  correo        varchar(120) not null unique,       -- el mismo de su cuenta para entrar
  telefono      varchar(20),
  departamento  varchar(40)  not null,              -- lista fija en trabajador.py
  cargo         varchar(40)  not null,              -- lista fija en trabajador.py
  fecha_ingreso date         not null,
  sueldo        integer      not null check (sueldo > 0),
  estado        varchar(20)  not null default 'activo'
                check (estado in ('activo', 'vacaciones', 'licencia', 'desvinculado')),
  created_at    timestamptz  not null default now()
);

-- Rol dentro del sistema:
--   'admin' ve y cambia todo, 'asistente' ve todo y solo corrige datos básicos,
--   'empleado' solo ve "Mi panel"
alter table public.trabajadores
  add column if not exists rol varchar(20) not null default 'empleado';
alter table public.trabajadores drop constraint if exists trabajadores_rol_check;
alter table public.trabajadores
  add constraint trabajadores_rol_check check (rol in ('admin', 'asistente', 'empleado'));

-- 2. Tabla solicitudes (vacaciones, permisos y licencias) ------------------
create table if not exists public.solicitudes (
  id            bigint generated always as identity primary key,
  trabajador_id bigint       not null references public.trabajadores (id) on delete cascade,
  tipo          varchar(20)  not null check (tipo in ('vacaciones', 'permiso', 'licencia')),
  fecha_inicio  date         not null,
  fecha_fin     date         not null,
  motivo        varchar(255),
  estado        varchar(20)  not null default 'pendiente'
                check (estado in ('pendiente', 'aprobada', 'rechazada')),
  created_at    timestamptz  not null default now(),
  check (fecha_fin >= fecha_inicio)
);

-- Índice para la relación solicitudes -> trabajadores: acelera "Mi panel"
-- (solicitudes de un trabajador). Supabase lo recomienda para toda clave foránea.
create index if not exists solicitudes_trabajador_id_idx on public.solicitudes (trabajador_id);

-- 3. Permisos: la aplicación Flask usa las tablas con la clave pública de Supabase
alter table public.trabajadores disable row level security;
alter table public.solicitudes disable row level security;
grant select, insert, update, delete on public.trabajadores, public.solicitudes to anon;

-- 4. Datos de prueba 100 % FICTICIOS ---------------------------------------
insert into public.trabajadores
  (rut, nombre, apellido, correo, telefono, departamento, cargo, fecha_ingreso, sueldo, estado)
values
  ('15482731-5', 'Camila',    'Rojas Fuentes',    'camila.rojas@losandes-demo.cl',      '+56 9 5123 4401', 'Administración',   'Gerente',                  '2017-03-06', 2950000, 'activo'),
  ('17234908-0', 'Matías',    'Soto Carrasco',    'matias.soto@losandes-demo.cl',       '+56 9 5123 4402', 'Administración',   'Analista',                 '2019-08-19', 1200000, 'activo'),
  ('19876543-0', 'Valentina', 'Muñoz Pizarro',    'valentina.munoz@losandes-demo.cl',   '+56 9 5123 4403', 'Administración',   'Asistente administrativo', '2023-01-09',  740000, 'vacaciones'),
  ('12650384-9', 'Jorge',     'Castillo Vera',    'jorge.castillo@losandes-demo.cl',    '+56 9 5123 4404', 'Operaciones',      'Jefe de área',             '2016-05-02', 1750000, 'activo'),
  ('16345027-5', 'Francisca', 'Díaz Morales',     'francisca.diaz@losandes-demo.cl',    '+56 9 5123 4405', 'Operaciones',      'Operario',                 '2021-10-11',  680000, 'activo'),
  ('20114873-1', 'Benjamín',  'Reyes Tapia',      'benjamin.reyes@losandes-demo.cl',    '+56 9 5123 4406', 'Operaciones',      'Operario',                 '2024-02-26',  650000, 'licencia'),
  ('13901256-9', 'Rodrigo',   'Fuentealba Núñez', 'rodrigo.fuentealba@losandes-demo.cl','+56 9 5123 4407', 'Ventas',           'Jefe de área',             '2018-11-05', 1800000, 'activo'),
  ('21045678-3', 'Antonia',   'Vargas Leiva',     'antonia.vargas@losandes-demo.cl',    '+56 9 5123 4408', 'Ventas',           'Ejecutivo de ventas',      '2025-04-14',  920000, 'activo'),
  ('14567290-2', 'Paula',     'Espinoza Araya',   'paula.espinoza@losandes-demo.cl',    '+56 9 5123 4409', 'Ventas',           'Ejecutivo de ventas',      '2015-09-01',  950000, 'desvinculado'),
  ('19234806-4', 'Tomás',     'Gutiérrez Bravo',  'tomas.gutierrez@losandes-demo.cl',   '+56 9 5123 4410', 'Tecnología',       'Técnico de soporte',       '2022-06-20', 1050000, 'activo'),
  ('22150349-K', 'Martín',    'Álvarez Cortés',   'martin.alvarez@losandes-demo.cl',    '+56 9 5123 4411', 'Tecnología',       'Analista',                 '2026-03-02', 1300000, 'activo'),
  ('18456012-7', 'Catalina',  'Navarro Jara',     'rrhh@losandes-demo.cl',              '+56 9 5123 4412', 'Recursos Humanos', 'Jefe de área',             '2021-05-10', 1600000, 'activo'),
  ('11873465-3', 'Sebastián', 'Pérez Lagos',      'sebastian.perez@losandes-demo.cl',   '+56 9 5123 4413', 'Recursos Humanos', 'Asistente administrativo', '2020-03-16',  850000, 'activo')
on conflict (rut) do nothing;

-- Catalina Navarro (jefa de RR.HH.) es la administradora: usa la cuenta rrhh@losandes-demo.cl
update public.trabajadores
set rol = 'admin', correo = 'rrhh@losandes-demo.cl', estado = 'activo'
where rut = '18456012-7';

-- Sebastián Pérez (asistente de RR.HH.) puede ver todo, pero solo corrige datos básicos
update public.trabajadores set rol = 'asistente' where rut = '11873465-3';

-- Solicitudes de ejemplo (solo se cargan si la tabla está vacía)
insert into public.solicitudes (trabajador_id, tipo, fecha_inicio, fecha_fin, motivo, estado)
select t.id, s.tipo, s.inicio::date, s.fin::date, s.motivo, s.estado
from (values
  ('17234908-0', 'vacaciones', '2026-10-05', '2026-10-09', 'Viaje familiar',          'pendiente'),
  ('16345027-5', 'permiso',    '2026-10-01', '2026-10-01', 'Trámite personal',        'pendiente'),
  ('21045678-3', 'vacaciones', '2026-11-16', '2026-11-27', 'Vacaciones de verano',    'pendiente'),
  ('19234806-4', 'licencia',   '2026-09-14', '2026-09-18', 'Reposo por gripe',        'aprobada'),
  ('12650384-9', 'permiso',    '2026-09-10', '2026-09-10', 'Hora médica',             'rechazada')
) as s (rut, tipo, inicio, fin, motivo, estado)
join public.trabajadores t on t.rut = s.rut
where not exists (select 1 from public.solicitudes);
