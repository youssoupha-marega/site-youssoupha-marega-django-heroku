from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from app_projet.models import Project
from app_blog.models import BlogPost
from app_service.models import Service
from .models import SiteProfile


def acceuil(request):
    # Récupérer les 3 projets mis en avant
    # Récupérer les 3 projets mis en avant
    projets_featured = Project.objects.filter(featured=True, is_published=True)
    
    # Récupérer les articles de blog mis en avant
    articles_recents = BlogPost.objects.filter(is_published=True, featured=True)
    
    # Récupérer les 3 services mis en avant
    services = Service.objects.filter(is_published=True, featured=True)
    
    context = {
        'projets': projets_featured,
        'articles': articles_recents,
        'services': services,
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
