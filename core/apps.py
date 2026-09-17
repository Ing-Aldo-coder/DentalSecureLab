from django.apps import AppConfig
from django.db.backends.signals import connection_created
from django.dispatch import receiver


def configure_sqlite_pragmas(sender, connection, **kwargs):
    """
    Optimiza SQLite para soportar la concurrencia clínica de 4 consultorios y recepción.
    Activa el modo WAL (Write-Ahead Logging) y un timeout de espera de 5000 ms.
    """
    if connection.vendor == 'sqlite':
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA journal_mode=WAL;')
            cursor.execute('PRAGMA busy_timeout=5000;')
            cursor.execute('PRAGMA synchronous=NORMAL;')


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        connection_created.connect(configure_sqlite_pragmas)
