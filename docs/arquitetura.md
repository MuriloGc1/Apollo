# Arquitetura do Sistema - RED

## Visão Geral
O sistema RED utiliza uma arquitetura em 3 camadas (3-Tier), baseada no modelo cliente-servidor.

## Camadas do Sistema

### Frontend (Apresentação)
Responsável pela interface com o usuário.

Tecnologias:
- HTML
- CSS
- JavaScript
- React

### Backend (Negócio)
Responsável pelas regras de negócio e processamento de dados.

Tecnologia:
- Python (API REST)

### Banco de Dados (Dados)
Responsável pelo armazenamento das informações.

Tecnologia:
- PostgreSQL

## Fluxo de Funcionamento

1. O usuário interage com o frontend
2. O frontend envia requisições ao backend
3. O backend processa as regras de negócio
4. O backend consulta o banco de dados
5. O banco retorna os dados
6. O backend responde ao frontend
7. O frontend exibe as informações ao usuário

## Tecnologias Utilizadas

- React
- Python
- PostgreSQL
- Git e GitHub
- Figma