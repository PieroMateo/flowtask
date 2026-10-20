"""Script ejecutable para crear las tablas y poblar las categorías base.

Uso:  python seed.py
"""

from app.seed import init_db

if __name__ == "__main__":
    inserted = init_db()
    print(f"Base de datos lista. Categorías nuevas insertadas: {inserted}")
