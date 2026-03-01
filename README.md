# DESAFIO TÉCNICO – BACKEND PYTHON (FLASK + REDIS) + FRONTEND ANGULAR

### 1. Objetivo
Construir uma aplicação full stack com:
- [x] Backend em Python + Flask
- [x] Banco de dados PostgreSQL
- [x] Fila com Redis e um worker próprio para processar as mensagens
- [x] Frontend em Angular
  
Funcionalmente, o sistema deve ter:
- [x] Autenticação de usuário (login/logout)
- [] Tela protegida com CRUD de produtos
- [] A tela de produtos no frontend não pode ser acessada sem estar logado e frontend deve bloquear o acesso via Route Guard.
- [x] Processar continuamente a fila com operações de insert, update e delete passando por fila no Redis e sendo aplicadas no banco por um worker.
- [x] - Registrar logs básicos das operações processadas (por exemplo: tipo de operação e ID do
produto).
- [x] Todos os endpoints de /products devem exigir token válido
- [x] Montar uma mensagem com: operação (create, update, delete) e dados do produto (ou ID, no caso de delete)
- [ ] Em caso de erro, registrar o problema para facilitar depuração.

A fazer:

 - 
 -  Arquivo README.md contendo:
 - Passo a passo para subir backend, worker e frontend.
 - Dependências necessárias.
 - Variáveis de ambiente (por exemplo: DATABASE_URL, REDIS_URL, JWT_SECRET_KEY).
 - Comandos básicos para execução (por exemplo: flask run, npm start, comando para iniciar o
worker).

Diferenciais:
- Testes automatizados no backend.
- Uso de Docker / Docker Compose para subir todos os serviços.
- Documentação de API (por exemplo, Swagger/OpenAPI).
- Boas práticas de segurança (hash de senha, expiração de token, etc.).