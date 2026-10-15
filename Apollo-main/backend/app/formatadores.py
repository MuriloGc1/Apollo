from datetime import datetime, timedelta

MESES_ABREV = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
DIAS_SEMANA_ABREV = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]


def data_hora_curta(dt: datetime) -> str:
    return f"{dt.strftime('%d/%m/%y')} {dt.strftime('%H:%M')}"


def data_curta(dt: datetime) -> str:
    return dt.strftime("%d/%m/%y")


def hora(dt: datetime) -> str:
    return dt.strftime("%H:%M")


def data_evento_proximo(dt: datetime) -> str:
    return f"{dt.day} {MESES_ABREV[dt.month - 1]} — {dt.strftime('%H:%M')}"


def hora_relativa(dt: datetime, agora: datetime) -> str:
    diferenca_dias = (agora.date() - dt.date()).days
    if diferenca_dias == 0:
        return hora(dt)
    if diferenca_dias == 1:
        return "Ontem"
    if diferenca_dias < 7:
        return DIAS_SEMANA_ABREV[int(dt.strftime("%w"))]
    return data_curta(dt)
