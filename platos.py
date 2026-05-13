# ============================================================
# platos.py — Gestión de Platos Chef-Costos
# ============================================================

import sqlite3


# ============================================================
# CLASE PLATO
# ============================================================

class Plato:

    def __init__(self, nombre):

        self.nombre = nombre

    def __str__(self):

        return f"🍽️ {self.nombre}"


# ============================================================
# GESTOR DE PLATOS
# ============================================================

class GestorPlatos:

    def __init__(self, db_name):

        self.db_name = db_name

    # ========================================================
    # CREAR TABLA
    # ========================================================

    def crear_tabla(self):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS platos (

                nombre TEXT PRIMARY KEY
            )
            """)

            conn.commit()

    # ========================================================
    # CREAR PLATO
    # ========================================================

    def crear(self, nombre):

        # ====================================================
        # VALIDACIONES
        # ====================================================

        if not nombre.strip():

            return "❌ Nombre inválido"

        try:

            with sqlite3.connect(self.db_name) as conn:

                conn.execute(
                    "PRAGMA foreign_keys = ON"
                )

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO platos
                VALUES (?)
                """, (nombre,))

                conn.commit()

            return (
                "✅ Plato registrado correctamente"
            )

        except sqlite3.IntegrityError:

            return "❌ El plato ya existe"

    # ========================================================
    # LEER PLATO
    # ========================================================

    def leer(self, nombre):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT nombre
            FROM platos
            WHERE nombre = ?
            """, (nombre,))

            dato = cursor.fetchone()

            if dato:

                return Plato(
                    nombre=dato[0]
                )

            return None

    # ========================================================
    # LISTAR PLATOS
    # ========================================================

    def listar(self):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT nombre
            FROM platos
            ORDER BY nombre
            """)

            datos = cursor.fetchall()

            platos = []

            for dato in datos:

                platos.append(
                    Plato(
                        nombre=dato[0]
                    )
                )

            return platos

    # ========================================================
    # ACTUALIZAR NOMBRE
    # ========================================================

    def actualizar(self,
                    nombre_actual,
                    nuevo_nombre):

        # ====================================================
        # VALIDACIONES
        # ====================================================

        if not self.existe(nombre_actual):

            return "❌ Plato no encontrado"

        if not nuevo_nombre.strip():

            return "❌ Nuevo nombre inválido"

        try:

            with sqlite3.connect(self.db_name) as conn:

                conn.execute(
                    "PRAGMA foreign_keys = ON"
                )

                cursor = conn.cursor()

                cursor.execute("""
                UPDATE platos
                SET nombre = ?
                WHERE nombre = ?
                """, (
                    nuevo_nombre,
                    nombre_actual
                ))

                conn.commit()

            return (
                "✅ Plato actualizado correctamente"
            )

        except sqlite3.IntegrityError:

            return (
                "❌ Ya existe un plato "
                "con ese nombre"
            )

    # ========================================================
    # ELIMINAR PLATO
    # ========================================================

    def eliminar(self, nombre):

        if not self.existe(nombre):

            return "❌ Plato no encontrado"

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM platos
            WHERE nombre = ?
            """, (nombre,))

            conn.commit()

        return (
            "✅ Plato eliminado correctamente"
        )

    # ========================================================
    # VERIFICAR EXISTENCIA
    # ========================================================

    def existe(self, nombre):

        return self.leer(nombre) is not None

    # ========================================================
    # CONTAR PLATOS
    # ========================================================

    def total_platos(self):

        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM platos
            """)

            total = cursor.fetchone()[0]

            return total

    # ========================================================
    # BUSCAR PLATOS
    # ========================================================

    def buscar(self, texto):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT nombre
            FROM platos
            WHERE nombre LIKE ?
            ORDER BY nombre
            """, (f"%{texto}%",))

            datos = cursor.fetchall()

            return [
                Plato(nombre=d[0])
                for d in datos
            ]