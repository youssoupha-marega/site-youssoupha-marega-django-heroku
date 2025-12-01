`.github` - GitHub Actions & CI

But
- Contient les workflows GitHub Actions et la configuration CI/CD du projet.

Fichiers clés
- `.github/workflows/deploy.yml` : workflow principal qui construit l'image Docker et la publie sur Heroku Container Registry, puis déploie l'application.

Que documente ce README
- But du workflow : build Docker, tests (si présents), push vers Heroku Container Registry, release sur Heroku.
- Secrets attendus :
  - `HEROKU_API_KEY` : clé d'API Heroku (stockée dans les secrets du dépôt)
  - `HEROKU_APP_NAME` : nom de l'application Heroku
  - `HEROKU_EMAIL` : email du compte Heroku (parfois utilisé par certaines actions)
- Étapes importantes dans `deploy.yml` :
  1. Checkout du code
  2. Set up Docker / Build (un `docker build` local dans CI pour faire échouer tôt si build fail)
  3. Login vers Heroku Container Registry
  4. Push de l'image et release
- Où regarder les logs : onglet `Actions` du dépôt → sélectionner le dernier run → cliquer sur le job et parcourir les étapes (build, push, release).

Débogage rapide
- Si le build Docker échoue : inspecter la sortie de l'étape `docker build` (packages manquants, erreurs pip/install). Souvent lié à des dépendances système (ex: Pillow requiert `zlib` et libs d'imagerie).
- Si l'authentification Heroku échoue : vérifier que `HEROKU_API_KEY` est correctement configuré (Settings → Secrets → Actions).
- Si le déploiement passe mais l'app plante : consulter les logs Heroku `heroku logs --tail -a <HEROKU_APP_NAME>`.

Meilleures pratiques
- Garder les secrets dans `Settings → Secrets` (GitHub) ou utiliser un service externe de gestion des secrets.
- Exécuter les tests (unitaires) dans le workflow avant le build docker si vous en ajoutez.

Ajouts possibles
- Ajouter un workflow `pull_request.yml` pour exécuter lint/tests sur chaque PR.
- Ajouter des badges de build dans le `README.md` racine (statut du pipeline).

Contact
- Pour toute modification des workflows, ouvrir une issue ou une PR et mentionner l'équipe/mainteneur.
