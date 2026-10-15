### RF-001 - Autenticação de usuários
O sistema deve permitir que usuários realizem autenticação por meio de credenciais válidas (email ou matrícula e senha), garantindo acesso seguro ao sistema.

O sistema deve:
- Validar credenciais informadas
- Permitir recuperação de senha
- Diferenciar tipos de usuários (aluno, professor, responsável)

---

### RF-002 - Cadastro de usuários
O sistema deve permitir o cadastro de novos usuários, com coleta e validação de dados obrigatórios.

O sistema deve:
- Permitir cadastro de alunos, professores e responsáveis
- Validar dados como email e senha
- Associar responsáveis aos alunos

---

### RF-003 - Gerenciamento de perfil
O sistema deve permitir que usuários visualizem e atualizem suas informações pessoais.

O sistema deve:
- Exibir dados do usuário
- Permitir edição de informações (nome, email, senha)
- Garantir validação dos dados atualizados

---

### RF-004 - Visualização de desempenho acadêmico
O sistema deve permitir que alunos e responsáveis visualizem o desempenho acadêmico.

O sistema deve:
- Exibir notas por disciplina
- Exibir frequência
- Apresentar histórico escolar consolidado

---

### RF-005 - Comunicação entre usuários
O sistema deve permitir comunicação entre usuários autorizados.

O sistema deve:
- Permitir envio e recebimento de mensagens
- Restringir comunicação conforme vínculo (turma/disciplina)
- Armazenar histórico de mensagens

---

### RF-006 - Gestão de tarefas
O sistema deve permitir o gerenciamento completo de tarefas acadêmicas.

O sistema deve:
- Permitir que professores criem tarefas
- Definir prazos de entrega
- Permitir envio de respostas pelos alunos
- Registrar status (pendente, entregue, atrasado)

---

### RF-007 - Agenda digital
O sistema deve disponibilizar uma agenda acadêmica digital.

O sistema deve:
- Exibir eventos, provas e atividades
- Permitir criação de eventos por professores
- Permitir visualização por alunos e responsáveis

---

### RF-008 - Biblioteca digital
O sistema deve permitir o compartilhamento de materiais educacionais.

O sistema deve:
- Permitir que professores publiquem materiais
- Permitir acesso aos alunos
- Organizar conteúdos por disciplina ou trilha

---

### RF-009 - Sistema de notificações
O sistema deve enviar notificações em tempo real por email.

O sistema deve:
- Notificar sobre novas tarefas
- Notificar sobre mensagens recebidas
- Notificar sobre eventos e prazos

---

### RF-010 — Lançamento de notas e frequência
O sistema deve permitir que professores registrem notas e frequência dos alunos.  
O sistema deve:

- Permitir lançamento de notas por disciplina e avaliação  
- Registrar presença e ausência por aula  
- Calcular automaticamente média final e status (aprovado/reprovado) conforme RNE-001  
- Atualizar o histórico em tempo real após cada lançamento  

---

### RF-011 — Gerenciamento de turmas e disciplinas
O sistema deve permitir a organização das turmas e disciplinas da instituição.  
O sistema deve:

- Permitir criação e edição de turmas  
- Vincular professores a disciplinas e turmas  
- Matricular alunos em turmas  
- Associar responsáveis a alunos vinculados  

---

### RF-012 — Painel administrativo
O sistema deve disponibilizar um painel de gestão para administradores da instituição.  
O sistema deve:

- Permitir criação e inativação de contas  
- Gerenciar vínculos entre usuários (aluno-responsável, professor-turma)  
- Visualizar relatórios gerais de desempenho da instituição  

---

### RF-013 — Recuperação de senha
O sistema deve permitir que usuários recuperem acesso à conta em caso de esquecimento de senha.  
O sistema deve:

- Enviar link de recuperação ao email cadastrado  
- Invalidar o link após uso ou expiração (15 minutos, conforme RNF-011)  
- Exigir confirmação de nova senha  