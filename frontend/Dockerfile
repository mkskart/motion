FROM node:18-slim

WORKDIR /app

# 1️⃣ Install dependencies (npm@8 installs optional Rollup binaries correctly)
COPY frontend/package*.json ./
RUN npm ci

# 2️⃣ Copy source
COPY frontend/ .

EXPOSE 5173

# 3️⃣ Run Vite dev server
CMD ["npm","run","dev","--","--host","0.0.0.0"]