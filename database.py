# ============================================================
# database.py — Configuración SQLite Chef-Costos
# ============================================================

import sqlite3
import os


# ============================================================
# NOMBRE BASE DE DATOS
# ============================================================

DB_NAME = "chef_costos.db"


# ============================================================
# CREAR BASE DE DATOS
# ============================================================

def crear_base_datos():

    # ========================================================
    # CREAR ARCHIVO SI NO EXISTE
    # ========================================================

    if not os.path.exists(DB_NAME):

        conexion = sqlite3.connect(DB_NAME)

        conexion.execute(
            "PRAGMA foreign_keys = ON"
        )

        cursor = conexion.cursor()

        # ====================================================
        # TABLA INGREDIENTES
        # ====================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes (

            nombre TEXT PRIMARY KEY,

            historico REAL NOT NULL,

            mercado REAL NOT NULL,

            unidad TEXT NOT NULL
        )
        """)

        # ====================================================
        # TABLA PLATOS
        # ====================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS platos (

            nombre TEXT PRIMARY KEY
        )
        """)

        # ====================================================
        # TABLA RECETAS
        # ====================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recetas (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            plato TEXT NOT NULL,

            ingrediente TEXT NOT NULL,

            cantidad REAL NOT NULL,

            UNIQUE(plato, ingrediente),

            FOREIGN KEY (plato)
                REFERENCES platos(nombre)
                ON DELETE CASCADE
                ON UPDATE CASCADE,

            FOREIGN KEY (ingrediente)
                REFERENCES ingredientes(nombre)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        )
        """)

        conexion.commit()
        conexion.close()

        print("✅ Base de datos creada correctamente")

    else:

        print("✅ Base de datos conectada")