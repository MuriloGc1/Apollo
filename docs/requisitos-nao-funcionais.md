### RNF-001 - Usabilidade
O sistema deve ser operável por usuários sem treinamento técnico. Pelo menos 80% dos usuários de teste (professores, alunos e responsáveis) devem conseguir realizar as tarefas principais — login, visualização de notas e envio de mensagens — sem assistência e em no máximo 3 cliques a partir do dashboard.

---

### RNF-002 - Desempenho
O sistema deve responder a 95% das requisições em até 2 segundos, considerando até 100 usuários simultâneos em ambiente de produção.

---

### RNF-003 - Segurança
O sistema deve: (a) armazenar senhas com hash bcrypt ou equivalente; (b) utilizar HTTPS em todas as comunicações; (c) implementar controle de acesso baseado em perfil (RBAC), garantindo que alunos não acessem dados de outros alunos e responsáveis vejam apenas dados de seus filhos vinculados.

---

### RNF-004 - Escalabilidade
A arquitetura deve suportar crescimento de até 500 usuários simultâneos sem necessidade de refatoração estrutural, permitindo escalonamento horizontal do backend Python.

---

### RNF-005 - Disponibilidade
O sistema deve manter alta disponibilidade, minimizando períodos de indisponibilidade.

---

### RNF-006 - Responsividade
O sistema deve funcionar corretamente em diferentes dispositivos, incluindo desktops, tablets e smartphones.

---

### RNF-007 - Manutenibilidade
O código deve seguir separação em camadas (Frontend, API, Banco), com componentes React reutilizáveis e cobertura mínima de comentários nos módulos críticos (autenticação, cálculo de médias).

---

### RNF-008 - Acessibilidade
A interface deve seguir as diretrizes WCAG 2.1 nível AA, incluindo contraste mínimo de 4,5:1 para textos, navegação por teclado e suporte a modo de alto contraste (já previsto no RF-008).

---

### RNF-009 - Confiabilidade
O banco de dados PostgreSQL deve garantir integridade referencial em todas as relações críticas (aluno-turma, nota-disciplina) via constraints. Nenhuma operação de escrita deve resultar em dados inconsistentes, com rollback automático em caso de falha.

---

### RNF-010 — Tempo de Sessão
A sessão do usuário deve expirar automaticamente após 30 minutos de inatividade, exigindo novo login para proteger dados sensíveis como notas e histórico escolar.

---

### RNF-011 — Recuperação de Senha
O sistema deve enviar o link de recuperação de senha em até 60 segundos após a solicitação, com validade de 15 minutos, tornando o link inválido após o uso.

---

### RNF-012 — Auditoria e Rastreabilidade
Toda alteração em notas, tarefas ou dados sensíveis deve gerar um log automático com data, hora e identificação do usuário responsável, conforme previsto na RNE-007. Os logs devem ser armazenados por no mínimo 1 ano letivo.

---

### RNF-013 — Compatibilidade de Navegadores
O sistema deve funcionar corretamente nas duas versões mais recentes dos navegadores Chrome, Firefox, Safari e Edge, sem degradação de funcionalidade.

---

### RNF-014 — Capacidade de Upload
O sistema deve suportar upload de arquivos de até 25MB por material didático na biblioteca digital, aceitando os formatos PDF, DOCX, PPTX, MP4 e imagens (JPG, PNG).

---

### RNF-015 — Notificações em Tempo Real
As notificações de novas mensagens, tarefas e notas devem ser entregues ao usuário em até 5 segundos após o evento, utilizando WebSocket ou mecanismo equivalente.