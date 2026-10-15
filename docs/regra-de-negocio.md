### RNE-001 - Critério de aprovação acadêmica
O aluno será considerado aprovado em uma disciplina quando atingir média final maior ou igual a média estabelecida pelo professor/instituição de ensino que está usando o sistema.

- A média deve ser calculada com base nas avaliações definidas pelo professor
- O sistema deve exibir claramente a situação do aluno (aprovado/reprovado)

---

### RNE-002 - Prazo de envio de tarefas
As tarefas devem ser enviadas dentro do prazo estabelecido pelo professor.

- Após o prazo, o sistema pode:
  - Bloquear o envio
  - Ou permitir envio com status de atraso
- O status da tarefa deve ser registrado (pendente, entregue, atrasado)

---

### RNE-003 - Acesso às informações acadêmicas
Responsáveis legais devem ter acesso completo às informações acadêmicas dos alunos vinculados.

- Inclui:
  - Notas
  - Frequência
  - Tarefas
- O acesso deve respeitar vínculo previamente cadastrado

---

### RNE-004 - Restrição de comunicação
A comunicação entre usuários deve respeitar os vínculos institucionais.

- Alunos só podem se comunicar com:
  - Professores de suas disciplinas
  - Usuários autorizados
- Mensagens fora desse escopo devem ser bloqueadas

---

### RNE-005 - Publicação de materiais didáticos
Apenas usuários com perfil de professor podem publicar materiais na biblioteca digital.

- Alunos possuem acesso apenas para visualização
- Conteúdos devem estar associados a disciplinas ou trilhas

---

### RNE-006 - Registro de alterações (auditoria)
Toda alteração em dados relevantes deve ser registrada.

- Inclui:
  - Alterações de notas
  - Atualizações de tarefas
  - Modificações de conteúdo
- O sistema deve manter histórico para auditoria

---

### RNE-007 - Associação entre alunos e responsáveis
Cada responsável pode estar vinculado a um ou mais alunos.

- O vínculo deve ser validado no cadastro
- Responsáveis só podem visualizar dados de alunos associados

---

### RNE-008 - Organização de conteúdos educacionais
Os materiais devem ser organizados de forma estruturada.

- Organização por:
  - Disciplina
  - Turma
  - Trilhas de aprendizagem
- Deve facilitar navegação e acesso aos conteúdos

---

### RNE-009 - Controle de permissões por perfil
O sistema deve diferenciar funcionalidades com base no perfil do usuário.

- Perfis:
  - Aluno
  - Professor
  - Responsável
- Cada perfil possui permissões específicas de acesso e ação

---

### RNE-010 - Frequência mínima para aprovação
O aluno só poderá ser considerado aprovado se possuir frequência mínima estabelecida pela instituição de ensino nas aulas de cada disciplina, independentemente da média obtida nas avaliações.

---

### RNE-011 - Vinculação professor-disciplina-turma
Um professor só pode lançar notas, criar tarefas e publicar materiais nas disciplinas e turmas às quais estiver oficialmente vinculado. Nenhuma ação pedagógica deve ser possível fora desse escopo.

---

### RNE-012 - Pesos das avaliações
A média final deve ser calculada com base nos pesos definidos pelo professor no momento da criação das avaliações. A soma dos pesos deve ser igual a 100% antes que o lançamento seja permitido.

---

### RNE-013 - Prazo mínimo de publicação de tarefas
Tarefas devem ser publicadas com antecedência mínima de 24 horas em relação ao prazo de entrega, impedindo que o professor crie uma tarefa com prazo imediato.

---

### RNE-014 - Restrição de edição de notas
Após o encerramento do período letivo da disciplina, notas só poderão ser alteradas por um administrador, com registro obrigatório de justificativa no log de auditoria.

---

### RNE-015 - Acesso à trilha por pré-requisito
O aluno só poderá acessar um material de nível avançado em uma trilha de aprendizagem se tiver concluído os materiais anteriores marcados como pré-requisito pelo professor.

---

### RNE-016 - Unicidade de matrícula e email
Nenhum usuário pode ser cadastrado com matrícula ou email já existente no sistema, independentemente do perfil. Tentativas de duplicação devem ser bloqueadas com mensagem explicativa.

---

### RNE-017 - Encerramento de turma
Ao encerrar uma turma, o sistema deve bloquear novos lançamentos de notas e tarefas, preservando todo o histórico para consulta futura por alunos e responsáveis.