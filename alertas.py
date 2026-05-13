# ============================================================
# alertas.py — Sistema de Alertas Chef-Costos
# ============================================================

from datetime import datetime


# ============================================================
# CLASE ALERTA
# ============================================================

class Alerta:

    def __init__(self,
                 ingrediente,
                 inflacion,
                 umbral):

        self.ingrediente = ingrediente
        self.inflacion = inflacion
        self.umbral = umbral

        self.fecha = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

    def __str__(self):

        return (
            f"⚠️ [{self.fecha}] "
            f"{self.ingrediente:<25} "
            f"Inflación: {self.inflacion:.1f}%"
        )


# ============================================================
# GESTOR DE ALERTAS
# ============================================================

class GestorAlertas:

    def __init__(self, umbral=20):

        self.umbral = umbral
        self.historial = []

    # ========================================================
    # ANALIZAR INFLACIÓN
    # ========================================================

    def analizar(self, gestor_ingredientes):

        alertas = []

        ingredientes = gestor_ingredientes.listar()

        for ingrediente in ingredientes:

            inflacion = (
                ingrediente.calcular_inflacion()
            )

            if inflacion > self.umbral:

                alerta = Alerta(
                    ingrediente=ingrediente.nombre,
                    inflacion=inflacion,
                    umbral=self.umbral
                )

                alertas.append(alerta)

                # ============================================
                # EVITAR DUPLICADOS EN HISTORIAL
                # ============================================

                existe = False

                for alerta_guardada in self.historial:

                    if (
                        alerta_guardada.ingrediente
                        == alerta.ingrediente
                    ):

                        existe = True
                        break

                if not existe:

                    self.historial.append(alerta)

        return alertas

    # ========================================================
    # MOSTRAR ALERTAS
    # ========================================================

    def mostrar_alertas(self, alertas):

        print("\n" + "=" * 60)
        print("🚨 ALERTAS DE INFLACIÓN")
        print("=" * 60)

        if not alertas:

            print("✅ No hay alertas activas")
            return

        for alerta in alertas:

            print(alerta)

    # ========================================================
    # MOSTRAR HISTORIAL
    # ========================================================

    def mostrar_historial(self):

        print("\n" + "=" * 60)
        print("📋 HISTORIAL DE ALERTAS")
        print("=" * 60)

        if not self.historial:

            print("❌ No hay alertas registradas")
            return

        for alerta in self.historial:

            print(alerta)

    # ========================================================
    # CONTAR ALERTAS
    # ========================================================

    def total_alertas(self):

        return len(self.historial)

    # ========================================================
    # LIMPIAR HISTORIAL
    # ========================================================

    def limpiar_historial(self):

        self.historial.clear()

        return (
            "✅ Historial de alertas eliminado"
        )

    # ========================================================
    # EXISTEN ALERTAS
    # ========================================================

    def hay_alertas(self):

        return len(self.historial) > 0