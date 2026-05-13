# ============================================================
# recetas.py — Gestión de Recetas Chef-Costos
# ============================================================

import sqlite3


# ============================================================
# CLASE RECETA
# ============================================================

class Receta:

    def __init__(self,
                 plato,
                 ingrediente,
                 cantidad):

        self.plato = plato
        self.ingrediente = ingrediente
        self.cantidad = cantidad

    def __str__(self):

        return (
            f"🍽️ Plato: {self.plato:<20} | "
            f"Ingrediente: {self.ingrediente:<20} | "
            f"Cantidad: {self.cantidad}"
        )


# ============================================================
# GESTOR DE RECETAS
# ============================================================

class GestorRecetas:

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

            conn.commit()

    # ========================================================
    # CREAR INGREDIENTE EN RECETA
    # ========================================================

    def crear(self,
              plato,
              ingrediente,
              cantidad):

        # ====================================================
        # VALIDACIONES
        # ====================================================

        if cantidad <= 0:

            return "❌ Cantidad inválida"

        if self.existe(plato, ingrediente):

            return (
                "❌ El ingrediente ya "
                "está en la receta"
            )

        try:

            with sqlite3.connect(self.db_name) as conn:

                conn.execute(
                    "PRAGMA foreign_keys = ON"
                )

                cursor = conn.cursor()

                cursor.execute("""
                INSERT INTO recetas
                (plato, ingrediente, cantidad)
                VALUES (?, ?, ?)
                """, (
                    plato,
                    ingrediente,
                    cantidad
                ))

                conn.commit()

            return (
                "✅ Ingrediente agregado "
                "a la receta"
            )

        except sqlite3.Error as e:

            return f"❌ Error: {e}"

    # ========================================================
    # LEER RECETAS DE UN PLATO
    # ========================================================

    def leer_por_plato(self, plato):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT plato,
                   ingrediente,
                   cantidad
            FROM recetas
            WHERE plato = ?
            ORDER BY ingrediente
            """, (plato,))

            datos = cursor.fetchall()

            return [Receta(*d) for d in datos]

    # ========================================================
    # LISTAR TODAS LAS RECETAS
    # ========================================================

    def listar(self):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT plato,
                   ingrediente,
                   cantidad
            FROM recetas
            ORDER BY plato
            """)

            datos = cursor.fetchall()

            return [Receta(*d) for d in datos]

    # ========================================================
    # ACTUALIZAR CANTIDAD
    # ========================================================

    def actualizar(self,
                    plato,
                    ingrediente,
                    nueva_cantidad):

        if nueva_cantidad <= 0:

            return "❌ Cantidad inválida"

        if not self.existe(plato, ingrediente):

            return (
                "❌ El ingrediente no "
                "existe en la receta"
            )

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            UPDATE recetas
            SET cantidad = ?
            WHERE plato = ?
            AND ingrediente = ?
            """, (
                nueva_cantidad,
                plato,
                ingrediente
            ))

            conn.commit()

        return (
            "✅ Cantidad actualizada "
            "correctamente"
        )

    # ========================================================
    # ELIMINAR INGREDIENTE DE RECETA
    # ========================================================

    def eliminar(self,
                 plato,
                 ingrediente):

        if not self.existe(plato, ingrediente):

            return (
                "❌ El ingrediente no "
                "existe en la receta"
            )

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM recetas
            WHERE plato = ?
            AND ingrediente = ?
            """, (
                plato,
                ingrediente
            ))

            conn.commit()

        return (
            "✅ Ingrediente eliminado "
            "de la receta"
        )

    # ========================================================
    # ELIMINAR RECETA COMPLETA
    # ========================================================

    def eliminar_receta_completa(self, plato):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            DELETE FROM recetas
            WHERE plato = ?
            """, (plato,))

            conn.commit()

        return (
            "✅ Receta eliminada correctamente"
        )

    # ========================================================
    # VERIFICAR EXISTENCIA
    # ========================================================

    def existe(self,
               plato,
               ingrediente):

        with sqlite3.connect(self.db_name) as conn:

            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            cursor = conn.cursor()

            cursor.execute("""
            SELECT *
            FROM recetas
            WHERE plato = ?
            AND ingrediente = ?
            """, (
                plato,
                ingrediente
            ))

            dato = cursor.fetchone()

            return dato is not None

    # ========================================================
    # CALCULAR COSTO TOTAL DEL PLATO
    # ========================================================

    def calcular_costo_plato(self,
                             plato,
                             gestor_ingredientes):

        recetas = self.leer_por_plato(plato)

        total = 0

        for receta in recetas:

            ingrediente = gestor_ingredientes.leer(
                receta.ingrediente
            )

            if ingrediente:

                subtotal = (
                    ingrediente.precio_mercado
                    * receta.cantidad
                )

                total += subtotal

        return total

    # ========================================================
    # CALCULAR PRECIO SUGERIDO
    # ========================================================

    def precio_sugerido(self,
                        plato,
                        gestor_ingredientes,
                        margen=35):

        costo = self.calcular_costo_plato(
            plato,
            gestor_ingredientes
        )

        return costo * (1 + margen / 100)

    # ========================================================
    # REPORTE DETALLADO DEL PLATO
    # ========================================================

    def detalle_plato(self,
                      plato,
                      gestor_ingredientes):

        recetas = self.leer_por_plato(plato)

        if not recetas:

            print("❌ No existe receta")
            return

        print("\n" + "=" * 60)
        print(f"📋 RECETA — {plato}")
        print("=" * 60)

        total = 0

        for receta in recetas:

            ingrediente = gestor_ingredientes.leer(
                receta.ingrediente
            )

            if ingrediente:

                subtotal = (
                    ingrediente.precio_mercado
                    * receta.cantidad
                )

                total += subtotal

                print(
                    f"{receta.ingrediente:<25} "
                    f"Cantidad: {receta.cantidad:<8} "
                    f"Costo: ${subtotal:,.0f}"
                )

        print("-" * 60)
        print(f"💰 COSTO TOTAL: ${total:,.0f}")

    # ========================================================
    # CONTAR RECETAS
    # ========================================================

    def total_recetas(self):

        with sqlite3.connect(self.db_name) as conn:

            cursor = conn.cursor()

            cursor.execute("""
            SELECT COUNT(*)
            FROM recetas
            """)

            total = cursor.fetchone()[0]

            return total