## Utilise une image Python officielle
#FROM python:3.12-slim
#
## Installe unzip et autres paquets système requis
#RUN apt-get update && \
#    apt-get install -y unzip curl && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*
#
## Crée un dossier de travail
#WORKDIR /app
#
## Copie les fichiers du projet
#COPY . .
#
## Installe les dépendances Python
#RUN pip install --no-cache-dir -r requirements.txt
#
## Construire le frontend statique et préparer les assets
#RUN reflex export --frontend-only --no-zip
#
## Installer Caddy pour servir le frontend et faire le reverse proxy vers le backend
#RUN apt-get update && apt-get install -y caddy
#
## Exposer le port Railway (généralement 8080)
#EXPOSE 8080
#
## Créer un Caddyfile pour le reverse proxy
#COPY Caddyfile /etc/caddy/Caddyfile
#
## Lancer le backend Reflex et Caddy dans le même conteneur
#CMD reflex run --env prod --backend-only --loglevel debug & \
#    caddy run --config /etc/caddy/Caddyfile --adapter caddyfile


# Utilise une image Python officielle
FROM python:3.12-slim

# Installe les paquets système requis
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

# Initialiser Reflex
RUN reflex init

# Exposer le port (Railway assigne dynamiquement via $PORT)
EXPOSE 8080

# Script de démarrage qui utilise le PORT de Railway
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Utiliser le PORT de Railway ou 8080 par défaut\n\
PORT="${PORT:-8080}"\n\
\n\
echo "Starting Reflex on port $PORT..."\n\
\n\
# Lancer Reflex en mode production\n\
exec reflex run --env prod --backend-host 0.0.0.0 --backend-port $PORT --loglevel info\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/bin/bash", "/app/start.sh"]