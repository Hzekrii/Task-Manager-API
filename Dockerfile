# ── Image de base ──
FROM python:3.11-slim

# ── Variables d'environnement ──
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ── Répertoire de travail ──
WORKDIR /app

# ── Installation des dépendances système ──
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Installation des dépendances Python ──
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copie du code source ──
COPY . .

# ── Exposition du port ──
EXPOSE 5000

# ── Commande de démarrage ──
CMD ["python", "run.py"]