from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages

from .models import SiteProfile
from .services import ProfileService


def acceuil(request):
    """
    Vue pour le profil par défaut à la racine /.
    
    Récupère le profil par défaut et construit le contexte avec le contenu
    mis en avant en utilisant le service ProfileService.
    
    Args:
        request: L'objet HttpRequest.
        
    Returns:
        HttpResponse avec le rendu du template acceuil.html.
    """
    site_profile = SiteProfile.objects.get_default_profile()
    context = ProfileService.build_profile_context(site_profile)
    return render(request, 'app_acceuil/acceuil.html', context)


def profile_home(request, nom=None, profession=None):
    """
    Vue pour un profil spécifique avec paramètres dans le chemin.
    
    Construit le slug à partir des paramètres nom et profession, récupère
    le profil correspondant et construit le contexte avec le service.
    
    Args:
        request: L'objet HttpRequest.
        nom: Le nom du profil (extrait de l'URL).
        profession: La profession du profil (extrait de l'URL).
        
    Returns:
        HttpResponse avec le rendu du template acceuil.html, ou redirect si paramètres manquants.
    """
    # Construire le slug du profil à partir des paramètres
    profile_slug = f"{nom}-{profession}" if nom and profession else ""
    
    if not profile_slug:
        # Si pas de paramètres, rediriger vers la racine
        return redirect('acceuil')
    
    # Charger le profil spécifique par son slug avec le manager optimisé
    site_profile = get_object_or_404(
        SiteProfile.objects.get_published_with_content(),
        slug=profile_slug
    )
    
    # Construire le contexte avec le service
    context = ProfileService.build_profile_context(site_profile)
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
