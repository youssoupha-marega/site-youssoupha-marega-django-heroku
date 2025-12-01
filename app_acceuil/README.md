app_acceuil

But
- Fournit la page d'accueil du site : profil, résumé, formations, expériences, et sections dynamiques (Compétences, Intérêts, Valeurs, etc.).

Architecture et responsabilités
- `models.py` : modèles principaux (ex : `SiteProfile`, `Education`, `Experience`, `Section`, `SectionItem`) — structure des données affichées sur la page d'accueil.
- `admin.py` : enregistre et personnalise l'administration (inlines pour `SectionItem`, aperçu des icônes, options `extra=0` / `can_delete`).
- `views.py` : vue(s) exposant les données au template (ex: `acceuil` view qui charge `SiteProfile` et sections).
- `templates/app_acceuil/acceuil.html` : template de la page d'accueil qui itère sur les `sections` et affiche les items.
- `static/app_acceuil/` : styles CSS et assets statiques (logo, icônes de démonstration).

Fichiers clés
- `models.py` — définitions des modèles et méthodes utilitaires.
- `admin.py` — configuration des inlines et aperçu image.
- `templates/app_acceuil/acceuil.html` — rendu principal.
- `static/app_acceuil/css/styles.css` — styles locaux.
- `migrations/` — historique des modifications de schéma.

Configuration / Variables d'environnement
- Utilise les paramètres globaux dans `project_site/settings.py` pour `MEDIA_ROOT`, `STATIC_ROOT` et autres variables.

Exécution locale
1. Activez l'environnement virtuel et installez les dépendances :

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

2. Appliquez les migrations et créez un superuser :

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Lancer le serveur :

```bash
python manage.py runserver
```

Modifier le contenu
- Ouvrez l'admin (`/admin/`), éditez `SiteProfile` pour modifier le texte principal, puis créez/éditez des `Section` et `SectionItem` pour gérer les blocs dynamiques.

Bonnes pratiques
- Stocker les médias en production sur un service externe (S3/Cloudinary) plutôt que dans le dépôt.
- Prévisualiser les images depuis l'admin avant déploiement.

Dépannage rapide
- Si les images ne s'affichent pas, vérifier `MEDIA_URL` et que le serveur de développement sert les médias (`django.conf.urls.static`).

Pour contribuer
- Ouvrez une issue pour proposer un changement, ou soumettez une pull request avec une brève description.