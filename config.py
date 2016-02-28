
# DB URI
# example DB URI:
# mysql+oursql://scott:tiger@localhost/mydatabase
# postgresql+psycopg2://scott:tiger@localhost/mydatabase
SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:root@localhost/project'
# example
#SQLALCHEMY_DATABASE_URI = 'mysql+oursql://root:mysql@localhost/project'

# Debug from SQLAlchemy
# Turn this to False on production
SQLALCHEMY_ECHO = True

# List of allowed origins for CORS
ALLOWED_ORIGINS = "['*']"

# List of allowed IPs
WHITELIST_IPS = ["127.0.0.1"]

# Configure your log paths
#LOG_FILE = 'outreach.log'

# Log level for the application
#LOG_LEVEL = 'DEBUG'

# destination for uploaded files
# example value - '/home/vlead/Desktop/outreach-portal/build/code/src/static/uploads/'
#UPLOAD_DIR_PATH = '/home/vlead/Desktop/outreach-portal/build/code/src/static/uploads/'

#DB_PATH = '/static/uploads/'

# allowed file extensions that can be uploaded
#ALLOWED_FILE_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv']

#APP_URL
APP_URL = "http://localhost:5000"

#Persona Verifier URL
#PERSONA_VERIFIER_URL = "https://verifier.login.persona.org/verify"
