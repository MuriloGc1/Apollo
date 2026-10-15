from datetime import datetime, date
import enum

from sqlalchemy import ForeignKey, String, Enum as SAEnum, DateTime, Date, Numeric, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Papel(str, enum.Enum):
    aluno = "aluno"
    professor = "professor"
    responsavel = "responsavel"


class TipoConversa(str, enum.Enum):
    individual = "individual"
    grupo = "grupo"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    papel: Mapped[Papel] = mapped_column(SAEnum(Papel), default=Papel.aluno)
    iniciais: Mapped[str] = mapped_column(String(4))
    cor_avatar: Mapped[str | None] = mapped_column(String(20), nullable=True)


class Materia(Base):
    __tablename__ = "materias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(80), unique=True)
    cor: Mapped[str] = mapped_column(String(20), default="#3b82f6")


class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (UniqueConstraint("aluno_id", "materia_id", name="uq_aluno_materia"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    frequencia_percentual: Mapped[float] = mapped_column(Numeric(5, 1), default=100)
    progresso_percentual: Mapped[int] = mapped_column(default=0)
    cor_progresso: Mapped[str | None] = mapped_column(String(20), nullable=True)

    aluno: Mapped["Usuario"] = relationship(foreign_keys=[aluno_id])
    materia: Mapped["Materia"] = relationship()
    professor: Mapped["Usuario"] = relationship(foreign_keys=[professor_id])
    notas: Mapped[list["Nota"]] = relationship(back_populates="matricula", order_by="Nota.bimestre")


class Nota(Base):
    __tablename__ = "notas"
    __table_args__ = (UniqueConstraint("matricula_id", "bimestre", name="uq_matricula_bimestre"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula_id: Mapped[int] = mapped_column(ForeignKey("matriculas.id"))
    bimestre: Mapped[int] = mapped_column(default=1)
    faltas: Mapped[int] = mapped_column(default=0)
    av1: Mapped[float] = mapped_column(Numeric(3, 1))
    av2: Mapped[float] = mapped_column(Numeric(3, 1))
    av3: Mapped[float] = mapped_column(Numeric(3, 1))

    matricula: Mapped["Matricula"] = relationship(back_populates="notas")


class MaterialBiblioteca(Base):
    __tablename__ = "materiais_biblioteca"

    id: Mapped[int] = mapped_column(primary_key=True)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    sigla: Mapped[str] = mapped_column(String(6))
    cor_gradiente_1: Mapped[str] = mapped_column(String(20))
    cor_gradiente_2: Mapped[str] = mapped_column(String(20))
    subtitulo: Mapped[str] = mapped_column(String(160))
    nome: Mapped[str] = mapped_column(String(160))
    badge_texto: Mapped[str] = mapped_column(String(40))
    badge_bg: Mapped[str] = mapped_column(String(20))
    badge_cor: Mapped[str] = mapped_column(String(20))
    tipos: Mapped[list] = mapped_column(JSON, default=list)  # [{"icone": "...", "label": "..."}]

    materia: Mapped["Materia"] = relationship()
    professor: Mapped["Usuario"] = relationship()


class FavoritoBiblioteca(Base):
    __tablename__ = "favoritos_biblioteca"

    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materiais_biblioteca.id"), primary_key=True)


class Tarefa(Base):
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"))
    descricao: Mapped[str] = mapped_column(String(500))
    prazo: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    entregue_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    materia: Mapped["Materia"] = relationship()


class Aviso(Base):
    __tablename__ = "avisos"

    id: Mapped[int] = mapped_column(primary_key=True)
    icone: Mapped[str] = mapped_column(String(60))
    titulo: Mapped[str] = mapped_column(String(160))
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EventoAgenda(Base):
    __tablename__ = "eventos_agenda"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    nome: Mapped[str] = mapped_column(String(160))
    cor: Mapped[str] = mapped_column(String(20))
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Conversa(Base):
    __tablename__ = "conversas"

    id: Mapped[int] = mapped_column(primary_key=True)
    aluno_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    outro_usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    tipo: Mapped[TipoConversa] = mapped_column(SAEnum(TipoConversa), default=TipoConversa.individual)
    nome_exibicao: Mapped[str] = mapped_column(String(120))
    iniciais: Mapped[str] = mapped_column(String(4))
    cor_bg: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cor_texto: Mapped[str | None] = mapped_column(String(20), nullable=True)

    outro_usuario: Mapped["Usuario | None"] = relationship(foreign_keys=[outro_usuario_id])
    mensagens: Mapped[list["Mensagem"]] = relationship(back_populates="conversa", order_by="Mensagem.criado_em")


class Mensagem(Base):
    __tablename__ = "mensagens"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversa_id: Mapped[int] = mapped_column(ForeignKey("conversas.id"))
    remetente_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    texto: Mapped[str] = mapped_column(String(2000))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    conversa: Mapped["Conversa"] = relationship(back_populates="mensagens")
