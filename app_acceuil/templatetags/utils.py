from django import template
from django.utils.text import slugify
import re

register = template.Library()


@register.filter(name='prefix')
def prefix(value):
    """
    Extract the prefix (first part before underscore) from a URL name.
    For example: 'blogue_list' -> 'blogue', 'projet_detail' -> 'projet'
    """
    if value:
        return value.split('_')[0]
    return value


@register.filter(name='extract_year')
def extract_year(value):
    """
    Extrait l'année ou la plage d'années à la fin d'un texte après une virgule.
    Ex: "Nordikeau, 2022" -> "2022"
    Ex: "AWS, 202" -> "202" (même si incomplet)
    """
    if not value or ',' not in value:
        return ""
    
    # Récupérer tout après la dernière virgule
    parts = value.split(',')
    year_part = parts[-1].strip()
    return year_part


@register.filter(name='remove_year')
def remove_year(value):
    """
    Retire l'année de la fin du texte (tout après la dernière virgule).
    Ex: "Nordikeau, 2022" -> "Nordikeau"
    """
    if not value or ',' not in value:
        return value
    
    # Retourner tout avant la dernière virgule
    parts = value.rsplit(',', 1)
    return parts[0].strip()


@register.simple_tag
def profile_url_params(profile):
    """
    Génère les paramètres d'URL pour un profil dans le chemin
    Retourne: nom=youssoupha-marega&profession=scientifique-de-donnees
    """
    if not profile or profile.is_default:
        return ""
    
    nom_slug = slugify(f"{profile.first_name}-{profile.last_name}")
    profession_slug = slugify(profile.profession) if profile.profession else "profil"
    return f"nom={nom_slug}&profession={profession_slug}"


@register.filter(name='profile_nom_slug')
def profile_nom_slug(profile):
    """
    Génère le slug du nom complet pour les URLs de profil.
    Ex: first_name='Yama', last_name='Sakho' -> 'yama-sakho'
    """
    if not profile:
        return ""
    return slugify(f"{profile.first_name}-{profile.last_name}")


@register.filter(name='profile_profession_slug')
def profile_profession_slug(profile):
    """
    Génère le slug de la profession pour les URLs de profil.
    Ex: profession='Data Analyst' -> 'data-analyst'
    """
    if not profile or not profile.profession:
        return "profil"
    return slugify(profile.profession)
