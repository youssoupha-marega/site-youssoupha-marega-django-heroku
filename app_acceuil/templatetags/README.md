templatetags (app_acceuil)

But
- Fournir des tags et filtres personnalisés réutilisables par les templates de l'app `app_acceuil`.

Fichiers clés
- `utils.py` : contient les fonctions exposées aux templates (`template filters` / `inclusion tags`).

Usage
- Charger le module dans un template :

```django
{% load utils %}
```

- Appeler les filtres/tags documentés dans `utils.py`.

Tests
- Si vous ajoutez des tags complexes, créez des tests unitaires dans `app_acceuil/tests.py` ou un fichier de tests dédié.

Bonnes pratiques
- Garder les tags simples et bien documentés ; éviter la logique lourde côté template (préférer préparer les données dans la vue).
