# APOLLO — Full-stack

Plataforma educacional (professores, alunos e responsáveis). Front-end estático
(HTML/CSS/JS puro) + back-end em Python (FastAPI) + PostgreSQL.

```
apollo-fullstack/
├── frontend/     → login.html, painel.html, recuperar-senha.html, css/, js/, assets/
└── backend/      → API FastAPI (app/), seed, requirements.txt
```

O back-end serve o front-end estático junto com a API — em desenvolvimento,
**um comando só sobe o site inteiro**.

---

## 1. Pré-requisitos

- Python 3.11+
- PostgreSQL 14+ instalado e rodando

## 2. Banco de dados

```bash
sudo -u postgres psql -c "CREATE USER apollo_user WITH PASSWORD 'apollo_dev_pass';"
sudo -u postgres psql -c "CREATE DATABASE apollo_db OWNER apollo_user;"
```

(Se preferir outro usuário/senha/banco, ajuste o `.env` no passo 4.)

## 3. Instalar dependências

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Os valores padrão do `.env.example` já batem com o comando do passo 2. Se
você mudou usuário/senha/banco, edite `DATABASE_URL` no `.env`.

## 5. Popular o banco com dados de exemplo

```bash
python -m app.seed
```

Cria as tabelas (se não existirem) e insere disciplinas, notas, tarefas,
avisos, agenda, biblioteca e conversas de exemplo. **Pode rodar de novo a
qualquer momento** — ele limpa e recria tudo do zero.

Usuário de teste criado pelo seed:
| Email | Senha |
|---|---|
| `murilo@apollo.edu` | `apollo123` |

(Os professores também têm login com a mesma senha, ex.: `jose.silva@apollo.edu`,
mas ainda não existe uma tela própria para eles — só a do aluno.)

## 6. Rodar

```bash
uvicorn app.main:app --reload
```

- Site: **http://localhost:8000/login.html**
- Documentação interativa da API (Swagger, gerada automaticamente pelo
  FastAPI): **http://localhost:8000/docs**

---

## Decisões que valem a pena conhecer

- **Limiares de nota/falta/frequência são um chute documentado**, não uma
  regra oficial de escola nenhuma — estão isolados em `app/regras.py` bem no
  topo do arquivo, exatamente para serem fáceis de trocar quando você souber
  a regra real.
- **Recuperação de senha** (`POST /api/auth/recuperar-senha`) valida o e-mail
  e responde com sucesso, mas **não envia e-mail nenhum ainda** — falta
  plugar um serviço de e-mail (SMTP, SendGrid, etc.). É o próximo passo óbvio
  ali.
- **Tabelas são criadas com `Base.metadata.create_all()`**, não com
  migrações. Ótimo para começar; quando o schema começar a mudar com
  frequência, vale migrar para Alembic (`pip install alembic`) para não
  perder dados a cada ajuste de coluna.
- **Token JWT fica em `sessionStorage`** (some ao fechar a aba). Trade-off
  razoável de conveniência x segurança para um projeto acadêmico — para virar
  produção de verdade, o próximo passo é refresh token + expiração mais curta.
- Só existe visão de **aluno**. `papel` já diferencia aluno/professor/
  responsável no banco, mas as telas de professor e responsável ainda não
  foram desenhadas.

## Estrutura do back-end

```
backend/app/
├── main.py          # cria o app, CORS, monta o front-end estático, inclui as rotas
├── config.py        # lê o .env
├── database.py      # engine/sessão do SQLAlchemy
├── models.py         # tabelas
├── schemas.py         # formato de entrada/saída de cada rota (Pydantic)
├── security.py         # hash de senha + JWT
├── regras.py            # limiares de status (nota/falta/frequência)
├── formatadores.py       # datas em português ("10/08/25 19:00", "Ontem"...)
├── seed.py                # dados de exemplo
└── routers/
    ├── auth.py            # login, recuperar senha
    ├── usuario.py          # usuário logado
    ├── avisos.py
    ├── disciplinas.py
    ├── tarefas.py           # + marcar como entregue
    ├── notas.py              # + gráficos de progresso/frequência
    ├── biblioteca.py          # + favoritar
    ├── agenda.py               # hoje / próximos / calendário
    └── mensagens.py             # contatos + chat + enviar mensagem
```
