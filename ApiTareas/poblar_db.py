"""
poblar_db.py  —  Inserta tareas de ejemplo para probar la API.
Ejecutar UNA vez después de iniciar app.py por primera vez.

Uso:
    python poblar_db.py
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tareas.db")

tareas_ejemplo = [
    ("Estudiar Flask",        "Repasar rutas, blueprints y contexto",   "pendiente"),
    ("Hacer ejercicio",       "30 minutos de cardio en la mañana",       "completada"),
    ("Leer documentación",    "Leer docs de SQLite y sqlite3 de Python", "en progreso"),
    ("Entregar proyecto",     "Subir código al repositorio de la clase", "pendiente"),
    ("Comprar despensa",      "Leche, huevos, pan y fruta",             "completada"),
]

def main():
    if not os.path.exists(DB_PATH):
        print("ERROR: La BD no existe. Ejecuta primero 'python app.py'.")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.executemany(
        "INSERT INTO tareas (titulo, descripcion, estado) VALUES (?, ?, ?)",
        tareas_ejemplo
    )
    conn.commit()
    total = conn.execute("SELECT COUNT(*) FROM tareas").fetchone()[0]
    conn.close()

    print(f"Insertadas {len(tareas_ejemplo)} tareas de ejemplo.")
    print(f"Total en la BD: {total}")

if __name__ == "__main__":
    main()
