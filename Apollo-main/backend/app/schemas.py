from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AvisoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    icone: str
    data: str
    titulo: str


class DisciplinaOut(BaseModel):
    nome: str
    professor: str
    iniciais: str
    corAvatar: str | None
    media: str
    statusMedia: str
    faltas: int
    statusFaltas: str
    frequencia: str
    statusFrequencia: str
    progresso: int
    corProgresso: str | None = None


class TarefaOut(BaseModel):
    id: int
    disciplina: str
    status: str
    descricao: str
    dataLabel: str


class TarefaStatusIn(BaseModel):
    status: str


class EventoOut(BaseModel):
    cor: str
    hora: str
    nome: str


class EventoCalendarioOut(BaseModel):
    dia: int
    mes: int
    ano: int


class NotaLinhaOut(BaseModel):
    disciplina: str
    corDot: str
    professor: str
    faltas: int
    statusFaltas: str
    av1: str
    av2: str
    av3: str
    total: str
    statusValores: str
    statusTotal: str
    statusAv1: str | None = None
    statusAv2: str | None = None
    statusAv3: str | None = None


class ProgressoItemOut(BaseModel):
    nome: str
    pct: int
    cor: str | None = None


class TipoMaterial(BaseModel):
    icone: str
    label: str


class BadgeMaterial(BaseModel):
    texto: str
    bg: str
    cor: str


class MaterialBibliotecaOut(BaseModel):
    id: int
    sigla: str
    gradiente: list[str]
    subtitulo: str
    nome: str
    professor: str
    badge: BadgeMaterial
    tipos: list[TipoMaterial]
    favorito: bool


class FavoritoIn(BaseModel):
    favorito: bool


class ContatoOut(BaseModel):
    id: str
    iniciais: str
    corBg: str | None = None
    corTexto: str | None = None
    nome: str
    info: str
    hora: str
    ativo: bool


class MensagemOut(BaseModel):
    direcao: str
    texto: str
    hora: str


class MensagemIn(BaseModel):
    texto: str


class UsuarioOut(BaseModel):
    nome: str
    papel: str
    iniciais: str


class LoginIn(BaseModel):
    email: str
    senha: str


class LoginOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut


class RecuperarSenhaIn(BaseModel):
    email: str


class MensagemGenericaOut(BaseModel):
    mensagem: str
