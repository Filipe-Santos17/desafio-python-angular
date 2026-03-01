FROM python:3.12-alpine AS base

# Melhor prática: evitar .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apk add --no-cache \
    build-base \
    libpq-dev

# Instalar uv
RUN pip install --no-cache-dir uv

# Copia apenas arquivos de dependência para cache otimizado
COPY uv.lock pyproject.toml ./

# Instala dependências no ambiente global
RUN uv pip install --system .

# Logs
RUN mkdir -p /var/log/app
RUN chmod -R 777 /var/log/app

FROM base AS dev

ENV FLASK_ENV=development

COPY . .

EXPOSE 5000

RUN chmod 777 ./bin/init.sh

CMD sh ./bin/init.sh

FROM base AS test

ENV FLASK_ENV=test
ENV PYTHONPATH=/app

RUN uv pip install --system . --group dev

COPY . .

EXPOSE 5000

RUN chmod 777 ./bin/init.sh

CMD sh ./bin/init.sh

FROM base AS prod

ENV FLASK_ENV=production

COPY . .

# Criar usuário não-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 5000

RUN chmod 777 ./bin/init.sh

CMD sh ./bin/init.sh