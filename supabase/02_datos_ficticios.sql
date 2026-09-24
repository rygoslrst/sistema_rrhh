-- =====================================================================
-- TalentoRH · Datos de prueba 100 % FICTICIOS
-- Empresa inventada: "Comercial Los Andes SpA".
-- Ejecutar DESPUÉS de 01_esquema.sql (SQL Editor > New query > Run).
-- =====================================================================

insert into public.departamentos (nombre, descripcion) values
  ('Administración y Finanzas', 'Contabilidad, pagos a proveedores y control presupuestario.'),
  ('Operaciones',               'Bodega, logística y despacho de pedidos.'),
  ('Ventas',                    'Atención de clientes y ejecutivos comerciales.'),
  ('Tecnología',                'Soporte computacional y desarrollo de sistemas internos.'),
  ('Recursos Humanos',          'Selección, contratos, remuneraciones y bienestar.')
on conflict (nombre) do nothing;

insert into public.cargos (nombre, descripcion, sueldo_base) values
  ('Gerente de Área',            'Dirige un departamento y responde por sus resultados.', 2800000),
  ('Jefe de Equipo',             'Coordina el trabajo diario de un grupo de personas.',   1650000),
  ('Analista',                   'Procesa información y elabora reportes.',               1150000),
  ('Desarrollador de Software',  'Construye y mantiene los sistemas internos.',           1400000),
  ('Ejecutivo de Ventas',        'Gestiona cartera de clientes y cotizaciones.',           900000),
  ('Asistente Administrativo',   'Apoyo en documentación y trámites internos.',            720000),
  ('Operario de Bodega',         'Recepción, almacenamiento y despacho de productos.',     650000),
  ('Encargado de Remuneraciones','Calcula sueldos, imposiciones y finiquitos.',           1250000)
on conflict (nombre) do nothing;

-- Los departamentos y cargos se buscan por nombre para no depender de los id.
insert into public.trabajadores
  (rut, nombres, apellidos, email, telefono, fecha_ingreso, sueldo, estado, departamento_id, cargo_id)
select t.rut, t.nombres, t.apellidos, t.email, t.telefono, t.fecha_ingreso::date, t.sueldo, t.estado,
       d.id, c.id
from (values
  ('15482731-5', 'Camila Andrea',   'Rojas Fuentes',    'camila.rojas@losandes-demo.cl',     '+56 9 5123 4401', '2017-03-06', 2950000, 'activo',       'Administración y Finanzas', 'Gerente de Área'),
  ('17234908-0', 'Matías Ignacio',  'Soto Carrasco',    'matias.soto@losandes-demo.cl',      '+56 9 5123 4402', '2019-08-19', 1200000, 'activo',       'Administración y Finanzas', 'Analista'),
  ('19876543-0', 'Valentina',       'Muñoz Pizarro',    'valentina.munoz@losandes-demo.cl',  '+56 9 5123 4403', '2023-01-09',  740000, 'vacaciones',   'Administración y Finanzas', 'Asistente Administrativo'),
  ('12650384-9', 'Jorge Andrés',    'Castillo Vera',    'jorge.castillo@losandes-demo.cl',   '+56 9 5123 4404', '2016-05-02', 1750000, 'activo',       'Operaciones',               'Jefe de Equipo'),
  ('16345027-5', 'Francisca',       'Díaz Morales',     'francisca.diaz@losandes-demo.cl',   '+56 9 5123 4405', '2021-10-11',  680000, 'activo',       'Operaciones',               'Operario de Bodega'),
  ('20114873-1', 'Benjamín',        'Reyes Tapia',      'benjamin.reyes@losandes-demo.cl',   '+56 9 5123 4406', '2024-02-26',  650000, 'licencia',     'Operaciones',               'Operario de Bodega'),
  ('18762390-1', 'Ignacia Paz',     'Herrera Salinas',  'ignacia.herrera@losandes-demo.cl',  '+56 9 5123 4407', '2020-07-13',  660000, 'activo',       'Operaciones',               'Operario de Bodega'),
  ('13901256-9', 'Rodrigo',         'Fuentealba Núñez', 'rodrigo.fuentealba@losandes-demo.cl','+56 9 5123 4408', '2018-11-05', 2700000, 'activo',       'Ventas',                    'Gerente de Área'),
  ('21045678-3', 'Antonia',         'Vargas Leiva',     'antonia.vargas@losandes-demo.cl',   '+56 9 5123 4409', '2025-04-14',  920000, 'activo',       'Ventas',                    'Ejecutivo de Ventas'),
  ('17890123-0', 'Diego Alonso',    'Contreras Silva',  'diego.contreras@losandes-demo.cl',  '+56 9 5123 4410', '2019-03-18',  980000, 'vacaciones',   'Ventas',                    'Ejecutivo de Ventas'),
  ('14567290-2', 'Paula',           'Espinoza Araya',   'paula.espinoza@losandes-demo.cl',   '+56 9 5123 4411', '2015-09-01',  950000, 'desvinculado', 'Ventas',                    'Ejecutivo de Ventas'),
  ('19234806-4', 'Tomás',           'Gutiérrez Bravo',  'tomas.gutierrez@losandes-demo.cl',  '+56 9 5123 4412', '2022-06-20', 1450000, 'activo',       'Tecnología',                'Desarrollador de Software'),
  ('16023477-6', 'Josefa',          'Sepúlveda Ortiz',  'josefa.sepulveda@losandes-demo.cl', '+56 9 5123 4413', '2020-01-27', 1700000, 'activo',       'Tecnología',                'Jefe de Equipo'),
  ('22150349-K', 'Martín',          'Álvarez Cortés',   'martin.alvarez@losandes-demo.cl',   '+56 9 5123 4414', '2026-03-02', 1400000, 'activo',       'Tecnología',                'Desarrollador de Software'),
  ('18456012-7', 'Catalina',        'Navarro Jara',     'catalina.navarro@losandes-demo.cl', '+56 9 5123 4415', '2021-05-10', 1300000, 'licencia',     'Recursos Humanos',          'Encargado de Remuneraciones'),
  ('11873465-3', 'Sebastián',       'Pérez Lagos',      'sebastian.perez@losandes-demo.cl',  '+56 9 5123 4416', '2014-08-04', 1180000, 'activo',       'Recursos Humanos',          'Analista')
) as t (rut, nombres, apellidos, email, telefono, fecha_ingreso, sueldo, estado, departamento, cargo)
join public.departamentos d on d.nombre = t.departamento
join public.cargos c        on c.nombre = t.cargo
on conflict (rut) do nothing;
