app_blog

But
- Gérer les articles de blog : création, édition via l'admin, affichage liste et détail.

Architecture
- `models.py` : `BlogPost` (titre, slug, contenu, auteur, date de publication, image, flags `is_published`).
- `views.py` : vues pour la liste (`ListView`) et le détail (`DetailView`) des posts.
- `urls.py` : routes locales (ex : `/blog/`, `/blog/<slug>/`).
- `templates/app_blog/` : `list.html`, `detail.html`.

Fichiers clés
- `models.py`, `views.py`, `admin.py` (personnalisation de l'admin), `templates/app_blog/`.

Exécution locale
- Créer/éditer des posts via l'admin (`/admin/`) ou via fixtures.
- Si vous ajoutez des champs, exécuter `makemigrations` puis `migrate`.

Bonnes pratiques
- Utiliser des slugs uniques pour les URLs lisibles.
- Protéger les champs sensibles et vérifier la pagination pour les listes longues.

Tests
- Ajouter des tests unitaires dans `app_blog/tests.py` pour les vues et la logique métier (publication, filtres `is_published`).