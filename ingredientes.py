# ============================================================
# ingredientes.py — Gestión de Ingredientes Chef-Costos
# ============================================================

import sqlite3


# ============================================================
# CLASE INGREDIENTE
# ============================================================

class Ingrediente:

    def __init__(self,
                 nombre,
                 precio_historico,
                 precio_mercado,
                 unidad):

        self.nombre = nombre
        self.precio_historico = precio_historico
        self.precio_mercado = precio_mercado
        self.unidad = unidad

    # ========================================================
    # CALCULAR INFLACIÓN
    # ========================================================

    def calcular_inflacion(self):

        if self.precio_historico <= 0:

            return 0

        return (
            (
                self.precio_mercado
                - self.precio_historico
            )
            / self.precio_historico
        ) * 100

    # ========================================================
    # VALIDAR ALERTA
    # ========================================================

    def tiene_alerta(self, umbral=20):

        return (
            self.calcular_inflacion()
            > umbral
        )

    # ========================================================
    # REPRESENTACIÓN
    # ========================================================

    def __str__(self):

        return (
            f"{self.nombre:<25} | "
            f"Histórico: ${self.precio_historico:,.0f} | "
            f"Mercado: ${self.precio_mercado:,.0f} | "
            f"Unidad: {self.unidad}"
        )


# ============================================================
# GESTOR DE INGREDIENTES
# ============================================================

class GestorIngredientes:

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
            CREATE TABLE IF NOT EXISTS ingredientes (

                nombre TEXT PRIMARY KEY,

                historico REAL NOT NULL,

                mercado REAL NOT NULL,

                unidad TEXT NOT NULL
            )
            """)

            conn.commit()

    # ========================================================
    # CREAR INGREDIENTE
    # ========================================================

    def crear(self,
              nombre,
              historico,
              mercado,
              unidad):

        # ====================================================
        # VALIDACIONES
        # ====================================================

        if not nombre.strip():

            return "❌ Nombre inválido"

        if historico <= 0 or mercado <= 0:

            return (
                "❌ Los precios deben "
                "ser mayores a cero"
            )

        try:

            with sqlite3.connect(self.db_name) as conn:

                conn.execute(
                    "PRAGMA foreign_keys = ON"
                )

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO ingredientes
                VALUES (?, ?, ?, ?)
                """, (
                    nombre,
                    historico,
                    mercado,
                    unidad
                ))

                conn.commit()

            return (
                "✅ Ingrediente "
                "registrado correctamente"
            )

        except sqlite3.IntegrityError:

            return "❌ El ingrediente ya existe"

    # ========================================================
    # LEER INGREDIENTE
    # ========================================================

    def leer(self, nombre):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM ingredientes
            WHERE nombre = ?
            """, (nombre,))

            dato = cursor.fetchone()

            if dato:

                return Ingrediente(
                    nombre=dato[0],
                    precio_historico=dato[1],
                    precio_mercado=dato[2],
                    unidad=dato[3]
                )

            return None

    # ========================================================
    # LISTAR INGREDIENTES
    # ========================================================

    def listar(self):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM ingredientes
            ORDER BY nombre
            """)

            datos = cursor.fetchall()

            ingredientes = []

            for dato in datos:

                ingredientes.append(

                    Ingrediente(
                        nombre=dato[0],
                        precio_historico=dato[1],
                        precio_mercado=dato[2],
                        unidad=dato[3]
                    )
                )

            return ingredientes

    # ========================================================
    # ACTUALIZAR INGREDIENTE
    # ========================================================

    def actualizar(self,
                    nombre,
                    historico=None,
                    mercado=None,
                    unidad=None):

        ingrediente = self.leer(nombre)

        if not ingrediente:

            return "❌ Ingrediente no encontrado"

        historico = (
            historico
            if historico is not None
            else ingrediente.precio_historico
        )

        mercado = (
            mercado
            if mercado is not None
            else ingrediente.precio_mercado
        )

        unidad = (
            unidad
            if unidad is not None
            else ingrediente.unidad
        )

        if historico <= 0 or mercado <= 0:

            return (
                "❌ Los precios deben "
                "ser mayores a cero"
            )

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE ingredientes
            SET historico = ?,
                mercado = ?,
                unidad = ?
            WHERE nombre = ?
            """, (
                historico,
                mercado,
                unidad,
                nombre
            ))

            conn.commit()

        return (
            "✅ Ingrediente "
            "actualizado correctamente"
        )

    # ========================================================
    # ELIMINAR INGREDIENTE
    # ========================================================

    def eliminar(self, nombre):

        if not self.existe(nombre):

            return "❌ Ingrediente no encontrado"

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM ingredientes
            WHERE nombre = ?
            """, (nombre,))

            conn.commit()

        return (
            "✅ Ingrediente "
            "eliminado correctamente"
        )

    # ========================================================
    # VERIFICAR EXISTENCIA
    # ========================================================

    def existe(self, nombre):

        return self.leer(nombre) is not None

    # ========================================================
    # CARGAR DATOS INICIALES
    # ========================================================

    def cargar_datos_iniciales(self, datos):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM ingredientes
            """)

            total = cursor.fetchone()[0]

            if total == 0:

                for nombre, info in datos.items():

                    cursor.execute("""
                    INSERT INTO ingredientes
                    VALUES (?, ?, ?, ?)
                    """, (
                        nombre,
                        info["historico"],
                        info["mercado"],
                        info["unidad"]
                    ))

                conn.commit()

    # ========================================================
    # CONTAR INGREDIENTES
    # ========================================================

    def total_ingredientes(self):

        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM ingredientes
            """)

            return cursor.fetchone()[0]