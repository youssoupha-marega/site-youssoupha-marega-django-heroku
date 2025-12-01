# site-youssoupha-marega-django-heroku

Description
-----------
Ce dépôt contient un site web personnel développé avec Django (plusieurs apps : `app_acceuil`, `app_blog`, `app_projet`, `app_service`, `app_chat`, ...). Le projet est packagé pour le déploiement via Docker et possède une configuration CI/CD pour déployer sur Heroku.

Hébergement
-----------
Le site est hébergé sur Heroku et accessible publiquement à :

https://site-youssoupha-marega-django-183342614e64.herokuapp.com/

Usage local (rapide)
--------------------
- Créer un environnement virtuel et installer les dépendances :

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

- Créer la base et un superuser :

```bash
python manage.py migrate
python manage.py createsuperuser
```

- Lancer le serveur de développement :

```bash
python manage.py runserver
```

Docker
------
Le projet inclut un `Dockerfile` et un `docker-compose.yml` pour exécuter l'application en conteneur. Exemple de build & run :

```bash
docker compose build
docker compose up
```

Remarques et bonnes pratiques
----------------------------
- Les fichiers sensibles (ex : `.env`) et l'environnement virtuel (`venv/`) sont ajoutés à `.gitignore`. Si vous les avez committés par erreur, exécutez :

```bash
git rm --cached .env
git rm -r --cached venv
git commit -m "Stop tracking .env and venv"
git push
```

- En production, il est recommandé d'utiliser un stockage externe pour les médias (S3, Cloudinary, ...).

Contribuer
----------
Ouvrez une issue ou un merge request pour proposer des changements. Voir les README locaux dans chaque app pour des informations détaillées sur leur fonctionnement.

Contact
-------
Pour toute question : utilisez les issues du dépôt.

Détails techniques supplémentaires
-------------------------------
- Langage / Framework : Python 3.x, Django 5.x.
- Base de données : SQLite en développement; adapter `DATABASES` pour la production (Postgres recommandé pour Heroku).
- Dépendances : listées dans `requirements.txt`.
- CI/CD : GitHub Actions construit et pousse l'image Docker vers Heroku Container Registry (voir `.github/workflows/deploy.yml`).

Configuration principale (exemples)
- `SECRET_KEY` : à définir en variable d'environnement.
- `DEBUG` : `False` en production.
- `ALLOWED_HOSTS` : ajouter le domaine Heroku ou custom domain.
- `CSRF_TRUSTED_ORIGINS` : ajouter `https://<votre-domaine>` si nécessaire.

Commandes utiles

```bash
# Créer venv et installer dépendances
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Migration et superuser
python manage.py migrate
python manage.py createsuperuser

# Lancer serveur local
python manage.py runserver

# Docker
docker compose build
docker compose up
```

Cloner le dépôt
---------------
Pour récupérer ce dépôt en local, utilisez l'une des commandes suivantes selon votre configuration Git:

```bash
# via SSH (préféré si votre clé SSH est configurée)
git clone git@github.com:youssoupha-marega/site-youssoupha-marega-django-heroku.git

# ou via HTTPS
git clone https://github.com/youssoupha-marega/site-youssoupha-marega-django-heroku.git
```

Étapes optionnelles après clonage
--------------------------------
- Entrer dans le dossier du projet :

```bash
cd site-youssoupha-marega-django-heroku
```

- (Optionnel) Créer un fichier `.env` à la racine pour les variables d'environnement requises (ex: `SECRET_KEY`, `DATABASE_URL`).
- Installer et activer l'environnement virtuel puis installer les dépendances :

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

- Appliquer les migrations et créer un superuser :

```bash
python manage.py migrate
python manage.py createsuperuser
```

- Lancer en local :

```bash
python manage.py runserver
```

- Pour exécuter via Docker (optionnel) :

```bash
docker compose build
docker compose up
```

Remarque sur l'hébergement
- Le site est déployé sur Heroku et accessible à :

- https://site-youssoupha-marega-django-183342614e64.herokuapp.com/

Si vous souhaitez que je génère un README en anglais ou ajoute des badges (CI, Docker, Heroku), dites-le.