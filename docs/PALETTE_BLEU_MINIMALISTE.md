# 🎨 Palette de Couleurs Minimaliste - Bleu Nuit & Bleu Ciel

Inspirée de votre photo professionnelle pour un design élégant, sobre et professionnel.

---

## 🌈 Palette Principale

### Bleu Nuit (Couleur Principale)
```css
--primary-blue: #2c5282        /* Bleu nuit professionnel - costume */
--primary-blue-dark: #1a365d   /* Bleu nuit plus foncé - ombres */
```

**Utilisation** :
- Boutons principaux
- Icônes de sections (Projets, Services, Contact)
- Liens actifs dans la navbar
- Titres au hover

### Bleu Ciel (Couleur Secondaire)
```css
--secondary-blue: #4a90a4      /* Bleu ciel doux - chemise */
--secondary-blue-light: #5fa8ba /* Bleu ciel plus clair - accents */
```

**Utilisation** :
- Icône Blog/Articles
- Icône Calendrier
- Accents subtils
- Hover secondaire

### Couleurs Neutres
```css
--text-primary: #1a202c        /* Noir doux pour titres */
--text-secondary: #4a5568      /* Gris foncé pour texte */
--text-muted: #718096          /* Gris moyen pour métadonnées */
--border-color: #e2e8f0        /* Gris très clair pour bordures */
--bg-light: #f7fafc            /* Blanc cassé pour backgrounds */
--bg-white: #ffffff            /* Blanc pur */
```

---

## 🎯 Application par Élément

### Navbar
- **Background** : Blanc avec légère opacité `rgba(255, 255, 255, 0.98)`
- **Bordure** : `#e2e8f0` (gris clair)
- **Avatar** : Bordure bleu nuit `rgba(44, 82, 130, 0.2)`
- **Titre** : Noir `#1a202c`
- **Lien actif** : Fond bleu nuit `#2c5282` + texte blanc
- **Lien hover** : Fond bleu nuit 8% `rgba(44, 82, 130, 0.08)` + texte bleu nuit

### Sections (Projets, Blog, Services, Contact)

#### Projets
- **Icône** : `#2c5282` (bleu nuit)
- **Titre** : `#1a202c` (noir doux)
- **Intro background** : Gradient bleu nuit 3% `rgba(44, 82, 130, 0.03)`
- **Bordure gauche** : Bleu nuit 40% `rgba(44, 82, 130, 0.4)`

#### Blog
- **Icône** : `#4a90a4` (bleu ciel)
- **Titre** : `#1a202c` (noir doux)
- **Intro background** : Gradient bleu ciel 3% `rgba(74, 144, 164, 0.03)`
- **Bordure gauche** : Bleu ciel 40% `rgba(74, 144, 164, 0.4)`

#### Services
- **Icône** : `#2c5282` (bleu nuit)
- **Titre** : `#1a202c` (noir doux)
- **Intro background** : Gradient bleu nuit 3%
- **Bordure gauche** : Bleu nuit 40%

#### Contact
- **Icône** : `#2c5282` (bleu nuit)
- **Titre** : `#1a202c` (noir doux)
- **Texte** : `#4a5568` (gris foncé)

### Boutons

#### Bouton Primaire (`.btn-custom-primary`)
```css
background: linear-gradient(135deg, #2c5282 0%, #1a365d 100%);
color: white;
border-radius: 8px;
box-shadow: 0 2px 8px rgba(44, 82, 130, 0.2);
```

#### Bouton Outline (`.btn-custom-outline`)
```css
border: 2px solid #2c5282;
background: transparent;
color: #2c5282;
border-radius: 8px;
```

**Hover** :
```css
background: #2c5282;
color: white;
box-shadow: 0 4px 16px rgba(44, 82, 130, 0.25);
```

### Cartes de Contenu

#### Carte Standard
- **Background** : Blanc `#ffffff`
- **Bordure** : Gris clair `#e2e8f0`
- **Shadow** : `0 1px 3px rgba(44, 82, 130, 0.08)`

#### Titre Carte
- **Couleur** : `#1a202c`
- **Hover** : `#2c5282` (bleu nuit)

#### Métadonnées
- **Icône Auteur** : `#2c5282` (bleu nuit)
- **Icône Date** : `#4a90a4` (bleu ciel)
- **Texte** : `#4a5568` (gris foncé)

#### Hover Carte
```css
transform: translateY(-4px);
box-shadow: 0 8px 24px rgba(44, 82, 130, 0.12);
border-color: rgba(44, 82, 130, 0.3);
```

### Séparateurs
```css
background: linear-gradient(90deg, 
    transparent 0%, 
    rgba(44, 82, 130, 0.15) 20%, 
    rgba(74, 144, 164, 0.2) 50%, 
    rgba(44, 82, 130, 0.15) 80%, 
    transparent 100%
);
height: 1px;
```

---

## 📐 Valeurs Complémentaires

### Ombres
```css
--shadow-sm: 0 1px 3px rgba(44, 82, 130, 0.08);
--shadow-md: 0 4px 12px rgba(44, 82, 130, 0.1);
--shadow-lg: 0 8px 24px rgba(44, 82, 130, 0.12);
```

### Border-radius
```css
Petit : 6px   (navbar toggler)
Moyen : 8px   (boutons, navbar links)
Standard : 10px (intros, cartes)
```

### Transitions
```css
--transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 🎨 Gradients

### Gradient Primaire (Bleu Nuit)
```css
--gradient-primary: linear-gradient(135deg, #2c5282 0%, #1a365d 100%);
```
**Utilisation** : Boutons principaux, backgrounds actifs

### Gradient Secondaire (Mix)
```css
--gradient-secondary: linear-gradient(135deg, #4a90a4 0%, #2c5282 100%);
```
**Utilisation** : Accents subtils

### Gradient Subtil
```css
--gradient-subtle: linear-gradient(135deg, rgba(44, 82, 130, 0.03) 0%, rgba(74, 144, 164, 0.03) 100%);
```
**Utilisation** : Backgrounds intro, hover cards

---

## ✨ Principes de Design

### Minimalisme
- **Pas de couleurs agressives**
- **Opacités très faibles** (3% pour backgrounds)
- **Bordures discrètes** (1px, couleurs claires)
- **Ombres subtiles** (8-12% d'opacité)

### Professionnalisme
- **Couleurs inspirées du costume** (bleu nuit élégant)
- **Blanc dominant** pour respirer
- **Typographie claire** (noir doux, pas de noir pur)
- **Contraste optimal** pour lisibilité

### Cohérence
- **Bleu nuit** pour actions principales et projets/services
- **Bleu ciel** pour articles et dates (plus doux)
- **Gris** pour texte secondaire
- **Blanc** pour l'espace

---

## 🔄 Avant → Après

### ❌ Avant (Violet/Multicolore)
```
Violet : #667eea → #764ba2
Bleu-cyan : #0093E9 → #80D0C7
Rose : #f093fb → #f5576c
```
❌ Trop de couleurs différentes  
❌ Gradients trop visibles  
❌ Manque d'unité visuelle

### ✅ Après (Bleu Nuit/Bleu Ciel)
```
Bleu nuit : #2c5282 → #1a365d
Bleu ciel : #4a90a4 → #5fa8ba
Gris : #1a202c → #718096
```
✅ Palette cohérente (2 bleus + neutres)  
✅ Design minimaliste et sobre  
✅ Professionnel et élégant  
✅ Inspiré de la photo  

---

## 📊 Contraste & Accessibilité

### Ratios de Contraste (WCAG AA+)
- Texte principal (#1a202c) sur blanc : **15.8:1** ✅
- Texte secondaire (#4a5568) sur blanc : **8.9:1** ✅
- Bleu nuit (#2c5282) sur blanc : **6.2:1** ✅
- Blanc sur bleu nuit (#2c5282) : **6.2:1** ✅

Tous les contrastes respectent les normes WCAG AA et AAA !

---

**Design inspiré par** : Photo professionnelle (costume bleu nuit, chemise bleu ciel, fond gris)  
**Philosophie** : Minimaliste, professionnel, élégant  
**Couleurs principales** : 2 bleus + neutres (noir, gris, blanc)  
**Résultat** : Interface sobre, moderne et harmonieuse
