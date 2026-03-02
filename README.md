# DESAFIO TÉCNICO – BACKEND PYTHON (FLASK + REDIS) + FRONTEND ANGULAR

## 1. Requisitos do projeto:
Construir uma aplicação full stack com:
- [x] Backend em Python + Flask
- [x] Banco de dados PostgreSQL
- [x] Fila com Redis e um worker próprio para processar as mensagens
- [x] Frontend em Angular
  
Funcionalmente, o sistema deve ter:
- [x] Autenticação de usuário (login/logout)
- [x] Tela protegida com CRUD de produtos
- [x] A tela de produtos no frontend não pode ser acessada sem estar logado e frontend deve bloquear o acesso via Route Guard.
- [x] Processar continuamente a fila com operações de insert, update e delete passando por fila no Redis e sendo aplicadas no banco por um worker.
- [x] Registrar logs básicos das operações processadas (por exemplo: tipo de operação e ID do
produto).
- [x] Todos os endpoints de /products devem exigir token válido
- [x] Montar uma mensagem com: operação (create, update, delete) e dados do produto (ou ID, no caso de delete)
- [x] Em caso de erro, registrar o problema para facilitar depuração.
- [x] Arquivo README.md contendo:
   - Passo a passo para subir backend, worker e frontend.
   - Dependências necessárias.
   - Variáveis de ambiente (por exemplo: DATABASE_URL, REDIS_URL, JWT_SECRET_KEY).
   - Comandos básicos para execução (por exemplo: flask run, npm start, comando para iniciar o worker).

Diferenciais:
- [x] Testes automatizados no backend.
- [x] Uso de Docker / Docker Compose para subir todos os serviços.
- [x] Documentação de API (por exemplo, Swagger/OpenAPI).
- [x] Boas práticas de segurança (hash de senha, expiração de token, etc.).

## 2. Estrutura de pastas do projeto
```bash
├── back
│   ├── alembic
│   │   ├── env.py
│   │   ├── __pycache__
│   │   │   └── env.cpython-312.pyc
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   │       ├── df75ea270624_first_migrate_create_tables.py
│   │       └── __pycache__
│   │           └── df75ea270624_first_migrate_create_tables.cpython-312.pyc
│   ├── alembic.ini
│   ├── app
│   │   ├── auth
│   │   │   ├── add_token_to_response.py
│   │   │   ├── auth_middlware.py
│   │   │   ├── __init__.py
│   │   │   └── jwt_token.py
│   │   ├── envs.py
│   │   ├── __init__.py
│   │   ├── libs
│   │   │   ├── crypto.py
│   │   │   ├── jwt.py
│   │   │   └── redis.py
│   │   ├── middlewares
│   │   ├── models
│   │   │   ├── database.py
│   │   │   ├── entities
│   │   │   │   ├── __init__.py
│   │   │   │   ├── product_entitie.py
│   │   │   │   └── user_entitie.py
│   │   │   └── repository
│   │   │       ├── __init__.py
│   │   │       ├── product_repository.py
│   │   │       └── user_repository.py
│   │   ├── __pycache__
│   │   │   ├── envs.cpython-312.pyc
│   │   │   └── __init__.cpython-312.pyc
│   │   ├── routes
│   │   │   ├── auth_routes.py
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── product_routes.py
│   │   ├── services
│   │   │   └── logger.py
│   │   └── utils
│   │       ├── clear_user.py
│   │       └── random.py
│   ├── app.log
│   ├── app.py
│   ├── Dockerfile
│   ├── global_error.py
│   ├── logs
│   ├── pyproject.toml
│   ├── requests.http
│   ├── uv.lock
│   └── worker.py
├── caddy
│   ├── caddy_config
│   │   └── caddy  
│   ├── caddy_data
│   │   └── caddy  
│   └── Caddyfile
├── docker-compose.yml
├── front
│   ├── angular.json
│   ├── Dockerfile
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   └── favicon.ico
│   ├── README.md
│   ├── src
│   │   ├── app
│   │   │   ├── app.config.ts
│   │   │   ├── app.html
│   │   │   ├── app.routes.ts
│   │   │   ├── app.ts
│   │   │   ├── components
│   │   │   │   ├── common
│   │   │   │   │   └── modais
│   │   │   │   │       └── product
│   │   │   │   │           ├── create
│   │   │   │   │           │   ├── create-modal-product.html
│   │   │   │   │           │   └── create-modal-product.ts
│   │   │   │   │           ├── delete
│   │   │   │   │           │   ├── delete-modal-product.html
│   │   │   │   │           │   └── delete-modal-product.ts
│   │   │   │   │           └── edit
│   │   │   │   │               ├── edit-modal-product.html
│   │   │   │   │               └── edit-modal-product.ts
│   │   │   │   └── ui
│   │   │   │       ├── input
│   │   │   │       │   ├── input.component.html
│   │   │   │       │   └── input.component.ts
│   │   │   │       └── label
│   │   │   │           ├── label.component.html
│   │   │   │           └── label.component.ts
│   │   │   ├── guards
│   │   │   │   ├── auth-guard.spec.ts
│   │   │   │   ├── auth-guard.ts
│   │   │   │   └── guest-guard.ts
│   │   │   ├── pages
│   │   │   │   ├── login
│   │   │   │   │   ├── login.page.html
│   │   │   │   │   └── login.page.ts
│   │   │   │   └── products
│   │   │   │       ├── products.page.html
│   │   │   │       └── products.page.ts
│   │   │   ├── services
│   │   │   │   ├── global_fetch.ts
│   │   │   │   └── token.ts
│   │   │   ├── tests
│   │   │   │   └── app.spec.ts
│   │   │   └── @types
│   │   │       └── index.d.ts
│   │   ├── index.html
│   │   ├── main.ts
│   │   └── styles.css
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   └── tsconfig.spec.json
├── LICENSE
└── README.md
```
44 diretórios, 81 arquivos

## 3. Tecnologias Usadas

Este projeto está sendo desenvolvido com as seguintes tecnologias:

- [Angular](https://angular.dev/)
- [Node](https://nodejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Python](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [PyJWT](https://pyjwt.readthedocs.io/)
- [Redis](https://redis.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [Redis Queue](https://python-rq.org/)

Componentes Estruturais:
- [Docker](https://www.docker.com/): Gerenciamento de containers, start e execução da aplicação e dependências em 2º plano
- [Postgresql](https://www.postgresql.org/): Banco de dados da aplicação, contendo dados de usuários e produtos
- [Redis](https://redis.io/): Cachê da aplicação para salvar dados frequentes e atuar como comunicação entre os containers da api e do worker por meio de filas
- [Caddy](https://caddyserver.com/): Proxy Reverso para prover encriptação http e load balancer para separar requisições do frontend e da api

## 4. Como executar o código

Para clonar e enviar o aplicativo, você precisa ter o [Git](https://git-scm.com), [Node.js](https://nodejs.org/en), [Python](https://docs.python.org/3/) e [Docker](https://www.docker.com/) instalados em sua máquina.

```bash
# Faça um clone do aplicativo.
$ git clone https://github.com/Filipe-Santos17/desafio-python-angular

# Abra a pasta.
$ cd desafio-python-angular

# Crie um arquivo '.env' na raiz do projeto e cole as variáveis  abaixo
$ touch .env

# Execute o código.
$ sudo docker compose up -d --build
```

Variáveis de ambiente:
```bash
ACCESS_TOKEN_EXPIRE_MINUTES=15
SECRET_KEY=6f63ccd8-7d26-49bf-8085-b8f2ede67c66
SECRET_KEY_REFRESH=294544d3-d64b-4412-acfd-cd7ee588d328
ALGORITHM=HS256
DATABASE_USER_SQL=postgres_db
DATABASE_PASSWORD_SQL=PASSWORD_SQL
DATABASE_NAME_SQL=NAME_SQL
STATE=dev
DNS_DOMAIN=localhost
```

## 5. Como executar os testes automatizados
Altere a variável de ambiente state:
```bash
STATE=test
```
e execute o comando para levantar a aplicação
```bash
$ sudo docker compose up -d --build --force-recreate
```

## 6. Como interromper o programa

Caso deseje também deletar os dados use a flag '--volumes' ao final do comando.
```bash
# Execute o código.
$ sudo docker compose down
```


[Filipe Santos on Linkedin](https://www.linkedin.com/in/filipemarquesdeveloper/)
