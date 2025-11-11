import os
from app import app as application

# Optional: set the FLASK_SECRET from environment or default
if 'FLASK_SECRET' not in os.environ:
    os.environ['FLASK_SECRET'] = 'please-change-this-in-production'
