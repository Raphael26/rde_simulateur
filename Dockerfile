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
    apt-get install -y unzip curl caddy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Crée un dossier de travail
WORKDIR /app

# Copie les fichiers du projet
COPY . .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Initialiser et pré-compiler le frontend pendant le build Docker
# Cela évite de compiler au runtime (qui cause l'erreur EAGAIN)
RUN reflex init
RUN reflex export --frontend-only --no-zip

# Exposer le port
EXPOSE 8080

# Copier le Caddyfile
COPY Caddyfile /etc/caddy/Caddyfile

# Script de démarrage avec migrations et gestion correcte des processus
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Running database migrations..."\n\
reflex db migrate || echo "Migration skipped or not needed"\n\
\n\
echo "Starting Reflex backend on port 8000..."\n\
reflex run --env prod --backend-only --loglevel info &\n\
BACKEND_PID=$!\n\
\n\
# Attendre que le backend soit prêt\n\
echo "Waiting for backend to start..."\n\
sleep 10\n\
\n\
echo "Starting Caddy on port 8080..."\n\
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile &\n\
CADDY_PID=$!\n\
\n\
# Attendre que les deux processus se terminent\n\
wait $BACKEND_PID $CADDY_PID\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/bin/bash", "/app/start.sh"]