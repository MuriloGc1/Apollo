NOTA_BOA = 7.0
NOTA_ATENCAO = 5.0

FALTAS_OK = 3
FALTAS_ATENCAO = 8

FREQUENCIA_BOA = 90
FREQUENCIA_ATENCAO = 75


def status_nota_disciplina(valor: float) -> str:
    if valor >= NOTA_BOA:
        return "green"
    if valor >= NOTA_ATENCAO:
        return "yellow"
    return "orange"


def status_nota_boletim(valor: float) -> str:
    if valor >= NOTA_BOA:
        return "green"
    if valor >= NOTA_ATENCAO:
        return "yellow"
    return "red"


def status_faltas_disciplina(faltas: int) -> str:
    if faltas <= FALTAS_OK:
        return "green"
    if faltas <= FALTAS_ATENCAO:
        return "yellow"
    return "orange"


def status_faltas_boletim(faltas: int) -> str:
    if faltas <= FALTAS_OK:
        return "green"
    if faltas <= FALTAS_ATENCAO:
        return "yellow"
    return "red"


def status_frequencia(pct: float) -> str:
    if pct >= FREQUENCIA_BOA:
        return "green"
    if pct >= FREQUENCIA_ATENCAO:
        return "yellow"
    return "orange"


def status_tarefa(entregue_em, prazo, agora) -> str:
    if entregue_em is not None:
        return "entregue"
    if prazo < agora:
        return "expirado"
    return "pendente"
