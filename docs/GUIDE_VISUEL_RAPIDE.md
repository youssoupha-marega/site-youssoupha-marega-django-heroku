# 🎨 Guide Visuel Rapide - Design Harmonisé

## 🌈 Palette de Couleurs par Section

### Navbar
```
Fond: Glassmorphism blanc translucide
Bordure: Gradient tricolore (#667eea → #764ba2 → #0093E9)
Avatar: Bordure violette 2px
Titre: Gradient violet
Nav Links Actifs: Fond gradient violet complet + texte blanc
```

### Section Projets 🚀
```
Titre: Gradient violet (#667eea → #764ba2)
Icône: fa-rocket avec gradient violet
Intro: Background violet 5% opacity
Bordure intro: 4px solid #667eea (gauche)
```

### Section Blog ✍️
```
Titre: Gradient bleu-cyan (#0093E9 → #80D0C7)
Icône: fa-pen-fancy avec gradient bleu
Intro: Background bleu-cyan 5% opacity
Bordure intro: 4px solid #0093E9 (gauche)
```

### Section Services 💼
```
Titre: Gradient rose (#f093fb → #f5576c)
Icône: fa-briefcase avec gradient rose
Intro: Background rose 5% opacity
Bordure intro: 4px solid #f093fb (gauche)
```

### Section Contact 📧
```
Titre: Gradient violet (#667eea → #764ba2)
Icône: fa-paper-plane avec gradient violet
Formulaire: Glassmorphism + bordure top tricolore 4px
Input focus: Bordure #667eea + shadow violette
Bouton: Gradient violet + icône
```

---

## 🎯 Composants Clés

### 1. Titre de Section
- **Font-size**: 2.5rem
- **Font-weight**: 800
- **Effet**: Gradient text clip
- **Icône**: Avec même gradient que le titre

### 2. Section Intro
- **Background**: Gradient 5% opacity
- **Padding**: 1.5rem
- **Border-radius**: 16px
- **Border-left**: 4px solid (couleur assortie)
- **Line-height**: 1.8

### 3. Boutons "Voir tous"
- **Class**: `btn btn-custom-outline`
- **Padding**: 0.65rem 1.5rem
- **Border-radius**: 12px
- **Display**: inline-flex avec gap 8px
- **Icône**: fa-arrow-right

### 4. Content Cards
- **Border-radius**: 12px
- **Box-shadow**: rgba(0,0,0,0.08)
- **Hover**: Transform scale(1.05) sur image
- **Animation**: fadeIn 0.6s
- **Métadonnées**: Icônes colorées (user: violet, calendar: bleu)

### 5. Séparateur de Section
- **Height**: 3px
- **Background**: Gradient tricolore avec transparence
- **Animation**: Shimmer 3s infinite
- **Margin**: 4rem 0

---

## 🎭 Effets Visuels

### Glassmorphism Standard
```css
background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(248,250,252,0.95));
backdrop-filter: blur(10px);
border: 1px solid rgba(100, 116, 139, 0.2);
box-shadow: 0 8px 32px rgba(102, 126, 234, 0.12);
```

### Hover Card
```css
transform: translateY(-6px);
box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
```

### Hover Bouton
```css
transform: translateY(-2px);
box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
```

### Focus Input
```css
border-color: #667eea;
box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
```

---

## 📏 Espacements Standards

### Padding
- **Petit**: 0.65rem (boutons)
- **Moyen**: 1.5rem (intro, cards)
- **Grand**: 2.5rem (formulaire contact)

### Border-radius
- **Petit**: 8px (badges)
- **Moyen**: 12px (boutons, inputs, cards)
- **Grand**: 16px (intro sections)
- **Extra**: 20px (formulaire contact)

### Gaps
- **Mini**: 6px (badges, métadonnées internes)
- **Standard**: 8px (boutons avec icônes)
- **Moyen**: 12px (entre éléments)

---

## 🔤 Typographie

### Titres de Section
```css
font-size: 2.5rem;
font-weight: 800;
background: gradient;
-webkit-background-clip: text;
```

### Sous-titres (Cards)
```css
font-size: 1.2rem;
font-weight: 700;
color: #1a1a2e;
```

### Texte Normal
```css
font-size: 1rem;
color: #64748b;
line-height: 1.7-1.8;
```

### Labels Formulaire
```css
font-weight: 700;
color: #1a1a2e;
display: flex;
align-items: center;
gap: 8px;
```

---

## ⚡ Transitions

### Standard
```css
transition: all 0.3s ease;
```

### Smooth (Premium)
```css
transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
```

### Images
```css
transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 🎨 Code Snippets Prêts à l'Emploi

### Nouveau Titre de Section
```html
<h2 class="section-title mb-0" style="
    font-size: 2.5rem; 
    font-weight: 800; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;">
    <i class="fas fa-YOUR-ICON me-3" style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;"></i>
    Votre Titre
</h2>
```

### Nouvelle Intro de Section
```html
<div class="section-intro mb-4" style="
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%); 
    padding: 1.5rem; 
    border-radius: 16px; 
    border-left: 4px solid #667eea; 
    color: #64748b; 
    line-height: 1.8;">
    Votre texte d'introduction
</div>
```

### Nouveau Bouton avec Icône
```html
<a href="#" class="btn btn-custom-outline" style="
    font-weight: 600; 
    padding: 0.65rem 1.5rem; 
    border-radius: 12px; 
    display: inline-flex; 
    align-items: center; 
    gap: 8px;">
    Texte du bouton
    <i class="fas fa-arrow-right"></i>
</a>
```

---

## 🎯 Checklist Avant Ajout d'une Nouvelle Section

- [ ] Choisir un gradient de couleur distinct
- [ ] Ajouter `animate-fade-in` à la balise `<section>`
- [ ] Utiliser un titre avec gradient et icône assortie
- [ ] Ajouter une intro avec background gradient léger
- [ ] Inclure un bouton "Voir tous" avec icône
- [ ] Utiliser `flex-wrap` et `gap` pour le responsive
- [ ] Tester le hover sur tous les éléments interactifs
- [ ] Vérifier la cohérence des espacements

---

## 🛠️ Classes Utilitaires Personnalisées

### Disponibles
- `.section-title` - Titre de section
- `.section-intro` - Introduction de section
- `.section-separator` - Séparateur animé
- `.btn-custom-primary` - Bouton gradient violet
- `.btn-custom-outline` - Bouton outline gradient
- `.card-custom` - Carte de contenu modernisée
- `.animate-fade-in` - Animation d'apparition

### Font Awesome Icons Utilisées
- **Projets**: `fa-rocket`
- **Blog**: `fa-pen-fancy`
- **Services**: `fa-briefcase`
- **Contact**: `fa-paper-plane`
- **User**: `fa-user-circle`
- **Calendar**: `fa-calendar-alt`
- **Email**: `fa-envelope`
- **Arrow**: `fa-arrow-right`
- **Calendly**: `fa-calendar-check`

---

**🎨 Harmonie = Cohérence + Variété**

Utilisez le **même système** (glassmorphism, border-radius, transitions) mais avec des **gradients différents** par section pour créer de la variété tout en maintenant l'harmonie !
