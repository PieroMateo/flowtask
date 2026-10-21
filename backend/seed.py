"""script ejecutable para crear las tablas y poblar las categorías base.
uso:  python seed.py
"""
#trae la funcion del otro archivo para crear las tablas y tener datos en la bd
from app.seed import init_db

if __name__ == "__main__":
    inserted = init_db()
    print(f"Base de datos lista. Categorías nuevas insertadas: {inserted}")
