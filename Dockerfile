# Dockerfile
FROM python:3.12.2-slim

# Optionnel mais pratique
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer les dépendances
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . /app

# (Pas obligatoire sur Heroku, mais pas grave)
EXPOSE 8000

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Lancer le serveur avec Gunicorn en utilisant le PORT fourni par Heroku
CMD ["sh", "-c", "gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --log-file -"]