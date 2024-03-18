"""
ASGI config for vekariya_erp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vekaria_erp.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

# Now we can import Django models and other components
from vekaria_erp.token_auth_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({

    'http':get_asgi_application(),
    'websocket': TokenAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),

    
})
