# Branches dev-ymarega
templates (templates globaux)

But
- Contient les templates partagés par le projet (squelette commun, includes, composants réutilisables).

Fichiers clés
- `base.html` : layout global étendu par les templates d'apps.

Structure et bonnes pratiques
- Mettre les fragments HTML réutilisables dans `templates/includes/` et charger via `{% include %}`.
- Utiliser des blocs (`{% block content %}`, `{% block head %}`) pour permettre l'extension claire des pages.

Internationalisation
- Si le projet devient multilingue, utiliser les tags `{% trans %}` et organiser les templates par langue si nécessaire.
