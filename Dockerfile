# Usar imagem Python oficial
FROM python:3.13-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (necessário para psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Criar diretório instance se não existir (para SQLite local)
RUN mkdir -p instance

# Expor porta (Railway fornecerá via variável PORT)
EXPOSE 5000

# Variável de ambiente para porta
ENV PORT=5000

# Comando para iniciar a aplicação com gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app

