-- =====================================================================
-- TalentoRH · Base de datos en Supabase
-- Cómo usarlo: Supabase > SQL Editor > New query > pegar todo > Run
-- Se puede ejecutar más de una vez sin duplicar datos.
-- =====================================================================

-- 1. Tabla -------------------------------------------------------------
create table if not exists public.trabajadores (
  id            bigint generated always as identity primary key,
  rut           varchar(12)  not null unique,       -- formato 12345678-K
  nombre        varchar(60)  not null,
  apellido      varchar(60)  not null,
  correo        varchar(120) not null unique,
  telefono      varchar(20),
  departamento  varchar(40)  not null,              -- lista fija en trabajador.py
  cargo         varchar(40)  not null,              -- lista fija en trabajador.py
  fecha_ingreso date         not null,
  sueldo        integer      not null check (sueldo > 0),
  estado        varchar(20)  not null default 'activo'
                check (estado in ('activo', 'vacaciones', 'licencia', 'desvinculado')),
  created_at    timestamptz  not null default now()
);

-- 2. Permisos: la aplicación Flask usa la tabla con la clave pública de Supabase
alter table public.trabajadores disable row level security;
grant select, insert, update, delete on public.trabajadores to anon;

-- 3. Datos de prueba 100 % FICTICIOS ---------------------------------------
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
  ('18456012-7', 'Catalina',  'Navarro Jara',     'catalina.navarro@losandes-demo.cl',  '+56 9 5123 4412', 'Recursos Humanos', 'Jefe de área',             '2021-05-10', 1600000, 'licencia')
on conflict (rut) do nothing;
