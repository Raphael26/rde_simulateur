# Utilise une image Python officielle
FROM python:3.12-slim

# Installe unzip et autres paquets système requis
RUN apt-get update && \
    apt-get install -y unzip curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers du projet
COPY . .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Construire le frontend statique et préparer les assets
RUN reflex export --frontend-only --no-zip

# Installer Caddy pour servir le frontend et faire le reverse proxy vers le backend
RUN apt-get update && apt-get install -y caddy

# Exposer le port Railway (généralement 8080)
EXPOSE 8080

# Créer un Caddyfile pour le reverse proxy
COPY Caddyfile /etc/caddy/Caddyfile

# Lancer le backend Reflex et Caddy dans le même conteneur
CMD reflex run --env prod --backend-only --loglevel debug & \
    caddy run --config /etc/caddy/Caddyfile --adapter caddyfile