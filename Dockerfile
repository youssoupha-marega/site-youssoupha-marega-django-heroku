# Dockerfile
FROM python:3.12.2-slim

# Optionnel mais pratique
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer les dépendances
COPY requirements.txt /app/
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   pkg-config \
	   zlib1g-dev \
	   libjpeg-dev \
	   libfreetype6-dev \
	   liblcms2-dev \
	   libwebp-dev \
	   tcl-dev \
	   tk-dev \
	   libharfbuzz-dev \
	   libfribidi-dev \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . /app

# (Pas obligatoire sur Heroku, mais pas grave)
EXPOSE 8000

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Lancer le serveur avec Gunicorn en utilisant le PORT fourni par Heroku (ou 8000 par défaut)
CMD ["sh", "-c", "gunicorn project_site.wsgi:application --bind 0.0.0.0:${PORT:-8000} --log-file -"]