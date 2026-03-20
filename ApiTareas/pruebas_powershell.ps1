# ================================================================
# PRUEBAS DE LA API DE TAREAS — PowerShell (Invoke-RestMethod)
# ================================================================
# Inicia la API primero:  python app.py
# Luego abre un segundo terminal y ejecuta los comandos de abajo.

# ----------------------------------------------------------------
# CREATE — POST /tareas
# ----------------------------------------------------------------

# Crear tarea 1
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo": "Estudiar Flask", "descripcion": "Repasar rutas y SQLite", "estado": "pendiente"}'

# Crear tarea 2 (estado por default = pendiente)
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo": "Hacer ejercicio", "descripcion": "30 minutos de cardio"}'

# Crear tarea 3
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo": "Leer documentacion", "descripcion": "Docs de SQLite", "estado": "en progreso"}'

# ----------------------------------------------------------------
# READ — GET /tareas
# ----------------------------------------------------------------

# Consultar todas las tareas
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method GET

# Filtrar solo las pendientes
Invoke-RestMethod -Uri "http://localhost:5000/tareas?estado=pendiente" -Method GET

# Filtrar solo las completadas
Invoke-RestMethod -Uri "http://localhost:5000/tareas?estado=completada" -Method GET

# ----------------------------------------------------------------
# UPDATE — PUT /tareas/<id>
# ----------------------------------------------------------------

# Actualizar solo el estado de la tarea con id=1
Invoke-RestMethod -Uri "http://localhost:5000/tareas/1" -Method PUT `
  -ContentType "application/json" `
  -Body '{"estado": "completada"}'

# Actualizar título, descripción y estado de la tarea con id=2
Invoke-RestMethod -Uri "http://localhost:5000/tareas/2" -Method PUT `
  -ContentType "application/json" `
  -Body '{"titulo": "Correr 5km", "descripcion": "Ruta del parque", "estado": "en progreso"}'

# ----------------------------------------------------------------
# DELETE — DELETE /tareas/<id>
# ----------------------------------------------------------------

# Eliminar la tarea con id=3
Invoke-RestMethod -Uri "http://localhost:5000/tareas/3" -Method DELETE

# Intentar eliminar una tarea que no existe (debe devolver 404)
Invoke-RestMethod -Uri "http://localhost:5000/tareas/999" -Method DELETE

# ================================================================
# RESPUESTAS ESPERADAS
# ================================================================
#
# POST exitoso    → HTTP 201, { "mensaje": "Tarea creada...", "tarea": {...} }
# GET exitoso     → HTTP 200, { "total": N, "tareas": [...] }
# PUT exitoso     → HTTP 200, { "mensaje": "Tarea actualizada...", "tarea": {...} }
# DELETE exitoso  → HTTP 200, { "mensaje": "Tarea con id=3 eliminada...", "eliminada": {...} }
# ID no encontrado→ HTTP 404, { "error": "No existe una tarea con id=..." }
# Campo faltante  → HTTP 400, { "error": "El campo '...' es requerido" }
# Estado inválido → HTTP 400, { "error": "Estado inválido", "validos": [...] }
