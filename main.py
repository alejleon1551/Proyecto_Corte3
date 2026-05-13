#  Estudiantes: Alejandra León, Samuel Simancas, Daniel Camacho
# ============================================================
# main.py — Sistema Chef-Costos
# ============================================================

from database import (
    crear_base_datos,
    DB_NAME
)

from ingredientes import GestorIngredientes
from platos import GestorPlatos
from recetas import GestorRecetas
from alertas import GestorAlertas
from reportes import GestorReportes


# ============================================================
# CONFIGURACIÓN
# ============================================================

CONFIG = {

    "umbral_inflacion": 20,
    "margen_venta": 35,
    "restaurante": "Chef-Costos",
    "moneda": "COP"
}


# ============================================================
# DATOS INICIALES
# ============================================================

INGREDIENTES_INICIALES = {

    "Pechuga de pollo": {
        "historico": 12000,
        "mercado": 15500,
        "unidad": "kg"
    },

    "Arroz blanco": {
        "historico": 2500,
        "mercado": 3200,
        "unidad": "kg"
    },

    "Aceite vegetal": {
        "historico": 8000,
        "mercado": 11000,
        "unidad": "litro"
    },

    "Papa criolla": {
        "historico": 1800,
        "mercado": 2100,
        "unidad": "kg"
    }
}


PLATOS_INICIALES = {

    "Bandeja Paisa": {

        "Arroz blanco": 0.2,
        "Pechuga de pollo": 0.25,
        "Aceite vegetal": 0.05
    },

    "Ajiaco": {

        "Papa criolla": 0.3,
        "Pechuga de pollo": 0.2
    }
}


# ============================================================
# INICIALIZAR SISTEMA
# ============================================================

def inicializar_sistema():

    crear_base_datos()

    gi = GestorIngredientes(DB_NAME)
    gp = GestorPlatos(DB_NAME)
    grc = GestorRecetas(DB_NAME)

    gi.crear_tabla()
    gp.crear_tabla()
    grc.crear_tabla()

    # ========================================================
    # CARGAR INGREDIENTES
    # ========================================================

    gi.cargar_datos_iniciales(
        INGREDIENTES_INICIALES
    )

    # ========================================================
    # CARGAR PLATOS Y RECETAS
    # ========================================================

    for plato, receta in PLATOS_INICIALES.items():

        if not gp.existe(plato):

            gp.crear(plato)

            for ingrediente, cantidad in receta.items():

                grc.crear(
                    plato,
                    ingrediente,
                    cantidad
                )

    ga = GestorAlertas(
        CONFIG["umbral_inflacion"]
    )

    gr = GestorReportes(
        CONFIG["restaurante"],
        CONFIG["margen_venta"],
        CONFIG["moneda"],
        CONFIG["umbral_inflacion"]
    )

    return gi, gp, grc, ga, gr


# ============================================================
# VALIDAR NÚMEROS
# ============================================================

def pedir_float(mensaje):

    while True:

        try:

            valor = float(
                input(mensaje)
                .replace(",", ".")
            )

            if valor <= 0:

                print(
                    "❌ Debe ser mayor a cero"
                )

                continue

            return valor

        except ValueError:

            print("❌ Número inválido")


# ============================================================
# MENÚ INGREDIENTES
# ============================================================

def menu_ingredientes(gi):

    while True:

        print("\n" + "=" * 60)
        print("🥬 GESTIÓN DE INGREDIENTES")
        print("=" * 60)

        print("1. Listar")
        print("2. Crear")
        print("3. Actualizar")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        # ====================================================
        # LISTAR
        # ====================================================

        if opcion == "1":

            ingredientes = gi.listar()

            if not ingredientes:

                print("❌ No hay ingredientes")
                continue

            for ingrediente in ingredientes:

                print(ingrediente)

        # ====================================================
        # CREAR
        # ====================================================

        elif opcion == "2":

            nombre = input(
                "Nombre: "
            ).strip()

            historico = pedir_float(
                "Precio histórico: "
            )

            mercado = pedir_float(
                "Precio mercado: "
            )

            unidad = input(
                "Unidad: "
            ).strip()

            print(

                gi.crear(
                    nombre,
                    historico,
                    mercado,
                    unidad
                )
            )

        # ====================================================
        # ACTUALIZAR
        # ====================================================

        elif opcion == "3":

            nombre = input(
                "Ingrediente: "
            ).strip()

            historico = pedir_float(
                "Nuevo histórico: "
            )

            mercado = pedir_float(
                "Nuevo mercado: "
            )

            unidad = input(
                "Unidad: "
            ).strip()

            print(

                gi.actualizar(
                    nombre,
                    historico,
                    mercado,
                    unidad
                )
            )

        # ====================================================
        # ELIMINAR
        # ====================================================

        elif opcion == "4":

            nombre = input(
                "Ingrediente: "
            ).strip()

            print(
                gi.eliminar(nombre)
            )

        elif opcion == "0":

            break

        else:

            print("❌ Opción inválida")


# ============================================================
# MENÚ PLATOS
# ============================================================

def menu_platos(gp, grc, gi):

    while True:

        print("\n" + "=" * 60)
        print("🍽️ GESTIÓN DE PLATOS")
        print("=" * 60)

        print("1. Listar")
        print("2. Crear")
        print("3. Ver receta")
        print("4. Eliminar")
        print("0. Volver")

        opcion = input("Opción: ")

        # ====================================================
        # LISTAR
        # ====================================================

        if opcion == "1":

            platos = gp.listar()

            if not platos:

                print("❌ No hay platos")
                continue

            for plato in platos:

                costo = grc.calcular_costo_plato(
                    plato.nombre,
                    gi
                )

                venta = grc.precio_sugerido(
                    plato.nombre,
                    gi
                )

                print(
                    f"{plato.nombre:<25}"
                    f"Costo: ${costo:,.0f} | "
                    f"Venta: ${venta:,.0f}"
                )

        # ====================================================
        # CREAR
        # ====================================================

        elif opcion == "2":

            nombre = input(
                "Nombre plato: "
            ).strip()

            resultado = gp.crear(nombre)

            print(resultado)

            if "❌" in resultado:

                continue

            while True:

                ingrediente = input(
                    "Ingrediente "
                    "(fin para terminar): "
                ).strip()

                if ingrediente.lower() == "fin":

                    break

                if not gi.existe(ingrediente):

                    print(
                        "❌ Ingrediente no existe"
                    )

                    continue

                cantidad = pedir_float(
                    "Cantidad: "
                )

                print(

                    grc.crear(
                        nombre,
                        ingrediente,
                        cantidad
                    )
                )

        # ====================================================
        # VER RECETA
        # ====================================================

        elif opcion == "3":

            plato = input(
                "Nombre plato: "
            ).strip()

            recetas = grc.leer_por_plato(plato)

            if not recetas:

                print("❌ No hay receta")
                continue

            for receta in recetas:

                print(receta)

        # ====================================================
        # ELIMINAR
        # ====================================================

        elif opcion == "4":

            nombre = input(
                "Plato: "
            ).strip()

            print(
                gp.eliminar(nombre)
            )

        elif opcion == "0":

            break

        else:

            print("❌ Opción inválida")


# ============================================================
# MENÚ REPORTES
# ============================================================

def menu_reportes(gr, gp, gi, grc):

    while True:

        print("\n" + "=" * 60)
        print("📊 REPORTES")
        print("=" * 60)

        print("1. Inflación")
        print("2. Platos")
        print("3. Detalle plato")
        print("4. Resumen")
        print("5. Ingredientes alerta")
        print("6. Reporte financiero")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":

            gr.reporte_inflacion(gi)

        elif opcion == "2":

            gr.reporte_platos(
                gp,
                gi,
                grc
            )

        elif opcion == "3":

            plato = input(
                "Nombre plato: "
            ).strip()

            gr.detalle_plato(
                plato,
                gp,
                gi,
                grc
            )

        elif opcion == "4":

            gr.resumen_general(
                gi,
                gp,
                grc
            )

        elif opcion == "5":

            gr.ingredientes_alerta(gi)

        elif opcion == "6":

            gr.reporte_financiero(
                gp,
                gi,
                grc
            )

        elif opcion == "0":

            break

        else:

            print("❌ Opción inválida")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def menu_principal():

    gi, gp, grc, ga, gr = (
        inicializar_sistema()
    )

    while True:

        print("\n" + "=" * 60)
        print("🍴 CHEF-COSTOS")
        print("=" * 60)

        print("1. Ingredientes")
        print("2. Platos")
        print("3. Reportes")
        print("4. Analizar alertas")
        print("5. Historial alertas")
        print("0. Salir")

        opcion = input("Opción: ")

        # ====================================================
        # INGREDIENTES
        # ====================================================

        if opcion == "1":

            menu_ingredientes(gi)

        # ====================================================
        # PLATOS
        # ====================================================

        elif opcion == "2":

            menu_platos(
                gp,
                grc,
                gi
            )

        # ====================================================
        # REPORTES
        # ====================================================

        elif opcion == "3":

            menu_reportes(
                gr,
                gp,
                gi,
                grc
            )

        # ====================================================
        # ALERTAS
        # ====================================================

        elif opcion == "4":

            alertas = ga.analizar(gi)

            ga.mostrar_alertas(alertas)

        elif opcion == "5":

            ga.mostrar_historial()

        # ====================================================
        # SALIR
        # ====================================================

        elif opcion == "0":

            print("👋 Hasta pronto")
            break

        else:

            print("❌ Opción inválida")


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

if __name__ == "__main__":

    menu_principal()