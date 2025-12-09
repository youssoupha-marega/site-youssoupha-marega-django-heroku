# Architecture Refactoring - Plan d'Amélioration Complète

## 📋 Objectif Global

Éliminer la duplication de code et créer une **source unique de vérité** pour :
- Les couleurs et thèmes
- Les composants réutilisables
- Les mises en page (templates)
- Les styles CSS
- **Les modèles de contenu (Project, BlogPost, Service)**

**Bénéfice** : Si on veut changer de couleur ou d'architecture, on change une fois et c'est appliqué partout. Ajouter un nouveau type de contenu = 5 min.

---

## 🎨 1. CSS Variables & Theme System (5 min)

### Problème Actuel
- Couleurs hardcodées partout : `#475569`, `#64748b`, `#1a202c`, `#2c5282`
- Changer une couleur = modifier 10+ fichiers
- Pas de cohérence visuelle centralisée

### Solution
Créer `static/css/theme-variables.css` avec :
```css
:root {
    /* Primary Colors */
    --primary-dark: #1a202c;
    --primary-light: #2c5282;
    --primary-accent: #4a90a4;
    
    /* Secondary Colors */
    --text-primary: #1a202c;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;
    --text-light: #cbd5e1;
    
    /* Background Colors */
    --bg-white: #ffffff;
    --bg-light: #f8fafc;
    --bg-border: #e2e8f0;
    
    /* Section Colors */
    --section-title-color: #475569;
    --section-icon-color: #2c5282;
    
    /* Accent Colors */
    --accent-project: #2c5282;
    --accent-blog: #4a90a4;
    --accent-service: #744210;
    
    /* Typography */
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 1rem;
    --font-size-lg: 1.15rem;
    --font-size-xl: 2rem;
    --font-weight-normal: 400;
    --font-weight-bold: 700;
    --font-weight-heavy: 800;
}
```

### Fichiers à Modifier
- ✅ Créer : `static/css/theme-variables.css`
- Update : `templates/base.html` - ajouter import
- Update : Tous les templates - remplacer couleurs par variables

---

## 🧩 2. Section Title Component (10 min)

### Problème Actuel
Même code répété dans 5 fichiers :
```html
<h2 class="section-title mb-0" style="font-size: 2rem; font-weight: 800; color: #475569; display: flex; align-items: center; gap: 12px;">
```

### Solution
Créer `templates/includes/section_title.html` :
```django
{% comment %} 
  Composant réutilisable pour les titres de section
  
  Usage:
  {% include "includes/section_title.html" with title="Mes Projets" icon="fa-rocket" %}
{% endcomment %}

<h2 class="section-title mb-0" style="font-size: 2rem; font-weight: 800; color: var(--section-title-color); display: flex; align-items: center; gap: 12px;">
    {% if icon %}
        <i class="fas {{ icon }}" style="color: var(--section-icon-color); font-size: 1.8rem;"></i>
    {% endif %}
    {{ title }}
</h2>
```

### Fichiers à Modifier
- ✅ Créer : `templates/includes/section_title.html`
- Update : `section_projects.html` - remplacer h2 par include
- Update : `section_blog.html` - remplacer h2 par include
- Update : `section_services_NEW.html` - remplacer h2 par include
- Update : `section_contact.html` - remplacer h2 par include

---

## 📄 3. Detail Pages Base Template (30 min)

### Problème Actuel
3 fichiers quasiment identiques :
- `app_projet/templates/app_projet/detail.html`
- `app_blog/templates/app_blog/detail.html`
- `app_service/templates/app_service/detail.html`

**Duplication** : 95% du code est le même (structure, métadonnées, styling)

### Solution
Créer `templates/detail_base.html` - template générique
```django
{% extends "base.html" %}
{% load static %}

{% block content %}
<section class="container py-5">
    <!-- Titre -->
    <h1 class="section-title mb-4">{{ object.title|striptags }}</h1>
    
    <!-- Métadonnées -->
    {% include "includes/metadata_block.html" with item=object context_type="detail" %}
    
    <!-- Image -->
    {% if object.main_image %}
    <img src="{{ object.main_image.url }}" alt="{{ object.title|striptags }}" class="w-100 mb-4">
    {% endif %}
    
    <!-- Résumé -->
    <div class="mb-4">
        <p class="lead">{{ object.resume|safe }}</p>
    </div>
    
    <!-- Contenu -->
    <div class="content-body">
        {{ object.content|safe }}
    </div>
</section>
{% endblock %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/detail_base.html`
- Update : `app_projet/detail.html` - hériter de detail_base
- Update : `app_blog/detail.html` - hériter de detail_base
- Update : `app_service/detail.html` - hériter de detail_base

---

## 📊 4. List Pages Base Template (30 min)

### Problème Actuel
3 fichiers très similaires :
- `app_projet/list.html`
- `app_blog/list.html`
- `app_service/list.html`

**Duplication** : Même structure, juste les icônes changent

### Solution
Créer `templates/list_base.html` - template générique
```django
{% extends "base.html" %}

{% block content %}
<section class="container py-5">
    <!-- Section Title -->
    {% include "includes/section_title.html" with title=page_title icon=page_icon %}
    
    <!-- Cards Grid -->
    <div class="row g-4 mt-4">
        {% for item in items %}
            <div class="col-lg-4 col-md-6">
                {% include "includes/content_card.html" with item=item %}
            </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/list_base.html`
- Update : `app_projet/list.html` - hériter de list_base
- Update : `app_blog/list.html` - hériter de list_base
- Update : `app_service/list.html` - hériter de list_base

---

## 🎨 5. Update content_card.html (5 min)

### Changement
Remplacer les couleurs hardcodées par des CSS variables

**Avant** :
```html
<p class="card-text mb-4" style="color: #64748b;">
```

**Après** :
```html
<p class="card-text mb-4" style="color: var(--text-secondary);">
```

### Fichiers à Modifier
- Update : `templates/includes/content_card.html` - utiliser var(--text-secondary), var(--primary-light), etc.

---

## 🗂️ 6. Metadata Display Component (15 min)

### Problème Actuel
Code de métadonnées répété dans :
- `content_card.html` (lignes 65-95)
- Detail pages (lignes 16-30)
- Section templates

### Solution
Créer `templates/includes/metadata_block.html` :
```django
{% comment %}
  Affiche les métadonnées (auteur, profession, dates)
  
  Usage:
  {% include "includes/metadata_block.html" with item=projet context_type="detail" %}
{% endcomment %}

{% if context_type == "detail" %}
    <!-- Metadata pour pages de détail -->
    <div class="metadata-detail mb-4">
        ...
    </div>
{% else %}
    <!-- Metadata pour cartes -->
    <div class="metadata-card">
        ...
    </div>
{% endif %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/includes/metadata_block.html`
- Update : `content_card.html` - remplacer lignes 65-95 par include
- Update : Detail pages - remplacer métadonnées par include

---

## 🎯 7. Icons & Assets Standardization (10 min)

### Problème Actuel
Icônes définies directement dans les templates :
- Projet : `fa-rocket`
- Blog : `fa-pen-fancy`
- Service : `fa-tools`

**Couleurs** : Différentes pour chaque type

### Solution
Créer `static/js/icons-config.js` (ou dans settings.py):
```python
# project_site/settings.py
CONTENT_TYPES_CONFIG = {
    'projet': {
        'icon': 'fa-rocket',
        'color': '#2c5282',
        'label': 'Projets'
    },
    'blog': {
        'icon': 'fa-pen-fancy',
        'color': '#4a90a4',
        'label': 'Blog'
    },
    'service': {
        'icon': 'fa-tools',
        'color': '#744210',
        'label': 'Services'
    }
}
```

Utiliser dans templates :
```django
{% load custom_tags %}
{% get_config 'projet' as config %}
<i class="fas {{ config.icon }}" style="color: {{ config.color }}"></i>
```

### Fichiers à Modifier
- Update : `project_site/settings.py` - ajouter CONTENT_TYPES_CONFIG
- Create : `app_acceuil/templatetags/custom_tags.py` - ajouter tag `get_config`
- Update : Templates - utiliser le tag au lieu de hardcoder

---

## 🚀 8. MAJEURE : Unified Content App (60 min)

### 🔴 PROBLÈME CRITIQUE - Architecture Dupliquée

Actuellement 3 apps identiques :
- `app_projet/` (Project model)
- `app_blog/` (BlogPost model)
- `app_service/` (Service model)

**98% du code est identique** :
- ✅ Même base model : `PublishableContent`
- ✅ Même structure : title, slug, resume, content, author_*, dates
- ✅ Même admin interface
- ✅ Même views (list, detail)
- ✅ Même URLs
- ✅ Même templates

### Solution : Unified Content App

Créer une seule app `app_content` avec un modèle générique :

```python
# app_content/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

CONTENT_TYPE_CHOICES = [
    ('project', 'Projet'),
    ('blog', 'Article de Blog'),
    ('service', 'Service'),
]

class Content(PublishableContent):
    """
    Modèle générique pour tous les types de contenu.
    Le type spécifie simplement les métadonnées et comportements.
    """
    
    # Type de contenu (détermine l'icône, couleur, URL, etc)
    content_type = models.CharField(
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES, 
        default='project',
        verbose_name=_("Type de contenu")
    )
    
    # Champs communs
    content = RichTextUploadingField(verbose_name=_("Contenu détaillé"))
    main_image = models.ImageField(
        upload_to='content/',
        blank=True,
        null=True,
        verbose_name=_("Image principale")
    )
    
    # Champs optionnels (certains utilisés selon le type)
    github_url = models.URLField(blank=True, verbose_name=_("Lien GitHub (projets)"))
    demo_url = models.URLField(blank=True, verbose_name=_("Lien démo (projets)"))
    calendly_url = models.URLField(blank=True, verbose_name=_("Lien Calendly (services)"))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Prix (services)")
    )
    duration = models.CharField(max_length=100, blank=True, verbose_name=_("Durée (services)"))
    
    def get_absolute_url(self):
        """Génère l'URL selon le type de contenu"""
        return reverse('content_detail', args=[self.content_type, self.slug])
    
    class Meta:
        verbose_name = "Contenu"
        verbose_name_plural = "Contenu"
        ordering = ['-created_at']
```

### Avantages

✅ **DRY** : 1 modèle au lieu de 3  
✅ **Maintenabilité** : 1 seule codebase  
✅ **Scalabilité** : Ajouter un type = ajouter une option de choix  
✅ **Admin unifié** : Tous les types dans un seul admin  
✅ **URLs simplifiées** : 1 pattern au lieu de 3  

### Impact

- ❌ Supprimer : `app_projet/`, `app_blog/`, `app_service/`
- ✅ Créer : `app_content/` avec modèle générique
- ✅ Update : URLs, views, templates pour utiliser `content_type`
- ✅ Migration de données : Convertir les 3 anciens types en Content avec `content_type`

### Fichiers Concernés

**À Créer:**
- `app_content/models.py`
- `app_content/views.py`
- `app_content/admin.py`
- `app_content/urls.py`
- `app_content/templates/content_list.html`
- `app_content/templates/content_detail.html`

**À Supprimer:**
- `app_projet/`
- `app_blog/`
- `app_service/`

**À Update:**
- `project_site/settings.py` - INSTALLED_APPS
- `project_site/urls.py` - routing
- `templates/` - tous les includes

---

## 🛠️ 9. Admin Interface Refactoring (20 min)

### Problème Actuel
3 AdminClasses quasi-identiques dans 3 fichiers différents

### Solution
Une seule `ContentAdmin` dans `app_content/admin.py` avec :
- Fieldsets dynamiques basés sur `content_type`
- Inline admin pour les détails optionnels
- Filtres intelligents

```python
# app_content/admin.py
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'author_name', 'published_at')
    list_filter = ('content_type', 'published_at', 'is_published')
    search_fields = ('title', 'resume', 'content')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('title', 'slug', 'resume', 'content_type')
        }),
        ('Contenu', {
            'fields': ('content', 'main_image')
        }),
        ('Champs optionnels', {
            'fields': (
                ('github_url', 'demo_url'),  # Pour projets
                ('calendly_url', 'price', 'duration'),  # Pour services
            ),
            'classes': ('collapse',)
        }),
        ('Auteur', {
            'fields': ('author_name', 'author_email', 'author_profession')
        }),
    )
```

---

## 📊 10. Performance Optimization (15 min)

### Problèmes Actuels
- ❌ N+1 queries (métadonnées chargées plusieurs fois)
- ❌ Images non optimisées
- ❌ CSS non minifiés en production

### Solutions

**1. Database Optimization**
```python
# views.py
def content_list(request, content_type):
    return Content.objects.filter(
        content_type=content_type,
        is_published=True
    ).select_related('author').prefetch_related('tags')  # Éviter N+1
```

**2. Image Optimization**
- Utiliser `easy-thumbnails` pour générer des versions miniatures
- Implémenter du lazy loading avec `loading="lazy"`

**3. Caching**
```python
# views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache 15 minutes
def content_list(request, content_type):
    ...
```

**4. Minification**
- `django-compressor` pour CSS/JS
- `whitenoise` pour static files en production

---

## 🎯 11. URL Routing Simplification (10 min)

### Avant (3 patterns)
```python
# app_projet/urls.py
path('projets/', ProjectListView.as_view(), name='project_list')
path('projets/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail')

# app_blog/urls.py
path('blog/', BlogListView.as_view(), name='blog_list')
path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail')

# app_service/urls.py
path('services/', ServiceListView.as_view(), name='service_list')
path('services/<slug:slug>/', ServiceDetailView.as_view(), name='service_detail')
```

### Après (1 pattern générique)
```python
# app_content/urls.py
path('<str:content_type>/', ContentListView.as_view(), name='content_list')
path('<str:content_type>/<slug:slug>/', ContentDetailView.as_view(), name='content_detail')
```

### Ou avec des redirects
```python
# project_site/urls.py
path('projets/', include('app_content.urls'), kwargs={'content_type': 'project'}),
path('blog/', include('app_content.urls'), kwargs={'content_type': 'blog'}),
path('services/', include('app_content.urls'), kwargs={'content_type': 'service'}),
```

---

## 📋 Checklist Refactoring

### Phase 1 : Fondations (45 min)
- [ ] **CSS Variables**
  - [ ] Créer `theme-variables.css`
  - [ ] Importer dans `base.html`
  - [ ] Remplacer couleurs hardcodées partout

- [ ] **Composants Réutilisables**
  - [ ] Créer `section_title.html`
  - [ ] Créer `metadata_block.html`
  - [ ] Update `content_card.html` avec variables

- [ ] **Templates Génériques**
  - [ ] Créer `detail_base.html`
  - [ ] Créer `list_base.html`
  - [ ] Update les 6 templates existants

### Phase 2 : Architecture (120 min) - 🔴 PRIORITAIRE
- [ ] **Créer app_content**
  - [ ] Modèle Content générique avec `content_type`
  - [ ] Views list/detail
  - [ ] Admin interface unifié
  - [ ] URLs simplifiées

- [ ] **Migration de Données**
  - [ ] Créer migrations data pour Project → Content
  - [ ] Créer migrations data pour BlogPost → Content
  - [ ] Créer migrations data pour Service → Content

- [ ] **Suppression des Anciennes Apps**
  - [ ] Supprimer `app_projet/`, `app_blog/`, `app_service/`
  - [ ] Update `INSTALLED_APPS` dans settings
  - [ ] Vérifier les références résiduelles

- [ ] **Tests & Validation**
  - [ ] Tester les URLs
  - [ ] Vérifier l'admin interface
  - [ ] Vérifier les templates s'affichent correctement

### Phase 3 : Optimisations (30 min)
- [ ] **Performance**
  - [ ] Ajouter `select_related()` et `prefetch_related()`
  - [ ] Implémenter caching
  - [ ] Optimiser les images

- [ ] **Configuration**
  - [ ] Ajouter CONTENT_TYPES_CONFIG dans settings
  - [ ] Créer templatetags custom si nécessaire

---

## 🚀 Avantages Après Refactoring COMPLET

✅ **Maintenabilité** : Changer une couleur = 1 fichier  
✅ **DRY** : No repeated code - 1 model au lieu de 3  
✅ **Scalabilité** : Ajouter un nouveau type de contenu = 5 lignes de code  
✅ **Cohérence** : Styling unifié partout  
✅ **Performance** : Caching, lazy loading, optimisation BD  
✅ **Admin** : 1 interface au lieu de 3  
✅ **URLs** : 2 patterns au lieu de 6  

---

## 📊 Résumé

| Tâche | Temps | Priorité | Complexité | Impact |
|-------|-------|----------|-----------|--------|
| CSS Variables | 5 min | 🔴 Haute | Faible | Moyen |
| Section Title | 10 min | 🔴 Haute | Faible | Moyen |
| Detail Base | 30 min | 🟡 Moyenne | Moyen | Moyen |
| List Base | 30 min | 🟡 Moyenne | Moyen | Moyen |
| Metadata Block | 15 min | 🟡 Moyenne | Moyen | Moyen |
| Icons Config | 10 min | 🟢 Basse | Faible | Faible |
| Update Card | 5 min | 🔴 Haute | Faible | Faible |
| **Unified Content App** | **60 min** | **🔴 HAUTE** | **Élevée** | **ÉNORME** |
| Admin Refactor | 20 min | 🟡 Moyenne | Moyen | Élevé |
| Performance | 15 min | 🟡 Moyenne | Moyen | Élevé |
| URL Simplification | 10 min | 🟡 Moyenne | Faible | Élevé |
| **TOTAL** | **~210 min (3.5h)** | - | - | - |

---

## 🎯 Recommandation

**Faire d'abord :**
1. ✅ **Phase 1** (Fondations) - Rapide, visuel, bon pour la confiance
2. ✅ **Phase 2** (Architecture - App Unifiée) - **LE gros changement** mais crucial
3. ✅ **Phase 3** (Optimisations) - Les petits finitions

Cette refactorisation complète rendra le projet **scalable, maintenable et propre** pour les années à venir. 🚀

---

## 🔗 Références

- [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
- [CSS Variables MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Django Template Inheritance](https://docs.djangoproject.com/en/5.1/topics/templates/#template-inheritance)
- [Django Model Inheritance](https://docs.djangoproject.com/en/5.1/topics/db/models/inheritance/)
- [Content Type Framework](https://docs.djangoproject.com/en/5.1/contenttypes/)


### Problème Actuel
- Couleurs hardcodées partout : `#475569`, `#64748b`, `#1a202c`, `#2c5282`
- Changer une couleur = modifier 10+ fichiers
- Pas de cohérence visuelle centralisée

### Solution
Créer `static/css/theme-variables.css` avec :
```css
:root {
    /* Primary Colors */
    --primary-dark: #1a202c;
    --primary-light: #2c5282;
    --primary-accent: #4a90a4;
    
    /* Secondary Colors */
    --text-primary: #1a202c;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;
    --text-light: #cbd5e1;
    
    /* Background Colors */
    --bg-white: #ffffff;
    --bg-light: #f8fafc;
    --bg-border: #e2e8f0;
    
    /* Section Colors */
    --section-title-color: #475569;
    --section-icon-color: #2c5282;
    
    /* Accent Colors */
    --accent-project: #2c5282;
    --accent-blog: #4a90a4;
    --accent-service: #744210;
    
    /* Typography */
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 1rem;
    --font-size-lg: 1.15rem;
    --font-size-xl: 2rem;
    --font-weight-normal: 400;
    --font-weight-bold: 700;
    --font-weight-heavy: 800;
}
```

### Fichiers à Modifier
- ✅ Créer : `static/css/theme-variables.css`
- Update : `templates/base.html` - ajouter import
- Update : Tous les templates - remplacer couleurs par variables

---

## 🧩 2. Section Title Component (10 min)

### Problème Actuel
Même code répété dans 5 fichiers :
```html
<h2 class="section-title mb-0" style="font-size: 2rem; font-weight: 800; color: #475569; display: flex; align-items: center; gap: 12px;">
```

### Solution
Créer `templates/includes/section_title.html` :
```django
{% comment %} 
  Composant réutilisable pour les titres de section
  
  Usage:
  {% include "includes/section_title.html" with title="Mes Projets" icon="fa-rocket" %}
{% endcomment %}

<h2 class="section-title mb-0" style="font-size: 2rem; font-weight: 800; color: var(--section-title-color); display: flex; align-items: center; gap: 12px;">
    {% if icon %}
        <i class="fas {{ icon }}" style="color: var(--section-icon-color); font-size: 1.8rem;"></i>
    {% endif %}
    {{ title }}
</h2>
```

### Fichiers à Modifier
- ✅ Créer : `templates/includes/section_title.html`
- Update : `section_projects.html` - remplacer h2 par include
- Update : `section_blog.html` - remplacer h2 par include
- Update : `section_services_NEW.html` - remplacer h2 par include
- Update : `section_contact.html` - remplacer h2 par include

---

## 📄 3. Detail Pages Base Template (30 min)

### Problème Actuel
3 fichiers quasiment identiques :
- `app_projet/templates/app_projet/detail.html`
- `app_blog/templates/app_blog/detail.html`
- `app_service/templates/app_service/detail.html`

**Duplication** : 95% du code est le même (structure, métadonnées, styling)

### Solution
Créer `templates/detail_base.html` - template générique
```django
{% extends "base.html" %}
{% load static %}

{% block content %}
<section class="container py-5">
    <!-- Titre -->
    <h1 class="section-title mb-4">{{ object.title|striptags }}</h1>
    
    <!-- Métadonnées -->
    {% include "includes/metadata_block.html" with item=object context_type="detail" %}
    
    <!-- Image -->
    {% if object.main_image %}
    <img src="{{ object.main_image.url }}" alt="{{ object.title|striptags }}" class="w-100 mb-4">
    {% endif %}
    
    <!-- Résumé -->
    <div class="mb-4">
        <p class="lead">{{ object.resume|safe }}</p>
    </div>
    
    <!-- Contenu -->
    <div class="content-body">
        {{ object.content|safe }}
    </div>
</section>
{% endblock %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/detail_base.html`
- Update : `app_projet/detail.html` - hériter de detail_base
- Update : `app_blog/detail.html` - hériter de detail_base
- Update : `app_service/detail.html` - hériter de detail_base

---

## 📊 4. List Pages Base Template (30 min)

### Problème Actuel
3 fichiers très similaires :
- `app_projet/list.html`
- `app_blog/list.html`
- `app_service/list.html`

**Duplication** : Même structure, juste les icônes changent

### Solution
Créer `templates/list_base.html` - template générique
```django
{% extends "base.html" %}

{% block content %}
<section class="container py-5">
    <!-- Section Title -->
    {% include "includes/section_title.html" with title=page_title icon=page_icon %}
    
    <!-- Cards Grid -->
    <div class="row g-4 mt-4">
        {% for item in items %}
            <div class="col-lg-4 col-md-6">
                {% include "includes/content_card.html" with item=item %}
            </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/list_base.html`
- Update : `app_projet/list.html` - hériter de list_base
- Update : `app_blog/list.html` - hériter de list_base
- Update : `app_service/list.html` - hériter de list_base

---

## 🎨 5. Update content_card.html (5 min)

### Changement
Remplacer les couleurs hardcodées par des CSS variables

**Avant** :
```html
<p class="card-text mb-4" style="color: #64748b;">
```

**Après** :
```html
<p class="card-text mb-4" style="color: var(--text-secondary);">
```

### Fichiers à Modifier
- Update : `templates/includes/content_card.html` - utiliser var(--text-secondary), var(--primary-light), etc.

---

## 🗂️ 6. Metadata Display Component (15 min)

### Problème Actuel
Code de métadonnées répété dans :
- `content_card.html` (lignes 65-95)
- Detail pages (lignes 16-30)
- Section templates

### Solution
Créer `templates/includes/metadata_block.html` :
```django
{% comment %}
  Affiche les métadonnées (auteur, profession, dates)
  
  Usage:
  {% include "includes/metadata_block.html" with item=projet context_type="detail" %}
{% endcomment %}

{% if context_type == "detail" %}
    <!-- Metadata pour pages de détail -->
    <div class="metadata-detail mb-4">
        ...
    </div>
{% else %}
    <!-- Metadata pour cartes -->
    <div class="metadata-card">
        ...
    </div>
{% endif %}
```

### Fichiers à Modifier
- ✅ Créer : `templates/includes/metadata_block.html`
- Update : `content_card.html` - remplacer lignes 65-95 par include
- Update : Detail pages - remplacer métadonnées par include

---

## 🎯 7. Icons & Assets Standardization (10 min)

### Problème Actuel
Icônes définies directement dans les templates :
- Projet : `fa-rocket`
- Blog : `fa-pen-fancy`
- Service : `fa-tools`

**Couleurs** : Différentes pour chaque type

### Solution
Créer `static/js/icons-config.js` (ou dans settings.py):
```python
# project_site/settings.py
CONTENT_TYPES_CONFIG = {
    'projet': {
        'icon': 'fa-rocket',
        'color': '#2c5282',
        'label': 'Projets'
    },
    'blog': {
        'icon': 'fa-pen-fancy',
        'color': '#4a90a4',
        'label': 'Blog'
    },
    'service': {
        'icon': 'fa-tools',
        'color': '#744210',
        'label': 'Services'
    }
}
```

Utiliser dans templates :
```django
{% load custom_tags %}
{% get_config 'projet' as config %}
<i class="fas {{ config.icon }}" style="color: {{ config.color }}"></i>
```

---

## 📋 Checklist Refactoring

- [ ] **Phase 1** : CSS Variables
  - [ ] Créer `theme-variables.css`
  - [ ] Importer dans `base.html`
  - [ ] Remplacer couleurs hardcodées partout

- [ ] **Phase 2** : Composants
  - [ ] Créer `section_title.html`
  - [ ] Créer `metadata_block.html`
  - [ ] Update tous les includes

- [ ] **Phase 3** : Templates Génériques
  - [ ] Créer `detail_base.html`
  - [ ] Créer `list_base.html`
  - [ ] Refactor les 6 templates existants

- [ ] **Phase 4** : Icons & Config
  - [ ] Créer config centralisée
  - [ ] Update tous les templates

- [ ] **Testing** : Vérifier visuellement
  - [ ] Toutes les pages s'affichent correctement
  - [ ] Couleurs appliquées uniformément
  - [ ] Tests passent tous

---

## 🚀 Avantages Après Refactoring

✅ **Maintenabilité** : Changer une couleur = 1 fichier  
✅ **DRY** : No repeated code  
✅ **Scalabilité** : Ajouter un nouveau type de contenu = 1 template dérivé  
✅ **Cohérence** : Styling unifié partout  
✅ **Performance** : CSS réutilisable  

---

## 📊 Résumé

| Tâche | Temps | Priorité | Complexité |
|-------|-------|----------|-----------|
| CSS Variables | 5 min | 🔴 Haute | Faible |
| Section Title | 10 min | 🔴 Haute | Faible |
| Detail Base | 30 min | 🟡 Moyenne | Moyen |
| List Base | 30 min | 🟡 Moyenne | Moyen |
| Metadata Block | 15 min | 🟡 Moyenne | Moyen |
| Icons Config | 10 min | 🟢 Basse | Faible |
| Update Card | 5 min | 🔴 Haute | Faible |
| **TOTAL** | **~105 min** | - | - |

---

## 🔗 Références

- [DRY Principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
- [CSS Variables MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/--*)
- [Django Template Inheritance](https://docs.djangoproject.com/en/5.1/topics/templates/#template-inheritance)
