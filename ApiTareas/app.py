from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "tareas.db")

ESTADOS_VALIDOS = ["pendiente", "en progreso", "completada"]

# ------------------------------------------------------------------
# Base de datos
# ------------------------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT    NOT NULL,
            descripcion TEXT    NOT NULL,
            estado      TEXT    NOT NULL DEFAULT 'pendiente'
        )
    """)
    conn.commit()
    conn.close()


# ------------------------------------------------------------------
# CREATE — POST /tareas
# ------------------------------------------------------------------

@app.route("/tareas", methods=["POST"])
def crear_tarea():
    """
    Crea una nueva tarea.

    Body JSON:
        {
            "titulo":      "Estudiar Flask",
            "descripcion": "Repasar rutas y SQLite",
            "estado":      "pendiente"   <-- opcional, default: pendiente
        }
    """
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "Se requiere un body JSON"}), 400

    # Validar campos requeridos
    for campo in ["titulo", "descripcion"]:
        if campo not in datos or not str(datos[campo]).strip():
            return jsonify({"error": f"El campo '{campo}' es requerido y no puede estar vacío"}), 400

    titulo      = datos["titulo"].strip()
    descripcion = datos["descripcion"].strip()
    estado      = datos.get("estado", "pendiente").strip().lower()

    if estado not in ESTADOS_VALIDOS:
        return jsonify({
            "error":   f"Estado inválido: '{estado}'",
            "validos": ESTADOS_VALIDOS
        }), 400

    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO tareas (titulo, descripcion, estado) VALUES (?, ?, ?)",
        (titulo, descripcion, estado)
    )
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "mensaje": "Tarea creada correctamente",
        "tarea": {
            "id":          nuevo_id,
            "titulo":      titulo,
            "descripcion": descripcion,
            "estado":      estado
        }
    }), 201


# ------------------------------------------------------------------
# READ — GET /tareas
# ------------------------------------------------------------------

@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    """
    Devuelve todas las tareas.
    Filtros opcionales por query params:
        GET /tareas?estado=pendiente
        GET /tareas?estado=completada
    """
    estado_filtro = request.args.get("estado")

    conn = get_db_connection()

    if estado_filtro:
        if estado_filtro.lower() not in ESTADOS_VALIDOS:
            conn.close()
            return jsonify({
                "error":   f"Estado de filtro inválido: '{estado_filtro}'",
                "validos": ESTADOS_VALIDOS
            }), 400
        filas = conn.execute(
            "SELECT * FROM tareas WHERE estado = ?", (estado_filtro.lower(),)
        ).fetchall()
    else:
        filas = conn.execute("SELECT * FROM tareas").fetchall()

    conn.close()

    tareas = [dict(fila) for fila in filas]
    return jsonify({"total": len(tareas), "tareas": tareas}), 200


# ------------------------------------------------------------------
# UPDATE — PUT /tareas/<id>
# ------------------------------------------------------------------

@app.route("/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    """
    Actualiza una tarea existente (parcial o total).

    Body JSON (todos los campos son opcionales):
        {
            "titulo":      "Nuevo título",
            "descripcion": "Nueva descripción",
            "estado":      "en progreso"
        }
    """
    conn = get_db_connection()

    # Verificar que la tarea existe
    tarea = conn.execute(
        "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
    ).fetchone()

    if tarea is None:
        conn.close()
        return jsonify({"error": f"No existe una tarea con id={tarea_id}"}), 404

    datos = request.get_json()
    if not datos:
        conn.close()
        return jsonify({"error": "Se requiere un body JSON con los campos a actualizar"}), 400

    # Tomar valores actuales y sobreescribir solo los que llegaron
    titulo      = datos.get("titulo",      tarea["titulo"]).strip()
    descripcion = datos.get("descripcion", tarea["descripcion"]).strip()
    estado      = datos.get("estado",      tarea["estado"]).strip().lower()

    if not titulo or not descripcion:
        conn.close()
        return jsonify({"error": "titulo y descripcion no pueden quedar vacíos"}), 400

    if estado not in ESTADOS_VALIDOS:
        conn.close()
        return jsonify({
            "error":   f"Estado inválido: '{estado}'",
            "validos": ESTADOS_VALIDOS
        }), 400

    conn.execute(
        "UPDATE tareas SET titulo = ?, descripcion = ?, estado = ? WHERE id = ?",
        (titulo, descripcion, estado, tarea_id)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Tarea actualizada correctamente",
        "tarea": {
            "id":          tarea_id,
            "titulo":      titulo,
            "descripcion": descripcion,
            "estado":      estado
        }
    }), 200


# ------------------------------------------------------------------
# DELETE — DELETE /tareas/<id>
# ------------------------------------------------------------------

@app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    """
    Elimina una tarea por su ID.
    """
    conn = get_db_connection()

    # Verificar que existe antes de borrar
    tarea = conn.execute(
        "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
    ).fetchone()

    if tarea is None:
        conn.close()
        return jsonify({"error": f"No existe una tarea con id={tarea_id}"}), 404

    conn.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "mensaje":    f"Tarea con id={tarea_id} eliminada correctamente",
        "eliminada":  dict(tarea)
    }), 200


# ------------------------------------------------------------------
# Arranque
# ------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Base de datos lista en:", DB_PATH)
    app.run(debug=True, port=5000)
