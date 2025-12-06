# Guide des Tests

Ce document explique comment exécuter et interpréter les tests de l'application.

## Structure des Tests

### Tests Unitaires

Les tests unitaires sont organisés par application Django :

1. **`app_acceuil/tests.py`** (261 lignes, 8 classes de test)
   - `SiteProfileModelTest` : Tests du modèle SiteProfile
   - `PublishableContentTest` : Tests du modèle abstrait PublishableContent
   - `TemplateTagsTest` : Tests des filtres personnalisés (`profile_nom_slug`, `profile_profession_slug`, etc.)
   - `AccueilViewTest` : Tests de la vue d'accueil
   - `ContextProcessorTest` : Tests du context processor

2. **`app_projet/tests.py`** (274 lignes, 6 classes de test)
   - `ProjectModelTest` : Tests du modèle Project
   - `ProjectListViewTest` : Tests de la vue liste racine
   - `ProjectDetailViewTest` : Tests de la vue détail racine
   - `ProfileProjectViewsTest` : Tests des vues avec contexte profil
   - `ProjectURLTest` : Tests de résolution d'URLs

3. **`app_blog/tests.py`** (263 lignes, 6 classes de test)
   - `BlogPostModelTest` : Tests du modèle BlogPost
   - `BlogListViewTest` : Tests de la vue liste racine
   - `BlogDetailViewTest` : Tests de la vue détail racine
   - `ProfileBlogViewsTest` : Tests des vues avec contexte profil
   - `BlogURLTest` : Tests de résolution d'URLs

4. **`app_service/tests.py`** (271 lignes, 6 classes de test)
   - `ServiceModelTest` : Tests du modèle Service
   - `ServiceListViewTest` : Tests de la vue liste racine
   - `ServiceDetailViewTest` : Tests de la vue détail racine
   - `ProfileServiceViewsTest` : Tests des vues avec contexte profil
   - `ServiceURLTest` : Tests de résolution d'URLs

### Tests d'Intégration

**`tests_integration.py`** (506 lignes, 6 classes de test)
- `NavigationIntegrationTest` : Tests de navigation complète
- `PoolArchitectureTest` : Tests du système de pool (contenu partagé entre profils)
- `URLGenerationTest` : Tests de génération d'URLs avec slugs
- `EndToEndUserFlowTest` : Tests de parcours utilisateur complet
- `TemplateFilterIntegrationTest` : Tests d'intégration des filtres de templates

## Exécution des Tests

### Tous les tests

```cmd
python manage.py test
```

### Tests d'une application spécifique

```cmd
python manage.py test app_acceuil
python manage.py test app_projet
python manage.py test app_blog
python manage.py test app_service
```

### Tests d'intégration uniquement

```cmd
python manage.py test tests_integration
```

### Tests d'une classe spécifique

```cmd
python manage.py test app_acceuil.tests.SiteProfileModelTest
python manage.py test app_projet.tests.ProfileProjectViewsTest
```

### Tests d'une méthode spécifique

```cmd
python manage.py test app_acceuil.tests.TemplateTagsTest.test_profile_nom_slug_filter
```

### Tests avec verbosité

```cmd
python manage.py test --verbosity=2
```

### Tests avec rapport de couverture

Si vous avez installé `coverage` :

```cmd
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

Ouvrez ensuite `htmlcov/index.html` dans votre navigateur.

## Couverture des Tests

### Modèles
- ✅ Création et sauvegarde
- ✅ Génération automatique de slugs
- ✅ Unicité des slugs
- ✅ Méthodes `get_absolute_url()`
- ✅ Méthodes `__str__()`
- ✅ Champs optionnels et valeurs par défaut
- ✅ Timestamps automatiques (created_at, updated_at)

### Vues
- ✅ Codes de statut HTTP (200, 404)
- ✅ Templates utilisés
- ✅ Contexte des vues (présence des données)
- ✅ Vues racine (`/projets/`, `/blogue/`, `/services/`)
- ✅ Vues profil (`/profil/nom=...&profession=.../projets/`)
- ✅ Filtrage par profil
- ✅ Gestion des erreurs 404

### URLs
- ✅ Résolution correcte des patterns d'URL
- ✅ URLs racine
- ✅ URLs profil avec paramètres
- ✅ Génération d'URLs via `reverse()`

### Template Tags
- ✅ Filtre `profile_nom_slug`
- ✅ Filtre `profile_profession_slug`
- ✅ Tag `profile_url_params`
- ✅ Filtre `extract_year`
- ✅ Filtre `remove_year`
- ✅ Gestion des espaces et caractères spéciaux

### Intégration
- ✅ Navigation complète entre pages
- ✅ Maintien du contexte profil
- ✅ Pool architecture (contenu partagé)
- ✅ Génération correcte des slugs dans URLs
- ✅ Parcours utilisateur de bout en bout
- ✅ Boutons "Retour" avec contexte profil

## Comportements Testés

### Pool Architecture
Les tests vérifient que :
- Un même contenu (projet, article, service) peut être associé à plusieurs profils
- Chaque profil voit uniquement le contenu qui lui est assigné
- Le même contenu est accessible via différentes URLs de profil
- Le contexte profil est maintenu lors de la consultation du contenu

### Génération d'URLs
Les tests vérifient que :
- Les noms composés sont correctement slugifiés (ex: "Jean-Claude Van Damme" → "jean-claude-van-damme")
- Les professions avec espaces sont slugifiées (ex: "Data Analyst" → "data-analyst")
- Les URLs ne contiennent jamais de valeurs non-slugifiées
- Les URLs sont cohérentes entre les vues et les templates

### Navigation
Les tests vérifient que :
- La navigation depuis une page profil maintient le contexte
- Les boutons "Retour" redirigent vers les bonnes URLs profil
- Les liens dans les cartes utilisent les URLs profil appropriées
- Les templates génèrent des URLs correctes avec les filtres personnalisés

## Statistiques des Tests

### Total : ~1575 lignes de code de tests

- **app_acceuil** : 261 lignes, 8 classes, ~30 tests
- **app_projet** : 274 lignes, 6 classes, ~25 tests
- **app_blog** : 263 lignes, 6 classes, ~24 tests
- **app_service** : 271 lignes, 6 classes, ~25 tests
- **tests_integration** : 506 lignes, 6 classes, ~20 tests

### Total estimé : ~124 tests individuels

## Commandes Utiles

### Exécuter tous les tests et afficher les échecs
```cmd
python manage.py test --failfast
```

### Exécuter les tests en parallèle (plus rapide)
```cmd
python manage.py test --parallel
```

### Garder la base de données de test (pour déboguer)
```cmd
python manage.py test --keepdb
```

### Exécuter les tests avec un pattern spécifique
```cmd
python manage.py test --pattern="test_profile*.py"
```

## Débogage des Tests

Si un test échoue :

1. **Augmenter la verbosité** : `python manage.py test --verbosity=2`
2. **Isoler le test** : Exécuter uniquement le test qui échoue
3. **Vérifier la base de données** : Utiliser `--keepdb` pour inspecter
4. **Ajouter des prints** : Temporairement dans le test pour voir les valeurs
5. **Utiliser le debugger** : 
   ```python
   import pdb; pdb.set_trace()
   ```

## Bonnes Pratiques

1. **Exécuter les tests avant chaque commit**
2. **Ajouter des tests pour chaque nouvelle fonctionnalité**
3. **Maintenir une couverture de code > 80%**
4. **Tester les cas limites et les erreurs**
5. **Utiliser des noms de tests descriptifs**
6. **Garder les tests simples et focalisés**

## CI/CD

Pour intégrer ces tests dans un pipeline CI/CD :

```yaml
# Exemple GitHub Actions
- name: Run Tests
  run: |
    python manage.py test --verbosity=2
    
# Exemple avec coverage
- name: Run Tests with Coverage
  run: |
    pip install coverage
    coverage run --source='.' manage.py test
    coverage report --fail-under=80
```

## Notes Importantes

- Les tests utilisent une base de données SQLite en mémoire par défaut
- Chaque test est isolé (rollback automatique après chaque test)
- Les fichiers média ne sont pas créés réellement pendant les tests
- Les migrations sont appliquées automatiquement avant les tests
