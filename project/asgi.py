"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# 1. تعيين إعدادات المشروع أولاً وقبل كل شيء
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# 2. تهيئة تطبيق الـ HTTP الأساسي
django_asgi_app = get_asgi_application()

# 3. الآن بعد أن تم تهيئة الإعدادات، نقوم باستيراد مكتبات الـ Channels وتطبيقنا بأمان
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import product.routing

# 4. تجميع البروتوكولات (HTTP و WebSocket)
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            product.routing.websocket_urlpatterns
        )
    ),
})