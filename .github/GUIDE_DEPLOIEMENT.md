# 🚀 Guide de Déploiement - CI/CD avec GitHub Actions et Heroku

## 📋 Table des matières
1. [Prérequis](#prérequis)
2. [Configuration initiale](#configuration-initiale)
3. [Workflow de développement](#workflow-de-développement)
4. [Déploiement en préproduction](#déploiement-en-préproduction)
5. [Déploiement en production](#déploiement-en-production)
6. [Vérification et monitoring](#vérification-et-monitoring)
7. [Rollback en cas de problème](#rollback-en-cas-de-problème)

---

## 🔧 Prérequis

### 1. Applications Heroku créées
- **Production** : `site-youssoupha-marega-django-183342614e64`
- **Préproduction** : À créer sur [Heroku Dashboard](https://dashboard.heroku.com/)

### 2. Secrets GitHub configurés
Allez dans : **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Ajoutez les secrets suivants :

| Nom du secret | Description | Comment l'obtenir |
|---------------|-------------|-------------------|
| `HEROKU_API_KEY` | Clé API Heroku | [Account Settings](https://dashboard.heroku.com/account) → API Key → Reveal |
| `HEROKU_APP_NAME` | Nom app production | `site-youssoupha-marega-django-183342614e64` |
| `HEROKU_APP_NAME_PREPROD` | Nom app préproduction | Nom de votre app de test sur Heroku |

---

## ⚙️ Configuration initiale

### 1. Vérifier les workflows
Deux fichiers de workflow sont présents dans `.github/workflows/` :

```
.github/workflows/
├── deploy.yml          # Production (branche main)
└── deploy-preprod.yml  # Préproduction (branche dev-ymarega)
```

### 2. Vérifier le Dockerfile
Assurez-vous que votre `Dockerfile` est configuré pour Heroku :
```dockerfile
# Le port doit être dynamique
CMD gunicorn project_site.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 💻 Workflow de développement

### Schéma du workflow
```
dev-ymarega (développement)
    ↓ push
[Tests + Deploy Preprod]
    ↓ Pull Request
main (production)
    ↓ merge
[Tests + Deploy Production]
```

---

## 🧪 Déploiement en préproduction

### Étape 1 : Développer sur dev-ymarega
```bash
# S'assurer d'être sur la bonne branche
git checkout dev-ymarega

# Faire vos modifications
# ... éditer vos fichiers ...

# Committer les changements
git add .
git commit -m "feat: ajout nouvelle fonctionnalité"
```

### Étape 2 : Pousser sur GitHub
```bash
git push origin dev-ymarega
```

### Étape 3 : Vérifier le déploiement automatique
1. Allez sur GitHub → Onglet **Actions**
2. Vous verrez un workflow "Deploy to Preprod (Heroku)" en cours
3. Le workflow exécute :
   - ✅ Installation des dépendances
   - ✅ Exécution des tests Django
   - ✅ Build de l'image Docker
   - ✅ Push sur Heroku Container Registry
   - ✅ Déploiement sur l'app de préproduction
   - ✅ Exécution des migrations

### Étape 4 : Tester en préproduction
```bash
# Ouvrir l'app de préproduction
heroku open --app <HEROKU_APP_NAME_PREPROD>
```

Vérifiez que tout fonctionne correctement avant de passer en production.

---

## 🎯 Déploiement en production

### Étape 1 : Créer une Pull Request
1. Allez sur GitHub → Onglet **Pull requests**
2. Cliquez sur **New pull request**
3. Configurez :
   - **Base** : `main`
   - **Compare** : `dev-ymarega`
4. Cliquez sur **Create pull request**

### Étape 2 : Vérification automatique
- Les tests s'exécutent automatiquement sur la PR
- Attendez que tous les checks soient verts ✅
- Vérifiez les changements dans l'onglet **Files changed**

### Étape 3 : Merger la Pull Request
1. Une fois les tests passés, cliquez sur **Merge pull request**
2. Confirmez le merge
3. **Le déploiement en production démarre automatiquement !**

### Étape 4 : Suivre le déploiement
1. Allez dans **Actions** → Workflow "Deploy to Production (Heroku)"
2. Surveillez l'exécution étape par étape
3. Une fois terminé, votre code est en production 🎉

### Étape 5 : Vérifier la production
```bash
# Ouvrir l'app de production
heroku open --app site-youssoupha-marega-django-183342614e64

# Vérifier les logs si besoin
heroku logs --tail --app site-youssoupha-marega-django-183342614e64
```

---

## 🔍 Vérification et monitoring

### Vérifier les logs sur Heroku
```bash
# Logs en temps réel
heroku logs --tail --app site-youssoupha-marega-django-183342614e64

# Logs des 100 dernières lignes
heroku logs -n 100 --app site-youssoupha-marega-django-183342614e64
```

### Vérifier l'état de l'application
```bash
# Status de l'app
heroku ps --app site-youssoupha-marega-django-183342614e64

# Informations sur l'app
heroku apps:info --app site-youssoupha-marega-django-183342614e64
```

### Exécuter des commandes Django sur Heroku
```bash
# Créer un superuser
heroku run python manage.py createsuperuser --app site-youssoupha-marega-django-183342614e64

# Collecter les fichiers statiques
heroku run python manage.py collectstatic --noinput --app site-youssoupha-marega-django-183342614e64

# Ouvrir un shell Django
heroku run python manage.py shell --app site-youssoupha-marega-django-183342614e64
```

---

## 🔄 Rollback en cas de problème

### Option 1 : Rollback via Heroku CLI
```bash
# Voir l'historique des releases
heroku releases --app site-youssoupha-marega-django-183342614e64

# Revenir à une version précédente (ex: v42)
heroku rollback v42 --app site-youssoupha-marega-django-183342614e64
```

### Option 2 : Rollback via GitHub
```bash
# Revenir au commit précédent sur main
git checkout main
git revert HEAD
git push origin main
```
→ Cela déclenchera automatiquement un nouveau déploiement avec l'ancienne version

### Option 3 : Rollback via l'interface Heroku
1. Allez sur [Heroku Dashboard](https://dashboard.heroku.com/)
2. Sélectionnez votre app
3. Onglet **Activity** → Trouvez la release précédente
4. Cliquez sur **Roll back to this version**

---

## 📝 Checklist de déploiement

### Avant chaque déploiement
- [ ] Les tests passent en local : `python manage.py test`
- [ ] Le code fonctionne en local : `python manage.py runserver`
- [ ] Les migrations sont créées : `python manage.py makemigrations`
- [ ] Le fichier `requirements.txt` est à jour
- [ ] Les variables d'environnement sont configurées sur Heroku
- [ ] La préproduction a été testée

### Après chaque déploiement
- [ ] L'application est accessible
- [ ] Les logs ne montrent pas d'erreurs
- [ ] Les fonctionnalités principales fonctionnent
- [ ] Les données sont cohérentes
- [ ] Les fichiers statiques sont servis correctement

---

## 🆘 Résolution de problèmes

### Le workflow échoue sur les tests
```bash
# Exécuter les tests en local
python manage.py test --verbosity=2

# Corriger les erreurs
# Puis recommitter et repousser
```

### Le build Docker échoue
```bash
# Tester le build en local
docker build -t test-app .
docker run -p 8000:8000 test-app

# Vérifier le Dockerfile
```

### L'application ne démarre pas sur Heroku
```bash
# Vérifier les logs
heroku logs --tail --app <APP_NAME>

# Vérifier les variables d'environnement
heroku config --app <APP_NAME>

# Redémarrer l'application
heroku restart --app <APP_NAME>
```

### Les migrations échouent
```bash
# Exécuter les migrations manuellement
heroku run python manage.py migrate --app <APP_NAME>

# Vérifier l'état des migrations
heroku run python manage.py showmigrations --app <APP_NAME>
```

---

## 📚 Ressources utiles

- [Documentation Heroku](https://devcenter.heroku.com/)
- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [Documentation Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Heroku Django Deployment Guide](https://devcenter.heroku.com/articles/deploying-python)

---

## 🎓 Bonnes pratiques

1. **Toujours tester en préproduction d'abord**
2. **Ne jamais pousser directement sur main**
3. **Utiliser des messages de commit descriptifs**
4. **Faire des PR avec des descriptions claires**
5. **Surveiller les logs après chaque déploiement**
6. **Maintenir le README.md à jour**
7. **Documenter les changements importants**

---

**Dernière mise à jour** : Décembre 2025
