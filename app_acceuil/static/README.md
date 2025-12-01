static/app_acceuil

But
- Contient les ressources statiques spécifiques à `app_acceuil` : CSS, images, icônes.

Structure
- `css/` : fichiers CSS (ex: `styles.css`).
- `img/` : images et logos utilisés par la page d'accueil.

Utilisation
- En développement, Django sert les fichiers statiques automatiquement.
- En production, exécuter :

```bash
python manage.py collectstatic
```

Configuration
- Vérifier `STATIC_URL` et `STATIC_ROOT` dans `project_site/settings.py`.

Bonnes pratiques
- Minimiser la taille des images pour de meilleures performances.
- Versionner les assets seulement s'ils sont de petite taille ; sinon utiliser un CDN.
