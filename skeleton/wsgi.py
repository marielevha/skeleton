import os

from django.core.wsgi import get_wsgi_application
import threading
from scraping import runner as rs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skeleton.settings')

application = get_wsgi_application()


# LAUNCH SCRAPING IN BACKGROUND
run = threading.Thread(target=rs.launch_schedule)
run.start()
