# DESAFIO TÉCNICO – BACKEND PYTHON (FLASK + REDIS) + FRONTEND ANGULAR

### 1. Objetivo
Construir uma aplicação full stack com:
- [] Backend em Python + Flask
- [] Banco de dados PostgreSQL
- [] Fila com Redis e um worker próprio para processar as mensagens
- [] Frontend em Angular
  
Funcionalmente, o sistema deve ter:
- [] Autenticação de usuário (login/logout)
- [] Tela protegida com CRUD de produtos
- [] Operações de insert, update e delete passando por fila no Redis e sendo aplicadas no banco
por um worker