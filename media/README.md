media

But
- Stocke les fichiers uploadés (images de profil, images de projets, uploads de blog, etc.).

Configuration
- `MEDIA_ROOT` et `MEDIA_URL` sont définis dans `project_site/settings.py`.

Bonnes pratiques
- Ne pas versionner les médias volumineux. Utiliser un stockage externe en production (AWS S3, Cloudinary, etc.).
- Ajouter un `.gitignore/media/` si vous avez des exemples locaux dont vous ne voulez pas garder l'historique.

Exécution locale
- En développement, les médias sont servis par Django lorsque `DEBUG=True`. En production, configurer un serveur ou un backend cloud.

Sécurité
- Valider/cleaner les fichiers uploadés pour éviter des extensions non désirées.
