FROM node:20-slim AS dev

WORKDIR /app

# Copia dependências primeiro (melhora cache)
COPY package.json package-lock.json ./

RUN npm install

# Copia restante do projeto
COPY . .

EXPOSE 4200

CMD ["npm", "run", "start"]


FROM node:20-slim AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm ci --omit=dev

COPY . .

# Build de produção do Angular
RUN npm run build


FROM node:20-slim AS prod

WORKDIR /app

# Instala apenas servidor estático leve
RUN npm install -g serve

# Copia build do Angular
COPY --from=build /app/dist ./dist

EXPOSE 4000

# Serve os arquivos estáticos
CMD ["serve", "-s", "dist", "-l", "4000"]