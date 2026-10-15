from datetime import datetime, timedelta, timezone

from app.database import SessionLocal, Base, engine
from app.models import (
    Usuario, Papel, Materia, Matricula, Nota, MaterialBiblioteca, FavoritoBiblioteca,
    Tarefa, Aviso, EventoAgenda, Conversa, TipoConversa, Mensagem,
)
from app.security import hash_senha

AGORA = datetime.now(timezone.utc)


def _h(horas: float) -> datetime:
    return AGORA + timedelta(hours=horas)


def rodar_seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        aluno = Usuario(nome="Murilo Ferreira", email="murilo@apollo.edu", senha_hash=hash_senha("apollo123"),
                        papel=Papel.aluno, iniciais="M")
        prof_mat = Usuario(nome="Prof. José da Silva", email="jose.silva@apollo.edu", senha_hash=hash_senha("apollo123"),
                            papel=Papel.professor, iniciais="JS")
        prof_por = Usuario(nome="Prof. Maria L. Costa", email="maria.costa@apollo.edu", senha_hash=hash_senha("apollo123"),
                            papel=Papel.professor, iniciais="ML", cor_avatar="#6366f1")
        prof_fil = Usuario(nome="Prof. Roberto S. Lima", email="roberto.lima@apollo.edu", senha_hash=hash_senha("apollo123"),
                            papel=Papel.professor, iniciais="RS", cor_avatar="#0891b2")
        prof_his = Usuario(nome="Prof. Thiago F. Ramos", email="thiago.ramos@apollo.edu", senha_hash=hash_senha("apollo123"),
                            papel=Papel.professor, iniciais="TF", cor_avatar="#b45309")
        prof_bio = Usuario(nome="Prof. Ana C. Ferreira", email="ana.ferreira@apollo.edu", senha_hash=hash_senha("apollo123"),
                            papel=Papel.professor, iniciais="AF", cor_avatar="#22c55e")
        db.add_all([aluno, prof_mat, prof_por, prof_fil, prof_his, prof_bio])
        db.flush()

        mat = Materia(nome="Matemática", cor="#3b82f6")
        por = Materia(nome="Português", cor="#8b5cf6")
        fil = Materia(nome="Filosofia", cor="#0891b2")
        his = Materia(nome="História", cor="#f97316")
        bio = Materia(nome="Biologia", cor="#22c55e")
        db.add_all([mat, por, fil, his, bio])
        db.flush()

        matriculas = [
            Matricula(aluno_id=aluno.id, materia_id=mat.id, professor_id=prof_mat.id, frequencia_percentual=92, progresso_percentual=57),
            Matricula(aluno_id=aluno.id, materia_id=por.id, professor_id=prof_por.id, frequencia_percentual=97, progresso_percentual=72),
            Matricula(aluno_id=aluno.id, materia_id=fil.id, professor_id=prof_fil.id, frequencia_percentual=98, progresso_percentual=80),
            Matricula(aluno_id=aluno.id, materia_id=his.id, professor_id=prof_his.id, frequencia_percentual=84, progresso_percentual=43, cor_progresso="#f97316"),
            Matricula(aluno_id=aluno.id, materia_id=bio.id, professor_id=prof_bio.id, frequencia_percentual=99, progresso_percentual=85),
        ]
        db.add_all(matriculas)
        db.flush()
        m_mat, m_por, m_fil, m_his, m_bio = matriculas

        db.add_all([
            Nota(matricula_id=m_mat.id, bimestre=1, faltas=8, av1=5.5, av2=6.0, av3=6.0),
            Nota(matricula_id=m_por.id, bimestre=1, faltas=3, av1=7.0, av2=7.5, av3=8.0),
            Nota(matricula_id=m_fil.id, bimestre=1, faltas=2, av1=8.0, av2=8.5, av3=8.0),
            Nota(matricula_id=m_his.id, bimestre=1, faltas=11, av1=4.8, av2=5.5, av3=5.0),
            Nota(matricula_id=m_bio.id, bimestre=1, faltas=1, av1=9.0, av2=8.0, av3=8.5),
        ])

        db.add_all([
            Tarefa(aluno_id=aluno.id, materia_id=mat.id,
                   descricao="Assistir ao vídeo anexado e enviar foto dos exercícios resolvidos do capítulo 7.",
                   prazo=_h(-30 * 24)),
            Tarefa(aluno_id=aluno.id, materia_id=por.id,
                   descricao="Produzir um texto dissertativo-argumentativo sobre os impactos das redes sociais.",
                   prazo=_h(5 * 24)),
            Tarefa(aluno_id=aluno.id, materia_id=fil.id,
                   descricao='Resumo sobre "A República" de Platão — capítulos I e II com reflexão pessoal.',
                   prazo=_h(-10 * 24), entregue_em=_h(-12 * 24)),
        ])

        db.add_all([
            Aviso(icone="fa-solid fa-bell", titulo="Semana de Prova", data_hora=_h(-1)),
            Aviso(icone="fa-solid fa-book", titulo="Novo Material", data_hora=_h(-24)),
            Aviso(icone="fa-solid fa-calendar", titulo="Reunião de Pais", data_hora=_h(-48)),
            Aviso(icone="fa-solid fa-trophy", titulo="Olimpíada de Math", data_hora=_h(-96)),
        ])

        db.add_all([
            EventoAgenda(aluno_id=aluno.id, nome="Prova de Filosofia", cor="#3b82f6", data_hora=_h(2)),
            EventoAgenda(aluno_id=aluno.id, nome="Entrega: Texto dissertativo", cor="#22c55e", data_hora=_h(6)),
            EventoAgenda(aluno_id=aluno.id, nome="Prova de Matemática", cor="#3b82f6", data_hora=_h(4 * 24)),
            EventoAgenda(aluno_id=aluno.id, nome="Entrega: Pesquisa de História", cor="#22c55e", data_hora=_h(9 * 24)),
            EventoAgenda(aluno_id=aluno.id, nome="Aula Extra: Redação", cor="#0c447c", data_hora=_h(12 * 24)),
            EventoAgenda(aluno_id=aluno.id, nome="Entrega de boletim", cor="#f97316", data_hora=_h(-3 * 24)),
            EventoAgenda(aluno_id=aluno.id, nome="Feriado — sem aula", cor="#ef4444", data_hora=_h(15 * 24)),
        ])

        materiais = [
            MaterialBiblioteca(materia_id=mat.id, professor_id=prof_mat.id, sigla="MAT",
                                cor_gradiente_1="#1a6bbf", cor_gradiente_2="#0c447c",
                                subtitulo="Probabilidade e estatística", nome="Matemática Avançada",
                                badge_texto="Matemática", badge_bg="#eef4ff", badge_cor="#1a6bbf",
                                tipos=[{"icone": "fa-solid fa-video", "label": "Videoaula disponível"},
                                       {"icone": "fa-solid fa-book", "label": "E-book incluído"},
                                       {"icone": "fa-regular fa-file-pdf", "label": "3 PDFs"}]),
            MaterialBiblioteca(materia_id=por.id, professor_id=prof_por.id, sigla="POR",
                                cor_gradiente_1="#6366f1", cor_gradiente_2="#4338ca",
                                subtitulo="Redação e literatura", nome="Língua Portuguesa",
                                badge_texto="Português", badge_bg="#eef4ff", badge_cor="#6366f1",
                                tipos=[{"icone": "fa-solid fa-video", "label": "2 Videoaulas"},
                                       {"icone": "fa-solid fa-book", "label": "E-book incluído"},
                                       {"icone": "fa-regular fa-file-pdf", "label": "5 Artigos"}]),
            MaterialBiblioteca(materia_id=fil.id, professor_id=prof_fil.id, sigla="FIL",
                                cor_gradiente_1="#0891b2", cor_gradiente_2="#0e7490",
                                subtitulo="Filosofia clássica", nome="Filosofia e Ética",
                                badge_texto="Filosofia", badge_bg="#eff6ff", badge_cor="#0891b2",
                                tipos=[{"icone": "fa-solid fa-video", "label": "Videoaula disponível"},
                                       {"icone": "fa-regular fa-file-pdf", "label": "8 Artigos"}]),
            MaterialBiblioteca(materia_id=his.id, professor_id=prof_his.id, sigla="HIS",
                                cor_gradiente_1="#b45309", cor_gradiente_2="#92400e",
                                subtitulo="Revolução Industrial", nome="História Geral",
                                badge_texto="História", badge_bg="#fff7ed", badge_cor="#b45309",
                                tipos=[{"icone": "fa-solid fa-video", "label": "3 Videoaulas"},
                                       {"icone": "fa-solid fa-book", "label": "E-book incluído"},
                                       {"icone": "fa-regular fa-file-pdf", "label": "4 PDFs"}]),
        ]
        db.add_all(materiais)
        db.flush()
        db.add(FavoritoBiblioteca(aluno_id=aluno.id, material_id=materiais[1].id))

        c_mat = Conversa(aluno_id=aluno.id, outro_usuario_id=prof_mat.id, nome_exibicao=prof_mat.nome, iniciais="JS")
        c_por = Conversa(aluno_id=aluno.id, outro_usuario_id=prof_por.id, nome_exibicao=prof_por.nome, iniciais="ML", cor_bg="#f0fdf4", cor_texto="#16a34a")
        c_fil = Conversa(aluno_id=aluno.id, outro_usuario_id=prof_fil.id, nome_exibicao=prof_fil.nome, iniciais="RS", cor_bg="#eff6ff", cor_texto="#1d4ed8")
        c_his = Conversa(aluno_id=aluno.id, outro_usuario_id=prof_his.id, nome_exibicao=prof_his.nome, iniciais="TF", cor_bg="#fff7ed", cor_texto="#c2410c")
        c_turma = Conversa(aluno_id=aluno.id, tipo=TipoConversa.grupo, nome_exibicao="Turma 3ºA — Geral", iniciais="3A", cor_bg="#fdf4ff", cor_texto="#7e22ce")
        db.add_all([c_mat, c_por, c_fil, c_his, c_turma])
        db.flush()

        db.add_all([
            Mensagem(conversa_id=c_mat.id, remetente_id=prof_mat.id, texto="Bom dia, Murilo! Viu o material novo que postei sobre probabilidade?", criado_em=_h(-1.5)),
            Mensagem(conversa_id=c_mat.id, remetente_id=aluno.id, texto="Bom dia, Professor! Vi sim, já comecei a ler. Tenho uma dúvida sobre o exercício 3.", criado_em=_h(-1.3)),
            Mensagem(conversa_id=c_mat.id, remetente_id=prof_mat.id, texto="Claro, pode perguntar. Qual é a dúvida?", criado_em=_h(-1.25)),
            Mensagem(conversa_id=c_mat.id, remetente_id=aluno.id, texto="Não entendi como calcular a probabilidade condicional quando os eventos não são independentes.", criado_em=_h(-1.2)),
            Mensagem(conversa_id=c_mat.id, remetente_id=prof_mat.id, texto="Boa pergunta! P(A|B) = P(A∩B) / P(B). Vou gravar um vídeo curto com exemplos. Aguarda!", criado_em=_h(-1.1)),
            Mensagem(conversa_id=c_por.id, remetente_id=prof_por.id, texto="Murilo, não esqueça de revisar a estrutura dissertativa antes de entregar.", criado_em=_h(-24)),
            Mensagem(conversa_id=c_fil.id, remetente_id=aluno.id, texto="Professor, o resumo pode ter até 2 páginas?", criado_em=_h(-50)),
            Mensagem(conversa_id=c_his.id, remetente_id=prof_his.id, texto="A pesquisa sobre a Revolução Industrial já está disponível na biblioteca.", criado_em=_h(-50)),
            Mensagem(conversa_id=c_turma.id, remetente_id=prof_mat.id, texto="Pessoal, lembrete: prova de Matemática na próxima semana.", criado_em=_h(-120)),
        ])

        db.commit()
        print("Seed concluído:")
        print(f"  Aluno de teste -> email: {aluno.email}  senha: apollo123")
        print(f"  {len(matriculas)} matrículas, {len(materiais)} materiais, 5 conversas.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    rodar_seed()
