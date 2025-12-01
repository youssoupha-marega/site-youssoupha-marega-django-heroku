app_projet

But
- Gérer et afficher les projets du portfolio (liste, détail, images, technologies utilisées).

Architecture
- `models.py` : `Project` et éventuellement `ProjectImage` ou `Feature`.
- `views.py` / `urls.py` : vues `list` et `detail` avec filtrage par publication.
- `templates/app_projet/` : `list.html`, `detail.html`.

Fichiers clés
- `models.py`, `admin.py` (gestion des images/ordering), `templates/app_projet/`.

Exécution locale
- Uploader les images via l'admin et vérifier qu'elles sont servies via `MEDIA_URL`.

Bonnes pratiques
- Préparer des tailles d'images adaptées (vignettes) et stocker les médias en production sur un service dédié.
- Ajouter un champ `is_published` pour contrôler la visibilité.
