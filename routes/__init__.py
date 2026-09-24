from routes import auth, cargos, dashboard, departamentos, trabajadores

BLUEPRINTS = [auth.bp, dashboard.bp, trabajadores.bp, departamentos.bp, cargos.bp]
