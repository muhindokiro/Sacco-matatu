import urllib.request,json
from .models import Owners
# Getting api key
api_key = None
# Getting the movie base url
base_url = None
def configure_request(app):
   global api_key,base_url
   api_key = app.config['OWNERS_API_KEY']
   base_url = app.config['OWNERS_API_BASE_URL']