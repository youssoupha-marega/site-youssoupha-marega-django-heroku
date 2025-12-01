app_service

But
- Gérer les fiches de services proposées (liste, détails, fonctionnalités associées).

Architecture
- `models.py` : `Service` (titre, description, icône, options, `is_published`).
- `views.py` / `urls.py` : vues pour afficher la liste et les pages détail.
- `templates/app_service/` : modèles HTML de rendu.

Fichiers clés
- `models.py`, `admin.py`, `templates/app_service/`.

Exécution et gestion
- Gérer la visibilité via `is_published`.
- Ajouter des fonctionnalités optionnelles (tarifs, liens d'appel à l'action) selon besoin.

Bonnes pratiques
- Faire attention aux liens externes et au référencement (meta tags) sur les pages de service.
