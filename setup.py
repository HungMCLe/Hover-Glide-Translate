from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account

# Path to your service account JSON key file
service_account_json = 'your Json File here'

# Load the credentials from the service account JSON key file
credentials = service_account.Credentials.from_service_account_file(service_account_json)

# Create clients for both Vision API and Translation API using the same credentials
vision_client = vision.ImageAnnotatorClient(credentials=credentials)
translate_client = translate.Client(credentials=credentials)