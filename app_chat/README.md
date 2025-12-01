app_chat

But
- Fournir (ou servir de base pour) une fonctionnalité de chat/messagerie du site.

Architecture possible
- `models.py` : stockage des messages et salons (si implémenté en base).
- `views.py` : endpoints pour l'affichage ou la gestion des messages.
- `templates/app_chat/` : interface utilisateur du chat.

Notes d'implémentation
- Pour le chat en temps réel, utiliser Django Channels et Redis pour le backend des WebSocket.
- Alternativement, intégrer un service tiers (Pusher, Ably) pour simplifier la mise en production.

Exécution locale
- Si Channels est ajouté, exécuter `daphne` ou configurer `runserver` pour supporter ASGI.

Tests & sécurité
- Valider la sanitation des messages pour éviter l'injection XSS.
- Ajouter des tests d'intégration pour le flux message/send/receive si possible.
