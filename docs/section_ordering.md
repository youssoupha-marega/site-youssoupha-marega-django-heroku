# Système d'ordonnancement des sections

## Vue d'ensemble

Le système vous permet de contrôler l'ordre d'affichage des sections principales (Projets, Blog, Services, Contact) dans:
- **La barre de navigation** (sauf Contact qui n'apparaît que sur la page d'accueil)
- **La page d'accueil**

## Configuration dans l'admin

### Accès aux paramètres

1. Allez dans **Admin** → **Profils du site** → Sélectionnez votre profil
2. Vous verrez maintenant 4 nouveaux champs dans chaque section:

#### Section Projets
- **`projects_display_order`** : Contrôle la position des projets (défaut: 2)

#### Section Blog  
- **`blog_display_order`** : Contrôle la position du blog (défaut: 3)

#### Section Services
- **`services_display_order`** : Contrôle la position des services (défaut: 4)

#### Section Contact (NOUVEAU)
- **`contact_display_order`** : Contrôle la position du contact (défaut: 5)
- **Note importante** : La section Contact apparaît **UNIQUEMENT sur la page d'accueil**, PAS dans la barre de navigation

## Comment ça fonctionne

### Ordre par défaut
```
Accueil (toujours en position 1, non modifiable)
Projets (2)
Blog (3)
Services (4)
Contact (5) - page d'accueil seulement
```

### Exemples de réordonnancement

#### Exemple 1: Mettre les Services en premier
```
projects_display_order = 3
blog_display_order = 4
services_display_order = 2
contact_display_order = 5
```
**Résultat** :
- Navbar: Accueil → Services → Projets → Blog
- Page d'accueil: Sections bio/formation/expérience → Services → Projets → Blog → Contact

#### Exemple 2: Mettre le Blog en premier, Contact en 3ème position
```
projects_display_order = 3
blog_display_order = 2
services_display_order = 4
contact_display_order = 3
```
**Résultat** :
- Navbar: Accueil → Blog → Projets → Services
- Page d'accueil: Sections bio/formation/expérience → Blog → Contact → Projets → Services

#### Exemple 3: Inverser l'ordre complet
```
projects_display_order = 4
blog_display_order = 3
services_display_order = 2
contact_display_order = 5
```
**Résultat** :
- Navbar: Accueil → Services → Blog → Projets
- Page d'accueil: Sections bio/formation/expérience → Services → Blog → Projets → Contact

## Sections fixes (non réordonnables)

Les sections suivantes restent toujours au même endroit sur la page d'accueil:

1. **Bio** (image de profil, description)
2. **Formation** (diplômes, certifications)
3. **Expérience** (parcours professionnel)
4. **Sections personnalisées** (créées via Section/SectionItem)

Ces sections apparaissent **TOUJOURS EN PREMIER** sur la page d'accueil, avant les sections réordonnables.

## Barre de navigation vs Page d'accueil

| Section   | Navbar | Page d'accueil |
|-----------|--------|----------------|
| Accueil   | ✓      | -              |
| Projets   | ✓      | ✓              |
| Blog      | ✓      | ✓              |
| Services  | ✓      | ✓              |
| Contact   | ✗      | ✓              |
| Bio       | ✗      | ✓ (fixe)       |
| Formation | ✗      | ✓ (fixe)       |
| Expérience| ✗      | ✓ (fixe)       |

## Tests recommandés

1. **Changez les valeurs** dans l'admin
2. **Sauvegardez** le profil
3. **Rafraîchissez** la page d'accueil
4. **Vérifiez** :
   - L'ordre des liens dans la navbar
   - L'ordre des sections sur la page d'accueil
   - Que Contact n'apparaît PAS dans la navbar

## Images des sections

Chaque section peut avoir:
- **Une image d'en-tête** (affichée à côté du titre sur la page d'accueil)
- **Une icône par défaut** (utilisée si aucune image n'est uploadée)

Images disponibles:
- `projects_home_image` : Image pour la section Projets
- `blog_home_image` : Image pour la section Blog
- `services_home_image` : Image pour la section Services
- `bio_title_image` : Image pour le titre de la bio

## Notes techniques

### Code backend
- **Modèle** : `app_acceuil/models.py` → méthode `get_ordered_sections()`
- **Admin** : `app_acceuil/admin.py` → fieldsets mis à jour
- **Context processor** : `app_acceuil/context_processors.py` → fonction `menu_items()`

### Templates
- **Includes** : `templates/includes/section_*.html` (un fichier par section)
- **Page principale** : `app_acceuil/templates/app_acceuil/acceuil.html` → boucle dynamique

### Migrations appliquées
- `0026_siteprofile_bio_title_image` : Ajout de l'image de titre de la bio
- `0027_siteprofile_blog_display_order_and_more` : Ajout des 4 champs display_order

## Dépannage

### La navbar ne change pas
- Vérifiez que vous avez bien sauvegardé le profil dans l'admin
- Rafraîchissez la page (Ctrl+F5 pour vider le cache)
- Vérifiez dans le terminal qu'il n'y a pas d'erreur

### Les sections n'apparaissent pas
- Assurez-vous que les projets/articles/services sont **publiés** (`is_published=True`)
- Vérifiez qu'il y a au moins 1 élément dans chaque section

### Contact apparaît dans la navbar
- Cela ne devrait JAMAIS arriver
- Si c'est le cas, contactez le développeur (bug dans le code)
