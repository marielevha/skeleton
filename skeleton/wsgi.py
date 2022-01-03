"""
WSGI config for skeleton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import threading
from scraping import run as rs
from scraping import models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skeleton.settings')

application = get_wsgi_application()


# LAUNCH SCRAPING IN BACKGROUND
run = threading.Thread(target=rs.launch_schedule)
run.start()
