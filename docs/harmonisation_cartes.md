# Harmonisation des Cartes de Contenu

## 📝 Objectif

Créer un système de cartes **uniforme et réutilisable** pour afficher tous les types de contenu (projets, articles de blog, services) à travers tout le site.

## ✅ Ce qui a été fait

### 1. Composant Réutilisable : `templates/includes/content_card.html`

Un template unique qui gère l'affichage de **tous les types de contenu** :

```django
{% include 'includes/content_card.html' with 
    item=projet 
    detail_url=projet.get_absolute_url 
    button_text="Voir le projet" 
%}
```

#### Paramètres Disponibles

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `item` | Object | **Requis** | L'objet de contenu (Project, BlogPost, Service) |
| `detail_url` | String | **Requis** | URL de la page de détail |
| `button_text` | String | **Requis** | Texte du bouton principal |
| `show_image` | Boolean | `True` | Afficher l'image principale |
| `show_author` | Boolean | `True` | Afficher les infos auteur |
| `show_date` | Boolean | `True` | Afficher la date de publication |
| `show_extra_button` | Boolean | `False` | Afficher un bouton supplémentaire |
| `extra_button_url` | String | - | URL du bouton supplémentaire |
| `extra_button_text` | String | `"Action"` | Texte du bouton supplémentaire |
| `extra_button_target` | String | - | Target du bouton (ex: `"_blank"`) |
| `truncate_words` | Integer | `20` | Nombre de mots pour le résumé |

### 2. Refactorisation des Templates

#### ✨ Avant (Code Dupliqué - 25 lignes par carte)

```django
<div class="card card-custom">
    <div class="card-body">
        <h3 class="card-title h5 mb-2">{{ projet.title }}</h3>
        {% if projet.main_image %}
        <div class="card-media">
            <img src="{{ projet.main_image.url }}" alt="{{ projet.title }}">
        </div>
        {% endif %}
        <p class="card-text text-muted small mb-2">
            <a href="mailto:{{ projet.author_email }}">{{ projet.author_name }}</a>,
            {{ projet.author_profession }}
            <span class="mx-1">|</span>
            {{ projet.published_at|date:"d M Y" }}
        </p>
        <p class="card-text mb-3">{{ projet.resume|striptags|truncatewords:20 }}</p>
        <a href="{% url 'projet_detail' projet.slug %}" class="btn btn-custom-primary mt-2">
            Voir le projet
        </a>
    </div>
</div>
```

#### ✨ Après (1 ligne)

```django
{% include 'includes/content_card.html' with item=projet detail_url=projet.get_absolute_url button_text="Voir le projet" %}
```

### 3. Fichiers Modifiés

| Fichier | Avant | Après | Réduction |
|---------|-------|-------|-----------|
| `app_acceuil/templates/app_acceuil/acceuil.html` | 75 lignes de HTML dupliqué | 3 includes | **-96%** |
| `app_projet/templates/app_projet/list.html` | 25 lignes | 1 include | **-96%** |
| `app_blog/templates/app_blog/list.html` | 25 lignes | 1 include | **-96%** |
| `app_service/templates/app_service/list.html` | 30 lignes | 1 include | **-97%** |

**Total : -155 lignes de code dupliqué éliminées**

## 🎨 Exemples d'Utilisation

### Carte de Projet (Simple)

```django
{% for projet in projets %}
<div class="col-md-4">
    {% include 'includes/content_card.html' with 
        item=projet 
        detail_url=projet.get_absolute_url 
        button_text="Voir le projet" 
    %}
</div>
{% endfor %}
```

### Carte d'Article de Blog

```django
{% for article in articles %}
<div class="col-md-4">
    {% include 'includes/content_card.html' with 
        item=article 
        detail_url=article.get_absolute_url 
        button_text="Lire l'article" 
    %}
</div>
{% endfor %}
```

### Carte de Service (Avec Bouton Calendly)

```django
{% for service in services %}
<div class="col-md-4">
    {% include 'includes/content_card.html' with 
        item=service 
        detail_url=service.get_absolute_url 
        button_text="En savoir plus" 
        show_extra_button=service.calendly_url 
        extra_button_url=service.calendly_url 
        extra_button_text="📅 Prendre rendez-vous" 
        extra_button_target="_blank" 
        show_image=False 
        show_author=False 
        show_date=False 
    %}
</div>
{% endfor %}
```

### Carte Personnalisée (Sans Image, 15 mots)

```django
{% include 'includes/content_card.html' with 
    item=mon_objet 
    detail_url="/mon-url/" 
    button_text="Découvrir" 
    show_image=False 
    truncate_words=15 
%}
```

## 🔧 Styles Centralisés

Tous les styles des cartes sont dans **`app_acceuil/static/app_acceuil/css/styles.css`** :

- `.card-custom` : Style de base de la carte
- `.card-media` : Conteneur d'image avec ratio 16:9
- `.btn-custom-primary` : Bouton principal bleu
- `.btn-custom-outline` : Bouton secondaire outline

Pas besoin de dupliquer les styles dans chaque template !

## 📊 Avantages

### 1. **Maintainabilité** 🛠️
- Une seule source de vérité pour les cartes
- Modification dans 1 fichier au lieu de 4+
- Réduction de 96% du code dupliqué

### 2. **Cohérence** 🎯
- Apparence uniforme sur tout le site
- Même comportement hover/animation
- Même structure responsive

### 3. **Flexibilité** 🎨
- Paramètres optionnels pour personnalisation
- Compatible avec tous les modèles PublishableContent
- Facile d'ajouter de nouveaux types de contenu

### 4. **Performance** ⚡
- Templates plus légers
- Moins de code à parser
- Meilleure performance de rendu

## 🚀 Ajout d'un Nouveau Type de Contenu

Exemple : Ajouter des "Témoignages"

```python
# app_testimonial/models.py
from app_acceuil.base_models import PublishableContent

class Testimonial(PublishableContent):
    company = models.CharField(max_length=200)
    rating = models.IntegerField(default=5)
```

```django
<!-- app_testimonial/templates/app_testimonial/list.html -->
{% for testimonial in testimonials %}
<div class="col-md-4">
    {% include 'includes/content_card.html' with 
        item=testimonial 
        detail_url=testimonial.get_absolute_url 
        button_text="Lire le témoignage" 
        show_image=False 
    %}
</div>
{% endfor %}
```

**C'est tout !** Pas besoin de créer un nouveau template de carte.

## 📖 Bonnes Pratiques

### ✅ À Faire

1. **Toujours** utiliser `get_absolute_url()` pour `detail_url`
2. **Toujours** spécifier `button_text` explicitement
3. **Limiter** le nombre de paramètres (utiliser les defaults)
4. **Tester** l'affichage responsive (mobile)

### ❌ À Éviter

1. **Ne pas** dupliquer le HTML de la carte
2. **Ne pas** créer de styles inline spécifiques
3. **Ne pas** modifier directement `content_card.html` pour un cas particulier
4. **Ne pas** oublier les balises `col-md-4` autour de l'include

## 🔍 Dépannage

### Problème : "Variable does not exist"

**Cause** : Paramètre requis manquant

```django
<!-- ❌ Mauvais -->
{% include 'includes/content_card.html' with item=projet %}

<!-- ✅ Bon -->
{% include 'includes/content_card.html' with 
    item=projet 
    detail_url=projet.get_absolute_url 
    button_text="Voir le projet" 
%}
```

### Problème : Bouton supplémentaire n'apparaît pas

**Solution** : Vérifier que `show_extra_button` est défini

```django
<!-- Vérifier que la condition est vraie -->
{% include 'includes/content_card.html' with 
    show_extra_button=service.calendly_url  <!-- Doit être truthy -->
    extra_button_url=service.calendly_url 
%}
```

### Problème : Image ne s'affiche pas

**Solution** : Vérifier que `main_image` existe

```python
# Dans votre modèle
class MyContent(PublishableContent):
    main_image = models.ImageField(upload_to='...', blank=True, null=True)
```

## 🎯 Prochaines Étapes

1. **Ajouter des variantes de cartes** (horizontale, compacte)
2. **Créer des animations** CSS au survol
3. **Ajouter des badges** (Nouveau, Populaire)
4. **Implémenter le lazy loading** des images

## 📚 Ressources

- [Django Template Include Documentation](https://docs.djangoproject.com/fr/5.1/ref/templates/builtins/#include)
- [Bootstrap Cards](https://getbootstrap.com/docs/5.3/components/card/)
- [CSS Grid Layout](https://developer.mozilla.org/fr/docs/Web/CSS/CSS_Grid_Layout)

---

**Auteur** : Refactorisation réalisée le 5 décembre 2025  
**Version** : 1.0  
**Compatibilité** : Django 5.1+, Bootstrap 5.3+
