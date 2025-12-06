from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service
from .models import SiteProfile


def acceuil(request):
    """Vue pour le profil par défaut à la racine /"""
    # Charger le profil par défaut (is_default=True)
    site_profile = SiteProfile.objects.prefetch_related(
        'educations', 'experiences', 'sections__items',
        'featured_projects', 'published_projects',
        'featured_articles', 'published_articles',
        'featured_services', 'published_services'
    ).filter(is_default=True, is_published=True).first()
    
    if not site_profile:
        # Fallback: utiliser le premier profil publié si aucun profil par défaut
        site_profile = SiteProfile.objects.prefetch_related(
            'educations', 'experiences', 'sections__items',
            'featured_projects', 'published_projects',
            'featured_articles', 'published_articles',
            'featured_services', 'published_services'
        ).filter(is_published=True).first()
    
    # Récupérer les projets mis en avant pour ce profil
    if site_profile and site_profile.featured_projects.exists():
        projets_featured = site_profile.featured_projects.filter(is_published=True)
    else:
        projets_featured = Project.objects.filter(featured=True, is_published=True)
    
    # Récupérer les articles mis en avant pour ce profil
    if site_profile and site_profile.featured_articles.exists():
        articles_recents = site_profile.featured_articles.filter(is_published=True)
    else:
        articles_recents = BlogPost.objects.filter(is_published=True, featured=True)
    
    # Récupérer les services mis en avant pour ce profil
    if site_profile and site_profile.featured_services.exists():
        services = site_profile.featured_services.filter(is_published=True)
    else:
        services = Service.objects.filter(is_published=True, featured=True)
    
    context = {
        'projets': projets_featured,
        'articles': articles_recents,
        'services': services,
        'site_profile': site_profile,
    }
    
    return render(request, 'app_acceuil/acceuil.html', context)


def profile_home(request, nom=None, profession=None):
    """Vue pour un profil spécifique avec paramètres dans le chemin"""
    from django.utils.text import slugify
    
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else ""
    
    if not profile_slug:
        # Si pas de paramètres, rediriger vers la racine
        from django.shortcuts import redirect
        return redirect('acceuil')
    
    # Charger le profil spécifique par son slug
    site_profile = get_object_or_404(
        SiteProfile.objects.prefetch_related(
            'educations', 'experiences', 'sections__items',
            'featured_projects', 'published_projects',
            'featured_articles', 'published_articles',
            'featured_services', 'published_services'
        ),
        slug=profile_slug,
        is_published=True
    )
    
    # Récupérer les projets mis en avant pour ce profil
    if site_profile.featured_projects.exists():
        projets_featured = site_profile.featured_projects.filter(is_published=True)
    else:
        projets_featured = site_profile.published_projects.filter(is_published=True)[:3]
    
    # Récupérer les articles mis en avant pour ce profil
    if site_profile.featured_articles.exists():
        articles_recents = site_profile.featured_articles.filter(is_published=True)
    else:
        articles_recents = site_profile.published_articles.filter(is_published=True)[:3]
    
    # Récupérer les services mis en avant pour ce profil
    if site_profile.featured_services.exists():
        services = site_profile.featured_services.filter(is_published=True)
    else:
        services = site_profile.published_services.filter(is_published=True)[:3]
    
    context = {
        'projets': projets_featured,
        'articles': articles_recents,
        'services': services,
        'site_profile': site_profile,
    }
    
    return render(request, 'app_acceuil/acceuil.html', context)

def formation(request):
    return render(request, 'formation.html')
    
def experience(request):
    return render(request, 'experience.html')

def projet(request):
    return render(request, 'projet.html')

def contact(request):
    """Handle contact form submissions and display a contact page if needed.

    The form posts to this view. The destination email is taken from the
    first `SiteProfile.email` found in the database. If none exists we fall
    back to `settings.DEFAULT_FROM_EMAIL` if available.
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        sender = request.POST.get('email', '').strip()
        message_body = request.POST.get('message', '').strip()

        # Determine recipient
        profile = SiteProfile.objects.first()
        recipient = None
        if profile and profile.email:
            recipient = profile.email
        else:
            recipient = getattr(settings, 'DEFAULT_FROM_EMAIL', None)

        if not recipient:
            messages.error(request, "Le message n'a pas pu être envoyé : adresse destinataire non configurée.")
            return redirect(reverse('acceuil'))

        subject = f"Contact depuis le site — {name or 'Visiteur'}"
        full_message = f"Message envoyé depuis le site par: {name}\nEmail: {sender}\n\n{message_body}"

        try:
            send_mail(subject, full_message, sender or settings.DEFAULT_FROM_EMAIL, [recipient])
            messages.success(request, "Merci — votre message a été envoyé.")
        except BadHeaderError:
            messages.error(request, "En-tête invalide détecté. Le message n'a pas été envoyé.")
        except Exception as exc:
            messages.error(request, f"Une erreur s'est produite lors de l'envoi du message : {exc}")

        return redirect(reverse('acceuil'))

    # If GET, just render a simple contact page if separate; reuse acceuil for now
    return render(request, 'contact.html')
