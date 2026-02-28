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

FROM base AS dev

ENV FLASK_ENV=development

# Copia aplicação
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

FROM base AS prod

ENV FLASK_ENV=production

# Copia aplicação
COPY . .

# Criar usuário não-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]