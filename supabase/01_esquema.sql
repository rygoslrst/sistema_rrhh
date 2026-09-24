-- =====================================================================
-- TalentoRH · Esquema de la base de datos (Supabase / PostgreSQL)
-- Cómo usarlo: Supabase > SQL Editor > New query > pegar todo > Run.
-- Se puede ejecutar más de una vez sin romper nada.
-- =====================================================================

-- ---------------------------------------------------------------------
-- 1. Tablas
-- ---------------------------------------------------------------------
create table if not exists public.departamentos (
  id          bigint generated always as identity primary key,
  nombre      varchar(80)  not null unique,
  descripcion varchar(255),
  created_at  timestamptz  not null default now()
);

create table if not exists public.cargos (
  id          bigint generated always as identity primary key,
  nombre      varchar(80)  not null unique,
  descripcion varchar(255),
  sueldo_base integer      not null default 0 check (sueldo_base >= 0),
  created_at  timestamptz  not null default now()
);

create table if not exists public.trabajadores (
  id              bigint generated always as identity primary key,
  rut             varchar(12)  not null unique,          -- formato 12345678-K
  nombres         varchar(60)  not null,
  apellidos       varchar(60)  not null,
  email           varchar(120) not null unique,
  telefono        varchar(20),
  fecha_ingreso   date         not null,
  sueldo          integer      not null check (sueldo > 0),
  estado          varchar(20)  not null default 'activo'
                  check (estado in ('activo', 'vacaciones', 'licencia', 'desvinculado')),
  departamento_id bigint       not null references public.departamentos (id) on delete restrict,
  cargo_id        bigint       not null references public.cargos (id) on delete restrict,
  created_at      timestamptz  not null default now(),
  updated_at      timestamptz  not null default now()
);

-- Índices para que los filtros por departamento, cargo y estado sean rápidos
create index if not exists idx_trabajadores_departamento on public.trabajadores (departamento_id);
create index if not exists idx_trabajadores_cargo        on public.trabajadores (cargo_id);
create index if not exists idx_trabajadores_estado       on public.trabajadores (estado);

-- ---------------------------------------------------------------------
-- 2. Actualizar updated_at automáticamente al modificar un trabajador
-- ---------------------------------------------------------------------
create or replace function public.actualizar_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists trg_trabajadores_updated_at on public.trabajadores;
create trigger trg_trabajadores_updated_at
  before update on public.trabajadores
  for each row execute function public.actualizar_updated_at();

-- ---------------------------------------------------------------------
-- 3. Seguridad: Row Level Security (RLS)
--    Solo los usuarios que iniciaron sesión (rol "authenticated") pueden
--    leer y escribir. Sin sesión (rol "anon") no se ve ningún dato.
-- ---------------------------------------------------------------------
alter table public.departamentos enable row level security;
alter table public.cargos        enable row level security;
alter table public.trabajadores  enable row level security;

drop policy if exists "Autenticados gestionan departamentos" on public.departamentos;
create policy "Autenticados gestionan departamentos"
  on public.departamentos for all to authenticated
  using (true) with check (true);

drop policy if exists "Autenticados gestionan cargos" on public.cargos;
create policy "Autenticados gestionan cargos"
  on public.cargos for all to authenticated
  using (true) with check (true);

drop policy if exists "Autenticados gestionan trabajadores" on public.trabajadores;
create policy "Autenticados gestionan trabajadores"
  on public.trabajadores for all to authenticated
  using (true) with check (true);

grant select, insert, update, delete
  on public.departamentos, public.cargos, public.trabajadores
  to authenticated;
