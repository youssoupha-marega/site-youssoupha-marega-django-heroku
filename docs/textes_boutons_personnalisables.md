# Textes de Boutons Personnalisables

## 📋 Vue d'ensemble

Cette fonctionnalité permet de personnaliser tous les textes des boutons de navigation pour chaque profil via l'interface d'administration Django.

## ✨ Nouveaux Champs Ajoutés au Modèle `SiteProfile`

**7 champs personnalisables** pour tous les boutons du site:

### Section Projets
- **`projects_detail_button_text`** (défaut: "Voir le projet")
  - Texte du bouton sur les cartes de projets
  - Utilisé dans: page d'accueil, liste des projets
  
- **`projects_back_button_text`** (défaut: "Retour aux projets")
  - Texte du bouton de retour sur la page détail d'un projet

### Section Blog
- **`blog_detail_button_text`** (défaut: "Lire l'article")
  - Texte du bouton sur les cartes d'articles
  - Utilisé dans: page d'accueil, liste des articles

- **`blog_back_button_text`** (défaut: "Retour aux articles")
  - Texte du bouton de retour sur la page détail d'un article

### Section Services
- **`services_detail_button_text`** (défaut: "En savoir plus")
  - Texte du bouton sur les cartes de services
  - Utilisé dans: page d'accueil, liste des services

- **`services_back_button_text`** (défaut: "Retour aux services")
  - Texte du bouton de retour sur la page détail d'un service

- **`services_calendly_button_text`** (défaut: "Prendre rendez-vous")
  - Texte du bouton Calendly (bouton secondaire sur les cartes de services)
  - Utilisé dans: page d'accueil, liste des services

## 🎯 Utilisation dans l'Admin

1. **Accéder à l'admin**: `/admin/app_acceuil/siteprofile/`
2. **Sélectionner un profil** à modifier
3. **Ouvrir les sections** (elles sont repliées par défaut):
   - "Section Projets (titres/textes)"
   - "Section Blog (titres/textes)"
   - "Section Services (titres/textes)"
4. **Modifier les textes** selon vos préférences
5. **Enregistrer** les modifications

## 📝 Exemples de Personnalisation

### Exemple 1: Profil Développeur
```
projects_detail_button_text = "Voir le code"
projects_back_button_text = "← Tous mes projets"
blog_detail_button_text = "Lire le tutoriel"
blog_back_button_text = "← Tous les tutoriels"
services_detail_button_text = "Découvrir"
services_back_button_text = "← Mes services"
```

### Exemple 2: Profil Designer
```
projects_detail_button_text = "Découvrir ce design"
projects_back_button_text = "← Portfolio"
blog_detail_button_text = "Lire l'article"
blog_back_button_text = "← Blog"
services_detail_button_text = "En savoir +"
services_back_button_text = "← Retour"
services_calendly_button_text = "Réserver un créneau"
```

### Exemple 3: Profil Multilingue (Anglais)
```
projects_detail_button_text = "View project"
projects_back_button_text = "← Back to projects"
blog_detail_button_text = "Read article"
blog_back_button_text = "← Back to blog"
services_detail_button_text = "Learn more"
services_back_button_text = "← Back to services"
services_calendly_button_text = "Book a meeting"
```

## 🔧 Fichiers Modifiés

### Modèle
- **`app_acceuil/models.py`**: Ajout de 7 nouveaux champs CharField

### Admin
- **`app_acceuil/admin.py`**: Ajout des champs dans les fieldsets appropriés

### Migrations
- **`app_acceuil/migrations/0021_siteprofile_blog_back_button_text_and_more.py`**: 6 premiers champs
- **`app_acceuil/migrations/0022_siteprofile_services_calendly_button_text.py`**: Bouton Calendly

### Templates mis à jour
#### Page d'accueil
- **`app_acceuil/templates/app_acceuil/acceuil.html`**:
  - Ligne ~709: Bouton projets
  - Ligne ~754: Bouton blog
  - Ligne ~820: Bouton services

#### Pages de liste
- **`app_projet/templates/app_projet/list.html`**: Bouton "Voir le projet"
- **`app_blog/templates/app_blog/list.html`**: Bouton "Lire l'article"
- **`app_service/templates/app_service/list.html`**: Bouton "En savoir plus"

#### Pages détail (boutons retour)
- **`app_projet/templates/app_projet/detail.html`**: Bouton "Retour aux projets"
- **`app_blog/templates/app_blog/detail.html`**: Bouton "Retour aux articles"
- **`app_service/templates/app_service/detail.html`**: Bouton "Retour aux services"

## ✅ Avantages

1. **Flexibilité linguistique**: Chaque profil peut avoir son propre texte (FR, EN, etc.)
2. **Personnalisation**: Adapter le ton selon le public cible
3. **Cohérence**: Les textes sont centralisés dans un seul endroit
4. **Maintenance facile**: Plus besoin de modifier les templates pour changer un texte
5. **Valeurs par défaut**: Les textes par défaut sont toujours disponibles

## 🚀 Migrations Appliquées

```bash
python manage.py makemigrations app_acceuil
python manage.py migrate app_acceuil
```

**Migrations**: 
- `0021_siteprofile_blog_back_button_text_and_more` (6 champs)
- `0022_siteprofile_services_calendly_button_text` (bouton Calendly)

## 💡 Notes Techniques

- Tous les nouveaux champs sont de type `CharField` avec `max_length=100`
- Les valeurs par défaut sont définies dans le modèle
- Les champs sont optionnels (`blank=True`)
- Les templates utilisent la syntaxe Django: `{{ site_profile.projects_detail_button_text }}`
- Compatible avec le système de profils multiples existant

## 🎨 Intégration avec le Design

Les boutons conservent leur style actuel:
- **Boutons de détail**: Style "btn-custom-primary" (fond blanc → bleu au survol)
- **Boutons retour**: Style "btn-custom-outline" (bordure bleue, fond transparent)
- Les icônes (flèches) sont préservées
- Les animations et transitions restent identiques

---

**Date de création**: 6 décembre 2025  
**Version Django**: 5.1.6  
**Migrations**: 0021 + 0022  
**Total champs ajoutés**: 7
