from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, get_connection
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
    """
    Gère les soumissions du formulaire de contact.
    
    Envoie deux emails :
    1. Notification au propriétaire du profil (Gmail configuré)
    2. Email de confirmation à l'expéditeur (si activé)
    
    Champs du formulaire:
    - name (obligatoire)
    - email (obligatoire)
    - company (optionnel)
    - profession (optionnel)
    - subject (obligatoire)
    - message (obligatoire)
    """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        name = request.POST.get('name', '').strip()
        sender_email = request.POST.get('email', '').strip()
        company = request.POST.get('company', '').strip()
        profession = request.POST.get('profession', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_body = request.POST.get('message', '').strip()

        # Récupérer le profil pour les messages personnalisés
        profile = SiteProfile.objects.first()
        
        # Vérifier que le profil a les identifiants Gmail configurés
        if not profile or not profile.email or not profile.gmail_app_password:
            error_msg = "La configuration email n'est pas complète. Veuillez contacter l'administrateur."
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', reverse('acceuil')))

        recipient = profile.email

        # Configurer la connexion email avec les identifiants de la base de données
        email_connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            username=profile.email,
            password=profile.gmail_app_password,
            use_tls=True,
            fail_silently=False
        )

        # === EMAIL 1 : Notification au propriétaire ===
        owner_subject = f"{subject} - Message de {name}"
        owner_message = f"""
Nouveau message reçu depuis le formulaire de contact

DE: {name}
EMAIL: {sender_email}
{f'ENTREPRISE: {company}' if company else ''}
{f'PROFESSION: {profession}' if profession else ''}

OBJET: {subject}

MESSAGE:
{message_body}

---
Ce message a été envoyé via le formulaire de contact de votre site web.
Pour répondre, utilisez l'adresse: {sender_email}
        """

        try:
            # Envoyer l'email au propriétaire
            send_mail(
                owner_subject,
                owner_message.strip(),
                profile.email,     # From: email du propriétaire
                [recipient],       # To: email du propriétaire
                connection=email_connection,
                fail_silently=False
            )
            
            # === EMAIL 2 : Confirmation à l'expéditeur ===
            if profile and profile.enable_confirmation_email:
                confirmation_subject = f"Confirmation de réception - {subject}"
                confirmation_message = f"""
Bonjour {name},

Merci de m'avoir contacté. J'ai bien reçu votre message concernant "{subject}".

Je vous répondrai dans les plus brefs délais à l'adresse {sender_email}.

Voici un récapitulatif de votre message :
{'-' * 50}
{message_body}
{'-' * 50}

Cordialement,
{profile.first_name + ' ' + profile.last_name if profile.first_name else 'L\'équipe'}

---
Ceci est un email automatique, merci de ne pas y répondre.
                """
                
                send_mail(
                    confirmation_subject,
                    confirmation_message.strip(),
                    profile.email,    # From: email du propriétaire
                    [sender_email],   # To: email de l'expéditeur
                    connection=email_connection,
                    fail_silently=True  # Ne pas bloquer si ça échoue
                )
            
            # Message de succès
            success_msg = profile.contact_success_message if profile and profile.contact_success_message else "Merci ! Votre message a été envoyé avec succès."
            messages.success(request, success_msg)
            
        except BadHeaderError:
            error_msg = profile.contact_error_message if profile and profile.contact_error_message else "En-tête invalide détecté. Le message n'a pas été envoyé."
            messages.error(request, error_msg)
        except Exception as exc:
            error_msg = profile.contact_error_message if profile and profile.contact_error_message else f"Une erreur s'est produite lors de l'envoi du message."
            messages.error(request, error_msg)
            # Log l'erreur pour le debug
            print(f"Erreur envoi email: {exc}")

        return redirect(request.META.get('HTTP_REFERER', reverse('acceuil')))

    # Si GET, rediriger vers la page d'accueil
    return redirect(reverse('acceuil'))

