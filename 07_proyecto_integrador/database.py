"""
==============================================================================
Módulo: 07_proyecto_integrador / database.py
Tema: Conexión y Configuración del ORM MySQL con SQLAlchemy 2.0 y PyMySQL.
==============================================================================
"""

import os
import sys
from contextlib import contextmanager
from typing import Generator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

try:
    from dotenv import load_dotenv
    # Cargar variables de entorno desde .env si existe en el proyecto
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    pass

# ==============================================================================
# CONFIGURACIÓN DE PARÁMETROS DE CONEXIÓN
# ==============================================================================
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "tienda_poo")

# URL de conexión SQLAlchemy para MySQL utilizando el driver PyMySQL
_credenciales = f"{DB_USER}:{quote_plus(DB_PASSWORD)}" if DB_PASSWORD else DB_USER
DATABASE_URL = f"mysql+pymysql://{_credenciales}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# Motor SQLAlchemy con pre-ping para evitar conexiones caídas y reciclaje de hilos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Fábrica de sesiones de trabajo (Unit of Work)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ==============================================================================
# BASE DECLARATIVA MODERNA (SQLAlchemy 2.0)
# ==============================================================================
class Base(DeclarativeBase):
    """Clase base de la cual heredarán todas las entidades mapeadas (ORM)."""
    pass


# ==============================================================================
# GESTOR DE CONTEXTO DE SESIÓN (PATRÓN CONTEXT MANAGER)
# ==============================================================================
@contextmanager
def obtener_sesion() -> Generator[Session, None, None]:
    """
    Gestor de contexto para transacciones atómicas.
    Aplica commit automáticamente si todo sale bien, o rollback en caso de error.
    """
    sesion = SessionLocal()
    try:
        yield sesion
        sesion.commit()
    except Exception:
        sesion.rollback()
        raise
    finally:
        sesion.close()


# ==============================================================================
# UTILIDAD DE INICIALIZACIÓN DE ESQUEMA Y TABLAS
# ==============================================================================
def asegurar_base_de_datos_mysql():
    """Crea la base de datos en el servidor MySQL si aún no existe."""
    import pymysql
    conexion = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
    finally:
        conexion.close()


def inicializar_base_datos(crear_bd: bool = True):
    """
    Garantiza que la base de datos exista y crea todas las tablas mapeadas
    registradas en Base.metadata.
    """
    if crear_bd and "mysql" in DATABASE_URL:
        try:
            asegurar_base_de_datos_mysql()
        except Exception as err:
            print(f"⚠️ [DB INIT]: No se pudo verificar la creación de BD: {err}")

    # Importar los modelos ORM para que Base.metadata conozca sus tablas
    try:
        from . import modelos_orm  # noqa: F401
    except (ImportError, ValueError):
        import modelos_orm  # noqa: F401

    Base.metadata.create_all(bind=engine)
    print(f"🗄️ [DB INIT]: Tablas creadas/verificadas con éxito en '{DB_NAME}'.")
