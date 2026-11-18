"""Regras de negocio do ECLSS (Environmental Control and Life Support System)."""

OXIGENIO_KG_POR_ASTRONAUTA_DIA = 0.84
AGUA_L_POR_ASTRONAUTA_DIA = 3.0
TAXAS_EMERGENCIA = {1: 1.0, 2: 1.5, 3: 2.0}  # nivel -> multiplicador de consumo
LIMITE_AUTONOMIA_CRITICA_DIAS = 7
COTA_EXTRA_NORMAL_KG = 100.0
COTA_EXTRA_RACIONAMENTO_KG = 25.0


class OxigenioInsuficienteError(Exception):
    """Estoque de oxigenio nao atende a quantidade solicitada."""


class NivelEmergenciaInvalidoError(ValueError):
    """Nivel de emergencia fora de 1..3."""


class CotaExcedidaError(Exception):
    """Solicitacao ultrapassa a cota de racionamento vigente."""


class GerenciadorRecursosMarte:
    def __init__(self, oxigenio_kg, agua_l, telemetria, astronautas=4):
        if oxigenio_kg < 0 or agua_l < 0 or astronautas <= 0:
            raise ValueError("Parametros iniciais invalidos")
        self.oxigenio_kg = oxigenio_kg
        self.agua_l = agua_l
        self.astronautas = astronautas
        self.telemetria = telemetria

    # --- calculos ---------------------------------------------------------
    def taxa_emergencia(self, nivel):
        if nivel not in TAXAS_EMERGENCIA:
            raise NivelEmergenciaInvalidoError(f"Nivel de emergencia invalido: {nivel}")
        return TAXAS_EMERGENCIA[nivel]

    def consumo_diario_oxigenio(self, nivel_emergencia=1, astronautas=None):
        n = self.astronautas if astronautas is None else astronautas
        return n * OXIGENIO_KG_POR_ASTRONAUTA_DIA * self.taxa_emergencia(nivel_emergencia)

    def consumo_diario_agua(self, nivel_emergencia=1, astronautas=None):
        n = self.astronautas if astronautas is None else astronautas
        return n * AGUA_L_POR_ASTRONAUTA_DIA * self.taxa_emergencia(nivel_emergencia)

    def autonomia_oxigenio_dias(self, nivel_emergencia=1):
        return self.oxigenio_kg / self.consumo_diario_oxigenio(nivel_emergencia)

    def em_racionamento(self):
        return self.autonomia_oxigenio_dias() < LIMITE_AUTONOMIA_CRITICA_DIAS

    def cota_extra_atual(self):
        return COTA_EXTRA_RACIONAMENTO_KG if self.em_racionamento() else COTA_EXTRA_NORMAL_KG

    # --- operacoes --------------------------------------------------------
    def verificar_estoque(self):
        """Dispara alerta de crise na telemetria se a autonomia for critica."""
        if self.em_racionamento():
            dias = self.autonomia_oxigenio_dias()
            self.telemetria.disparar_alerta("CRITICO", f"Autonomia de oxigenio critica: {dias:.1f} dias")
            return True
        return False

    def solicitar_cota_extra(self, astronauta, quantidade_kg):
        if quantidade_kg <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if quantidade_kg > self.oxigenio_kg:
            raise OxigenioInsuficienteError(
                f"Solicitado {quantidade_kg} kg, disponivel {self.oxigenio_kg} kg"
            )
        if quantidade_kg > self.cota_extra_atual():
            raise CotaExcedidaError(f"Limite da cota: {self.cota_extra_atual()} kg")
        self.oxigenio_kg -= quantidade_kg
        self.verificar_estoque()
        return {"astronauta": astronauta, "aprovado_kg": quantidade_kg, "estoque_kg": self.oxigenio_kg}

    def enviar_status(self):
        return self.telemetria.enviar_relatorio(
            {"oxigenio_kg": self.oxigenio_kg, "agua_l": self.agua_l, "astronautas": self.astronautas}
        )
