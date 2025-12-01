project_site (configuration du projet)

But
- Contient la configuration globale du projet Django : paramètres, routes racines et points d'entrée WSGI/ASGI.

Fichiers clés
- `settings.py` : configuration (DEBUG, ALLOWED_HOSTS, DATABASES, STATIC/MEDIA, variables d'environnement).
- `urls.py` : routes racines et inclusion des URLs des apps.
- `wsgi.py` / `asgi.py` : points d'entrée pour le déploiement (WSGI pour Gunicorn, ASGI pour Channels/Daphne).

Variables d'environnement importantes
- `SECRET_KEY`, `DATABASE_URL` (si vous utilisez dj-database-url), `DEBUG`, `ALLOWED_HOSTS`, configuration de stockage des médias.

Déploiement
- Le projet est configuré pour être packagé via Docker et déployé sur Heroku. Vérifier :

- `Dockerfile` : image de production.
- `.github/workflows/deploy.yml` : pipeline CI/CD vers Heroku Container Registry.

Conseils de déploiement
- Ajouter `ALLOWED_HOSTS` pour le domaine de production et `CSRF_TRUSTED_ORIGINS` si vous utilisez HTTPS sur un domaine spécifique.
- En production, désactiver `DEBUG` et configurer un backend de stockage pour les médias.

Exécution locale
1. Créez un fichier `.env` pour les secrets (ne pas le committer).

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Migrer la base et lancer le serveur :

```bash
python manage.py migrate
python manage.py runserver
```

Docker (rapide)

```bash
docker compose build
docker compose up
```

Tests & maintenance
- Ajouter des commandes de vérification en CI : tests unitaires, linting, build Docker.
