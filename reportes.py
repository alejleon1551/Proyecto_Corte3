# ============================================================
# reportes.py — Reportes Chef-Costos
# ============================================================

from datetime import datetime


# ============================================================
# GESTOR DE REPORTES
# ============================================================

class GestorReportes:

    def __init__(self,
                 nombre_restaurante,
                 margen=35,
                 moneda="COP"):

        self.restaurante = nombre_restaurante
        self.margen = margen
        self.moneda = moneda

    # ========================================================
    # ENCABEZADO
    # ========================================================

    def encabezado(self, titulo):

        print("\n" + "=" * 70)

        print(f"🍴 {self.restaurante}")
        print(titulo)

        print(
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

        print("=" * 70)

    # ========================================================
    # REPORTE DE INFLACIÓN
    # ========================================================

    def reporte_inflacion(self,
                          gestor_ingredientes):

        self.encabezado(
            "📈 REPORTE DE INFLACIÓN"
        )

        ingredientes = gestor_ingredientes.listar()

        if not ingredientes:

            print("❌ No hay ingredientes")
            return

        for ingrediente in ingredientes:

            inflacion = (
                ingrediente.calcular_inflacion()
            )

            estado = (
                "⚠️ ALERTA"
                if inflacion > 20
                else "✅ OK"
            )

            print(
                f"{ingrediente.nombre:<25} "
                f"{inflacion:>8.1f}% "
                f"{estado}"
            )

    # ========================================================
    # REPORTE DE PLATOS
    # ========================================================

    def reporte_platos(self,
                       gestor_platos,
                       gestor_ingredientes,
                       gestor_recetas):

        self.encabezado(
            "🍽️ REPORTE DE PLATOS"
        )

        platos = gestor_platos.listar()

        if not platos:

            print("❌ No hay platos")
            return

        for plato in platos:

            costo = (
                gestor_recetas.calcular_costo_plato(
                    plato.nombre,
                    gestor_ingredientes
                )
            )

            venta = (
                gestor_recetas.precio_sugerido(
                    plato.nombre,
                    gestor_ingredientes,
                    self.margen
                )
            )

            utilidad = venta - costo

            print(
                f"{plato.nombre:<25} "
                f"Costo: ${costo:,.0f} | "
                f"Venta: ${venta:,.0f} | "
                f"Ganancia: ${utilidad:,.0f}"
            )

    # ========================================================
    # DETALLE DE PLATO
    # ========================================================

    def detalle_plato(self,
                      nombre_plato,
                      gestor_platos,
                      gestor_ingredientes,
                      gestor_recetas):

        plato = gestor_platos.leer(
            nombre_plato
        )

        if not plato:

            print("❌ Plato no encontrado")
            return

        recetas = (
            gestor_recetas.leer_por_plato(
                nombre_plato
            )
        )

        if not recetas:

            print("❌ El plato no tiene receta")
            return

        self.encabezado(
            f"📋 DETALLE — {nombre_plato}"
        )

        total = 0

        for receta in recetas:

            ingrediente = (
                gestor_ingredientes.leer(
                    receta.ingrediente
                )
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
                    f"Subtotal: ${subtotal:,.0f}"
                )

        venta = (
            total
            * (1 + self.margen / 100)
        )

        utilidad = venta - total

        print("-" * 70)

        print(
            f"💰 COSTO TOTAL: "
            f"${total:,.0f}"
        )

        print(
            f"🏷️ PRECIO SUGERIDO: "
            f"${venta:,.0f}"
        )

        print(
            f"📈 GANANCIA ESTIMADA: "
            f"${utilidad:,.0f}"
        )

    # ========================================================
    # RESUMEN GENERAL
    # ========================================================

    def resumen_general(self,
                        gestor_ingredientes,
                        gestor_platos,
                        gestor_recetas):

        self.encabezado(
            "📊 RESUMEN GENERAL"
        )

        total_ingredientes = len(
            gestor_ingredientes.listar()
        )

        total_platos = len(
            gestor_platos.listar()
        )

        total_recetas = (
            gestor_recetas.total_recetas()
        )

        print(
            f"🥬 Ingredientes registrados: "
            f"{total_ingredientes}"
        )

        print(
            f"🍽️ Platos registrados: "
            f"{total_platos}"
        )

        print(
            f"📋 Registros en recetas: "
            f"{total_recetas}"
        )

    # ========================================================
    # INGREDIENTES CON ALERTA
    # ========================================================

    def ingredientes_alerta(self,
                            gestor_ingredientes,
                            umbral=20):

        self.encabezado(
            "🚨 INGREDIENTES EN ALERTA"
        )

        ingredientes = gestor_ingredientes.listar()

        encontrados = False

        for ingrediente in ingredientes:

            inflacion = (
                ingrediente.calcular_inflacion()
            )

            if inflacion > umbral:

                encontrados = True

                print(
                    f"{ingrediente.nombre:<25} "
                    f"{inflacion:>8.1f}%"
                )

        if not encontrados:

            print(
                "✅ No hay ingredientes "
                "con inflación crítica"
            )# ============================================================
# reportes.py — Reportes Chef-Costos
# ============================================================

from datetime import datetime


# ============================================================
# GESTOR DE REPORTES
# ============================================================

class GestorReportes:

    def __init__(self,
                 nombre_restaurante,
                 margen=35,
                 moneda="COP",
                 umbral=20):

        self.restaurante = nombre_restaurante
        self.margen = margen
        self.moneda = moneda
        self.umbral = umbral

    # ========================================================
    # ENCABEZADO
    # ========================================================

    def encabezado(self, titulo):

        print("\n" + "=" * 70)

        print(f"🍴 {self.restaurante}")
        print(titulo)

        print(
            datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        )

        print("=" * 70)

    # ========================================================
    # REPORTE DE INFLACIÓN
    # ========================================================

    def reporte_inflacion(self,
                          gestor_ingredientes):

        self.encabezado(
            "📈 REPORTE DE INFLACIÓN"
        )

        ingredientes = (
            gestor_ingredientes.listar()
        )

        if not ingredientes:

            print("❌ No hay ingredientes")
            return

        for ingrediente in ingredientes:

            inflacion = (
                ingrediente.calcular_inflacion()
            )

            estado = (
                "⚠️ ALERTA"
                if inflacion > self.umbral
                else "✅ OK"
            )

            print(
                f"{ingrediente.nombre:<25} "
                f"{inflacion:>8.1f}% "
                f"{estado}"
            )

    # ========================================================
    # REPORTE DE PLATOS
    # ========================================================

    def reporte_platos(self,
                       gestor_platos,
                       gestor_ingredientes,
                       gestor_recetas):

        self.encabezado(
            "🍽️ REPORTE DE PLATOS"
        )

        platos = gestor_platos.listar()

        if not platos:

            print("❌ No hay platos")
            return

        for plato in platos:

            costo = (
                gestor_recetas.calcular_costo_plato(
                    plato.nombre,
                    gestor_ingredientes
                )
            )

            venta = (
                gestor_recetas.precio_sugerido(
                    plato.nombre,
                    gestor_ingredientes,
                    self.margen
                )
            )

            utilidad = venta - costo

            print(
                f"{plato.nombre:<25} "
                f"Costo: ${costo:,.0f} | "
                f"Venta: ${venta:,.0f} | "
                f"Ganancia: ${utilidad:,.0f}"
            )

    # ========================================================
    # DETALLE DE PLATO
    # ========================================================

    def detalle_plato(self,
                      nombre_plato,
                      gestor_platos,
                      gestor_ingredientes,
                      gestor_recetas):

        plato = gestor_platos.leer(
            nombre_plato
        )

        if not plato:

            print("❌ Plato no encontrado")
            return

        recetas = (
            gestor_recetas.leer_por_plato(
                nombre_plato
            )
        )

        if not recetas:

            print(
                "❌ El plato no tiene receta"
            )

            return

        self.encabezado(
            f"📋 DETALLE — {nombre_plato}"
        )

        total = 0

        for receta in recetas:

            ingrediente = (
                gestor_ingredientes.leer(
                    receta.ingrediente
                )
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
                    f"Subtotal: ${subtotal:,.0f}"
                )

        venta = (
            total
            * (1 + self.margen / 100)
        )

        utilidad = venta - total

        print("-" * 70)

        print(
            f"💰 COSTO TOTAL: "
            f"${total:,.0f}"
        )

        print(
            f"🏷️ PRECIO SUGERIDO: "
            f"${venta:,.0f}"
        )

        print(
            f"📈 GANANCIA ESTIMADA: "
            f"${utilidad:,.0f}"
        )

    # ========================================================
    # RESUMEN GENERAL
    # ========================================================

    def resumen_general(self,
                        gestor_ingredientes,
                        gestor_platos,
                        gestor_recetas):

        self.encabezado(
            "📊 RESUMEN GENERAL"
        )

        total_ingredientes = (
            gestor_ingredientes.total_ingredientes()
        )

        total_platos = (
            gestor_platos.total_platos()
        )

        total_recetas = (
            gestor_recetas.total_recetas()
        )

        print(
            f"🥬 Ingredientes registrados: "
            f"{total_ingredientes}"
        )

        print(
            f"🍽️ Platos registrados: "
            f"{total_platos}"
        )

        print(
            f"📋 Registros en recetas: "
            f"{total_recetas}"
        )

    # ========================================================
    # INGREDIENTES CON ALERTA
    # ========================================================

    def ingredientes_alerta(self,
                            gestor_ingredientes):

        self.encabezado(
            "🚨 INGREDIENTES EN ALERTA"
        )

        ingredientes = (
            gestor_ingredientes.listar()
        )

        encontrados = False

        for ingrediente in ingredientes:

            inflacion = (
                ingrediente.calcular_inflacion()
            )

            if inflacion > self.umbral:

                encontrados = True

                print(
                    f"{ingrediente.nombre:<25} "
                    f"{inflacion:>8.1f}%"
                )

        if not encontrados:

            print(
                "✅ No hay ingredientes "
                "con inflación crítica"
            )

    # ========================================================
    # REPORTE FINANCIERO SIMPLE
    # ========================================================

    def reporte_financiero(self,
                           gestor_platos,
                           gestor_ingredientes,
                           gestor_recetas):

        self.encabezado(
            "💵 REPORTE FINANCIERO"
        )

        platos = gestor_platos.listar()

        if not platos:

            print("❌ No hay platos")
            return

        costo_total = 0
        venta_total = 0

        for plato in platos:

            costo = (
                gestor_recetas.calcular_costo_plato(
                    plato.nombre,
                    gestor_ingredientes
                )
            )

            venta = (
                gestor_recetas.precio_sugerido(
                    plato.nombre,
                    gestor_ingredientes,
                    self.margen
                )
            )

            costo_total += costo
            venta_total += venta

        utilidad_total = (
            venta_total - costo_total
        )

        print(
            f"💰 Costos acumulados: "
            f"${costo_total:,.0f}"
        )

        print(
            f"🏷️ Ventas proyectadas: "
            f"${venta_total:,.0f}"
        )

        print(
            f"📈 Ganancia potencial: "
            f"${utilidad_total:,.0f}"
        )