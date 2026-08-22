# ============================================================
# gunicorn.conf.py - CONFIGURACIÓN DE PRODUCCIÓN
# ============================================================
# Se usa junto con --preload: la app (y su db.create_all()) se
# importa una sola vez en el proceso maestro, antes de bifurcar
# los workers. post_fork descarta esa conexión heredada para que
# cada worker abra su propia conexión nueva a PostgreSQL.


def post_fork(server, worker):
    from app import app
    from models import db

    with app.app_context():
        db.engine.dispose()
