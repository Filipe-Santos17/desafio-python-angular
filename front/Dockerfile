FROM node:20-slim AS dev

WORKDIR /app

# Copiar apenas dependências primeiro (melhora cache)
COPY package.json package-lock.json ./

RUN npm i

# Copiar restante do projeto
COPY . .

EXPOSE 4200

# Build produção
CMD ["npm", "run", "start"]

FROM node:20-slim AS prod

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

# Copiar restante do projeto
COPY . .

EXPOSE 4000

#Conserto depois
CMD ["nginx", "-g", "daemon off;"] 