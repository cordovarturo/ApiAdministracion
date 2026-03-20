# API de Tareas — CRUD completo con Flask + SQLite

Proyecto de práctica para implementar un CRUD completo
(Create, Read, Update, Delete) con Flask y SQLite.

## Archivos

```
api_tareas/
├── app.py                 ← API principal
├── poblar_db.py           ← Inserta datos de ejemplo
├── pruebas_powershell.ps1 ← Comandos para probar en PowerShell
└── tareas.db              ← Se crea automáticamente
```

## Instalación y arranque

```powershell
pip install flask
python app.py
```

## Endpoints

| Método | Ruta              | Acción          | Código éxito |
|--------|-------------------|-----------------|--------------|
| POST   | /tareas           | Crear tarea     | 201 Created  |
| GET    | /tareas           | Consultar todas | 200 OK       |
| PUT    | /tareas/\<id\>    | Actualizar      | 200 OK       |
| DELETE | /tareas/\<id\>    | Eliminar        | 200 OK       |

## Estados válidos de una tarea

- `pendiente` (valor por defecto al crear)
- `en progreso`
- `completada`

## Ejemplos rápidos en PowerShell

```powershell
# Crear
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method POST `
  -ContentType "application/json" `
  -Body '{"titulo": "Mi tarea", "descripcion": "Descripcion aqui", "estado": "pendiente"}'

# Consultar todas
Invoke-RestMethod -Uri "http://localhost:5000/tareas" -Method GET

# Filtrar por estado
Invoke-RestMethod -Uri "http://localhost:5000/tareas?estado=pendiente" -Method GET

# Actualizar solo el estado
Invoke-RestMethod -Uri "http://localhost:5000/tareas/1" -Method PUT `
  -ContentType "application/json" `
  -Body '{"estado": "completada"}'

# Eliminar
Invoke-RestMethod -Uri "http://localhost:5000/tareas/1" -Method DELETE
```

## Conceptos nuevos respecto al ejercicio anterior

| Concepto | Descripción |
|---|---|
| `PUT` con `<int:id>` | Parámetro de ruta — Flask extrae el id de la URL automáticamente |
| `DELETE` con `<int:id>` | Igual, pero elimina el registro |
| Verificar existencia | Antes de UPDATE o DELETE, hacer un SELECT para confirmar que el id existe |
| Actualización parcial | Si el campo no llega en el body, se usa el valor actual de la BD |
| Código 404 | Se devuelve cuando el recurso solicitado no existe |
| Filtros con `request.args` | `?estado=pendiente` se lee con `request.args.get("estado")` |
